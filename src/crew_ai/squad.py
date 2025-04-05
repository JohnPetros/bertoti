from os import getenv
from datetime import datetime

from crewai import Crew, Process, LLM
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

        database_tools = [
            ChabotTools.list_database_tables,
            ChabotTools.describe_database_tables,
            ChabotTools.check_sql_query,
            ChabotTools.execute_sql_query,
        ]

        agents = ChatbotAgents()
        technical_support = agents.technical_support([], deepseek_llm)
        database_support = agents.database_support(database_tools, deepseek_llm)

        tasks = ChatbotTasks()
        answer_tchnical_question = tasks.answer_technical_question(technical_support)
        answer_database_question = tasks.answer_database_question(database_support)

        self.__crew = Crew(
            agents=[
                technical_support,
                database_support,
            ],
            tasks=[
                answer_tchnical_question,
                answer_database_question,
            ],
            process=Process.sequential,
            verbose=True,
        )

    def start(self):
        self.__crew.kickoff(
            inputs={"topic": "Tecnologia", "current_time": str(datetime.now())}
        )

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
            model="groq/llama3-70b-8192",
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
