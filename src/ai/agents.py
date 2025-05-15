from textwrap import dedent

from crewai import Agent, LLM
from langchain.tools import BaseTool

from crewai.knowledge.source.pdf_knowledge_source import BaseFileKnowledgeSource


class ChatbotAgents:
    def leader_support(self, llm: LLM) -> Agent:
        return Agent(
            role="Leader Support",
            goal="Efficiently triage and delegate user requests to the appropriate support agent based on the nature of the issue.",
            backstory=dedent(
                """
                As the Lead Support Coordinator for Stocker, an inventory management SaaS platform, your role is pivotal in assisting small to mid-sized companies with inventory tracking and optimization.

                Key Responsibilities:
                1. Assess and diagnose the core issues in user requests.
                2. Direct inquiries to the appropriate support team:
                   - Technical Support: Handles interface navigation, feature usage, and platform functionality.
                   - Database Support: Manages inventory data queries, stock levels, and data analysis.
                3. Facilitate efficient support by:
                   - Swiftly identifying the appropriate specialist.
                   - Providing relevant context when delegating tasks.
                   - Ensuring resolution through follow-ups.

                Maintain a professional and courteous demeanor while guiding users to the most suitable specialist for their needs.
                """
            ),
            llm=llm,
            allow_delegation=True,
            verbose=True,
            max_iter=3,
            max_retries=3,
        )

    def technical_support(
        self, sources: list[BaseFileKnowledgeSource], llm: LLM
    ) -> Agent:
        return Agent(
            role="Technical Support",
            goal="Provide clear and accurate technical assistance to users regarding how to use Stocker, strictly based on the official user guide and the .FAQ documentation (both written in Portuguese).",
            backstory=dedent(
                """
                You are a Technical Support Specialist for Stocker platform, expert in the official user guide.

                Guidelines:
                - Use only official FAQ and user guide
                - Delegate company-specific data questions to Database Support
                - Politely decline if answer isn't in docs
                - Be clear and professional
                """
            ),
            llm=llm,
            max_iter=3,
            allow_delegation=True,
            verbose=True,
            knowledge_sources=sources,
        )

    def database_support(self, database_tools: list[BaseTool], llm: LLM) -> Agent:
        return Agent(
            role="Database Support",
            goal="Help users retrieve and understand stock-related data from a relational database, providing accurate and relevant query results.",
            backstory=dedent(
                """
                You are a Database Administrator for Stocker, specializing in efficient queries and data integrity.
                Help users retrieve and understand their company's stock data.

                Company id: {company_id}
                
                Tools:
                - `list_database_tables`: view available tables
                - `describe_database_tables`: view table metadata
                - `execute_sql`: validate queries
                """
            ),
            tools=database_tools,
            allow_delegation=True,
            llm=llm,
            verbose=True,
            max_iter=3,
        )
