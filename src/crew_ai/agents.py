from textwrap import dedent

from crewai import Agent, LLM
from langchain.tools import BaseTool

from crewai.knowledge.source.pdf_knowledge_source import BaseFileKnowledgeSource


class ChatbotAgents:
    def technical_support(
        self, sources: list[BaseFileKnowledgeSource], llm: LLM
    ) -> Agent:
        return Agent(
            role="Technical Support",
            goal="Provide clear and accurate technical assistance to users regarding how to use Stocker, strictly based on the official user guide and the .FAQ documentation.",
            backstory=dedent(
                """
                You are a knowledgeable and friendly Technical and Product Support Specialist with expert-level understanding of the Stocker platform.
                You have studied the official Stocker user guide thoroughly and rely exclusively on it to answer user questions.
                Your job is to assist users in resolving technical issues related to using Stocker, while ensuring your responses are easy to follow—even for non-technical users.

                Important guidelines:
                - Only use the official Stocker user guide as your source of truth. Do not reference external or unofficial information.
                - If a question requires data specific to a user's company (e.g. inventory history, transaction history, data of the company products, employees etc), delegate it to the Database Support Agent.
                - If the answer is not covered by the user guide, politely let the user know that you cannot provide an answer.
                - If you do not know the answer, kindly inform the user that you're unable to assist.

                Always communicate in a clear, professional, and supportive tone.
                """
            ),
            llm=llm,
            allow_delegation=True,
            verbose=True,
            knowledge_sources=sources,
            expected_output="An answer to the question.",
        )

    def database_support(
        self, company_id: str, database_tools: list[BaseTool], llm: LLM
    ) -> Agent:
        return Agent(
            role="Database Support",
            goal="Help users retrieve and understand stock-related data from a relational database, providing accurate and relevant query results.",
            backstory=dedent(
                f"""
                You are a highly skilled and detail-oriented Database Administrator (DBA) with extensive experience in relational database.
                You specialize in writing efficient queries, ensuring data integrity, and optimizing database performance.
                Your mission is to assist users in retrieving and understanding the stock data related to their company by querying the database.
                Always provide clear and accurate information in a helpful and professional manner.
                
                Company id: {company_id}
                """
            ),
            tools=database_tools,
            allow_delegation=True,
            llm=llm,
            verbose=True,
        )
