from textwrap import dedent

from crewai import Agent, Task


class ChatbotTasks:
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
                """
            ),
        )

    def answer_database_question(self, agent: Agent):
        return Task(
            agent=agent,
            description=dedent(
                """
                Perform a read-only query in a relational database for the company with ID: {company_id} for the question: {question}

                ✅ Only SELECT operations are allowed.  
                ❌ No INSERT, UPDATE, DELETE, or any other mutation operations are permitted.

                All queries must return **no more than 10 rows**.
                """
            ),
            expected_output="An answer to the question without including any sql query or result.",
        )
