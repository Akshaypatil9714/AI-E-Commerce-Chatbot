import vertexai
from vertexai.generative_models import GenerativeModel
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'config.env'))

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Set your project ID and initialize Vertex AI
project_id = os.getenv("Gemini_Project_ID")
vertexai.init(project=project_id, location="us-central1")

def generate_response(context, query, max_time=60):
    try:
        model = GenerativeModel("gemini-1.5-flash-001")
        prompt = f"Context: {context[:500]}\n\nQuestion: {query}\n\nAnswer:"

        response = model.generate_content(
            prompt
        )

        return response.text.strip() if response else "Sorry, I couldn't generate a response."
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I couldn't generate a response due to an error."