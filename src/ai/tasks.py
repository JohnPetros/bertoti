from textwrap import dedent

from crewai import Agent, Task


class ChatbotTasks:
    def resolve_question(self, agent: Agent):
        return Task(
            agent=agent,
            description=dedent(
                """
                Your task is to resolve the following user question by analyzing its content and delegating it to the appropriate support agent.
                Be aware the question is always in Portuguese language.

                Question: "{question}"
                
                The history of the conversation is:
                "{history}"

                Determine whether to route to:
                - Technical Support Agent (for Stocker interface, pricing, limitations, services - based on official docs)
                - Database Support Agent (for stock data analysis)

                Break complex questions into parts if needed. Provide clear, friendly responses.
                Do not mention the user or the company id in the answer.
                The answer must be in Portuguese language.
                The answer must be in a short and concise format.
                Do not say technical details about database in the answer.
                """
            ),
            max_retries=3,
            expected_output="A complete and user-friendly answer that may include delegated insights from the appropriate agents.",
        )

    def answer_technical_question(self, agent: Agent):
        return Task(
            agent=agent,
            description=dedent(
                """
                Your task is to analyze and respond to the user question with a clear, accurate explanation.

                Base your answer **strictly on Stocker's official user guide and FAQ**. If information isn't in these docs, politely decline to answer.

                Keep the response simple and user-friendly.
                
                User question: {question}
                """
            ),
            max_retries=3,
            expected_output="A clear, concise, and user-friendly answer based on the official documentation.",
        )

    def answer_database_question(self, agent: Agent):
        return Task(
            agent=agent,
            description=dedent(
                """
                Query the database for company ID: {company_id} to answer: {question}

                SELECT only
                No mutations allowed
                """
            ),
            max_retries=3,
            expected_output="A human answer to the user question without any sql query.",
        )
