from os import getenv, environ


from crewai import Crew, Process, LLM
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

from src.core.structures import ChatMessage
from src.database import chat_message_repository

from .agents import ChatbotAgents
from .tasks import ChatbotTasks
from .tools import ChabotTools

environ["CREWAI_DISABLE_TELEMETRY"] = "true"


class ChatbotSquad:
    def __init__(self):
        deepseek_llm = self.__get_deepseek_llm()
        gemma_llm = self.__get_gemma_llm()
        llama_llm = self.__get_llama_llm()
        # mistral_llm = self.__get_mistral_llm()
        gemini_llm = self.__get_gemini_llm()
        qwen_llm = self.__get_qwen_llm()

        database_tools = [
            ChabotTools.list_database_tables,
            ChabotTools.describe_database_tables,
            ChabotTools.execute_sql_query,
        ]

        text_source = TextFileKnowledgeSource(
            file_paths=["faq.txt"],
        )
        pdf_source = PDFKnowledgeSource(file_paths=["user-guide.pdf"])

        agents = ChatbotAgents()
        leader_support = agents.leader_support(deepseek_llm)
        technical_support = agents.technical_support(
            [text_source, pdf_source], gemma_llm
        )
        database_support = agents.database_support(database_tools, gemma_llm)

        tasks = ChatbotTasks()
        resolve_question = tasks.resolve_question(leader_support)
        answer_tchnical_question = tasks.answer_technical_question(technical_support)
        answer_database_question = tasks.answer_database_question(database_support)

        self.__crew = Crew(
            agents=[
                technical_support,
                database_support,
            ],
            tasks=[
                resolve_question,
                answer_tchnical_question,
                answer_database_question,
            ],
            process=Process.hierarchical,
            verbose=True,
            manager_agent=leader_support,
            embedder={
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": getenv("GEMINI_API_KEY"),
                },
            },
        )

    def start(self, question: str, company_id: str, user_id: str) -> str:
        history = self.__get_history(company_id, user_id)
        # self.__save_history(question, "user", company_id, user_id)

        answer = self.__crew.kickoff(
            inputs={"question": question, "company_id": company_id, "history": history},
        )

        # self.__save_history(answer.raw, "bot", company_id, user_id)

        return answer.raw

    def __save_history(
        self, messageContent: str, sender: str, company_id: str, user_id: str
    ):
        message = ChatMessage(
            content=messageContent,
            sender=sender,
            company_id=company_id,
            user_id=user_id,
        )
        chat_message_repository.add(message)

    def __get_history(self, company_id: str, user_id: str) -> str:
        messages = chat_message_repository.find_many_by_user_and_company(
            user_id, company_id
        )
        return "\n".join(
            [f"{message.sender}: {message.content}" for message in messages]
        )

    def __get_deepseek_llm(self):
        api_key = getenv("OPEN_ROUTER_API_KEY")
        llm = LLM(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model="openrouter/deepseek/deepseek-r1:free",
            temperature=0,
        )
        return llm

    def __get_qwen_llm(self) -> LLM:
        api_key = getenv("OPEN_ROUTER_API_KEY")
        llm = LLM(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model="openrouter/qwen/qwen3-235b-a22b:free",
            temperature=0,
        )
        return llm

    def __get_gemma_llm(self):
        api_key = getenv("OPEN_ROUTER_API_KEY")
        llm = LLM(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model="openrouter/google/gemma-3-27b-it:free",
            temperature=0,
        )
        return llm

    def __get_llama_llm(self):
        api_key = getenv("OPEN_ROUTER_API_KEY")
        llm = LLM(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model="openrouter/meta-llama/llama-4-maverick:free",
            temperature=0,
        )
        return llm

    def __get_mistral_llm(self):
        groq_api_key = getenv("GROQ_API_KEY")
        llm = LLM(
            api_key=groq_api_key,
            model="groq/mistral-saba-24b",
            max_tokens=600,
            temperature=0,
        )
        return llm

    def __get_gemini_llm(self):
        groq_api_key = getenv("GEMINI_API_KEY")
        llm = LLM(
            api_key=groq_api_key,
            model="gemini/gemini-1.5-flash",
            max_tokens=600,
            temperature=0,
        )
        return llm
