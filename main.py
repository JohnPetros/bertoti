import asyncio
from dotenv import load_dotenv

from chatbot import chatbot_agent
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from src.utils import add_user_query_to_history, call_agent_async

load_dotenv()

session_service = DatabaseSessionService(db_url="sqlite:///./sqlite.db")


async def main_async():
    APP_NAME = "Stocker Chatbot"
    USER_ID = "aiwithbrandon"
    SESSION_ID = None

    initial_state = {
        "user_name": "Brandon Hancock",
        "company_id": "29fcf7a0-5ee3-4cb0-b36e-ecc825f1cdaa",
    }

    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME, user_id=USER_ID
    )
    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        new_session = session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")

    runner = Runner(
        agent=chatbot_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("\nWelcome to Stocker Chatbot!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        add_user_query_to_history(
            session_service, APP_NAME, USER_ID, SESSION_ID, user_input
        )

        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
