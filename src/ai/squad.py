from os import getenv
from datetime import datetime
from json import dumps, loads

from crewai import Crew, Process, LLM
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

from .agents import ChatbotAgents
from .tasks import ChatbotTasks
from .tools import ChabotTools
from ..cache.redis_cache import RedisCache


class ChatbotSquad:
    def __init__(self):
        # deepseek_llm = self.__get_deepseek_llm()
        # gemma_llm = self.__get_gemma_llm()
        # llama_llm = self.__get_llama_llm()
        # mistral_llm = self.__get_mistral_llm()
        gemini_llm = self.__get_gemini_llm()
        qwen_llm = self.__get_qwen_llm()
        self.__cache = RedisCache()

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
        leader_support = agents.leader_support(qwen_llm)
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

    def start(self, question: str, company_id: str, user_id: str) -> str:
        cache_key = f"company:{company_id}:user:{user_id}:messages"

        history = self.__get_history(cache_key)
        self.__update_history(cache_key, "user", question)

        answer = self.__crew.kickoff(
            inputs={"question": question, "company_id": company_id, "history": history},
        )

        self.__update_history(cache_key, "bot", answer.raw)

        return answer.raw

    def save_message(self, messageContent: str, sender: str):
        message = {
            "content": messageContent,
            "sender": sender,
            "timestamp": datetime.now().isoformat(),
        }
        key = f"company:{self.company_id}:user:{self.user_id}:messages"
        self._cache.add_item(key, dumps(message))

    def __get_deepseek_llm(self):
        groq_api_key = getenv("GROQ_API_KEY")
        llm = LLM(
            api_key=groq_api_key,
            model="groq/deepseek-r1-distill-llama-70b",
            max_tokens=1250,
            temperature=0,
        )
        return llm

    def __get_qwen_llm(self) -> LLM:
        api_key = getenv("OPEN_ROUTER_API_KEY")
        print("api_key", api_key)
        llm = LLM(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model="openrouter/qwen/qwq-32b:free",
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

    def __get_history(self, key: str) -> str:
        messages = self.__cache.get_last_items(key)
        history = "No message yet"

        for message in messages:
            message = loads(message)
            history += f"{message['sender']}: {message['content']}\n"
        return history

    def __update_history(self, key: str, sender: str, message_content: str) -> None:
        message = {
            "content": message_content,
            "sender": sender,
            "timestamp": datetime.now().isoformat(),
        }
        self.__cache.add_item(key, dumps(message))
