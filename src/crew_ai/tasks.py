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

            Carefully determine whether the question should be answered by:
            - The Technical Support Agent (for questions about using the Stocker interface or understanding product behavior such as princing, limitations, available services etc. Always based on the official FAQ and user guide documentations)
            - The Database Support Agent (for questions requiring access to or analysis of the company's stock data)

            If needed, break the question into smaller parts and assign them accordingly. Your final response should be clear, friendly, and helpful.
            """
            ),
            expected_output="A complete and user-friendly answer that may include delegated insights from the appropriate agents.",
        )

    def answer_technical_question(self, agent: Agent):
        return Task(
            agent=agent,
            description=dedent(
                """
                Your task is to carefully analyze the following user question and respond with a clear, accurate, and friendly explanation.

                You must base your answer **strictly on the official Stocker user guide and the .FAQ documentation**. Do not use any other sources or assumptions.

                If the information required is not covered in those documents, politely inform the user that you cannot provide an answer.

                Ensure your response is easy to understand, even for users with little or no technical background.
                
                The answer must be less than 25 words.

                User question: {question}
                """,
            ),
            expected_output="A clear, concise, and user-friendly answer based on the official documentation.",
        )

    def answer_database_question(self, agent: Agent):
        return Task(
            agent=agent,
            description=dedent(
                """
                Perform a read-only query in a relational database for the company with ID: {company_id} for the question: {question}

                ✅ Only SELECT operations are allowed.  
                ❌ No INSERT, UPDATE, DELETE, or any other mutation operations are permitted.
                """
            ),
            expected_output="A human answer to the user question without any sql query.",
        )
