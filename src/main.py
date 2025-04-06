from crew_ai import chatbot_squad
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    chatbot_squad.start(
        question="What questions are there in the FAQ?",
        company_id="29fcf7a0-5ee3-4cb0-b36e-ecc825f1cdaa",
    )
