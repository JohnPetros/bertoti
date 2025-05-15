from datetime import datetime
from json import loads

from google.adk.runners import Runner as AdkRunner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from sqlite3 import connect

from src.chatbot.agent import chatbot_agent
from src.core.structures import ChatMessage


class Runner:
    def __init__(self):
        self.app_name = "Stocker Chatbot"
        self.session_service = DatabaseSessionService(db_url="sqlite:///./sqlite.db")

    async def answer_message(
        self,
        query: str,
        company_id: str,
        user_id: str,
        session_id: str,
    ):
        initial_state = {
            "user_id": user_id,
            "company_id": company_id,
        }
        session = self.session_service.get_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id,
        )

        if session:
            session_id = session.id
        else:
            session = self.session_service.create_session(
                app_name=self.app_name,
                user_id=user_id,
                state=initial_state,
            )
            session_id = session.id

        runner = AdkRunner(
            agent=chatbot_agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )

        self.__add_user_query_to_history(user_id, session_id, query)

        print(f"Query: {query}")
        print(f"Session ID: {session_id}")

        agent_response = await self.__call_agent_async(
            runner=runner,
            user_id=user_id,
            session_id=session_id,
            query=query,
        )
        return agent_response

    def get_all_messages(self, user_id: str, session_id: str):
        with connect("./sqlite.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT content, timestamp FROM events 
                WHERE user_id = ? AND session_id = ? AND content LIKE ?
                """,
                (user_id, session_id, '%{"parts": [{"text":%'),
            )
            chat_messages = []
            for row in cursor.fetchall():
                data = loads(row[0])
                sent_at = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f")
                sent_at = sent_at.replace(microsecond=0)

                chat_messages.append(
                    ChatMessage(
                        sender="user" if data["role"] == "user" else "bot",
                        content=data["parts"][0]["text"],
                        sent_at=sent_at,
                    )
                )
            return chat_messages

    def __update_history(self, user_id: str, session_id: str, entry: dict):
        try:
            session = self.session_service.get_session(
                app_name=self.app_name, user_id=user_id, session_id=session_id
            )

            interaction_history = session.state.get("interaction_history", [])

            if "timestamp" not in entry:
                entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            interaction_history.append(entry)

            updated_state = session.state.copy()
            updated_state["interaction_history"] = interaction_history

            self.session_service.create_session(
                app_name=self.app_name,
                user_id=user_id,
                session_id=session_id,
                state=updated_state,
            )
        except Exception as e:
            print(f"Error updating interaction history: {e}")
            pass

    def __add_user_query_to_history(self, user_id: str, session_id: str, query: str):
        self.__update_history(
            user_id,
            session_id,
            {
                "action": "user_query",
                "query": query,
            },
        )

    def __add_agent_response_to_history(
        self, user_id: str, session_id: str, agent_name: str, response: str
    ):
        self.__update_history(
            user_id,
            session_id,
            {
                "action": "agent_response",
                "agent": agent_name,
                "response": response,
            },
        )

    async def __process_agent_response(self, event):
        final_response = None
        if event.is_final_response():
            if (
                event.content
                and event.content.parts
                and hasattr(event.content.parts[0], "text")
                and event.content.parts[0].text
            ):
                final_response = event.content.parts[0].text.strip()

        return final_response

    async def __call_agent_async(self, runner, user_id, session_id, query):
        content = types.Content(role="user", parts=[types.Part(text=query)])
        final_response_text = None
        agent_name = None

        try:
            async for event in runner.run_async(
                user_id=user_id, session_id=session_id, new_message=content
            ):
                if event.author:
                    agent_name = event.author

                response = await self.__process_agent_response(event)
                if response:
                    final_response_text = response
        except Exception as e:
            print(f"ERROR during agent run: {e}")

        if final_response_text and agent_name:
            self.__add_agent_response_to_history(
                user_id,
                session_id,
                agent_name,
                final_response_text,
            )

        return final_response_text
