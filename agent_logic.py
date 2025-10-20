# agent_logic.py
import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in environment. Please check your .env file.")

# --- Initialize LLM and Memory ---
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

def parse_goal_request(user_input: str):
    """
    Takes a user goal request and returns structured goal details as JSON.
    """

    prompt = f"""
    You are an AI Tennis Goal Planner.
    Convert the user's goal request into a structured JSON with these fields:
    - Goal Type (Technical, Tactical, Physical, Mental)
    - Topic
    - Subject
    - Date (infer if not given)
    - Time (if mentioned)
    - About Goal (a motivational one-liner)

    Respond ONLY with valid JSON. Do not include explanations or markdown.

    Example:
    {{
        "Goal Type": "Technical",
        "Topic": "Serve Accuracy",
        "Subject": "Improve my serve consistency",
