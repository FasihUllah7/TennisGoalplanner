# agent_logic.py
import json
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import os

# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Initialize LLM and Memory ---
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

def parse_goal_request(user_input: str):
    """
    Takes a user goal request and returns structured goal details.
    """
    prompt = f"""
    You are an AI Tennis Goal Planner.
    Convert the user's goal request into a structured format with these fields:
    - Goal Type (Technical, Tactical, Physical, Mental)
    - Topic
    - Subject
    - Date (infer if not given)
    - Time (if mentioned)
    - About Goal (a motivational one-liner)

    Respond strictly in valid JSON format.
    
    Example:
    {{
        "Goal Type": "Technical",
        "Topic": "Serve Accuracy",
        "Subject": "Improve my serve consistency",
        "Date": "2025-10-20",
        "Time": "17:00",
        "About Goal": "Focus on improving toss and follow-through"
    }}

    User Input: {user_input}
    """

    try:
        result = conversation.run(prompt)
        structured_goal = json.loads(result)
        return structured_goal
    except Exception as e:
        return {"error": f"Failed to parse goal: {str(e)}", "raw_response": result}
