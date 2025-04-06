from os import getenv

from crewai import Crew, Process, LLM
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from dotenv import load_dotenv

from .agents import ChatbotAgents
from .tasks import ChatbotTasks
from .tools import ChabotTools

load_dotenv()


class ChatbotSquad:
    def __init__(self):
        deepseek_llm = self.__get_deepseek_llm()
        gemma_llm = self.__get_gemma_llm()
        llama_llm = self.__get_llama_llm()
        qwen_llm = self.__get_qwen_llm()
        mistral_llm = self.__get_mistral_llm()
        gemini_llm = self.__get_gemini_llm()

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
        leader_support = agents.leader_support(llama_llm)
        technical_support = agents.technical_support(
            [text_source, pdf_source], gemini_llm
        )
        database_support = agents.database_support(database_tools, gemini_llm)

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

    def start(self, question: str, company_id: str):
        self.__crew.kickoff(inputs={"question": question, "company_id": company_id})

    def __get_deepseek_llm(self):
        groq_api_key = getenv("GROQ_API_KEY")
        llm = LLM(
            api_key=groq_api_key,
            model="groq/deepseek-r1-distill-llama-70b",
            max_tokens=1250,
            temperature=0,
        )
        return llm

    def __get_qwen_llm(self):
        groq_api_key = getenv("GROQ_API_KEY")
        llm = LLM(
            api_key=groq_api_key,
            model="groq/qwen-2.5-32b",
            max_tokens=600,
            temperature=0,
        )
        return llm

    def __get_gemma_llm(self):
        groq_api_key = getenv("GROQ_API_KEY")
        llm = LLM(
            api_key=groq_api_key,
            model="groq/gemma2-9b-it",
            max_tokens=600,
            temperature=0,
        )
        return llm

    def __get_llama_llm(self):
        groq_api_key = getenv("GROQ_API_KEY")
        llm = LLM(
            api_key=groq_api_key,
            model="groq/llama-3.3-70b-versatile",
            max_tokens=600,
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
