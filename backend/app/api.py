from fastapi import APIRouter, Request, HTTPException
from .gemini import generate_response
from .pinecone_utils import query_pinecone, get_pinecone_index, load_knowledge_base, build_context
import json
import asyncio

router = APIRouter()

# Load the knowledge base from the JSON file
with open("knowledge_base.json", "r") as file:
    knowledge_base = json.load(file)

# Create a Pinecone index
index = get_pinecone_index()

# Load the knowledge base into Pinecone
load_knowledge_base(knowledge_base)


@router.post("/chat/")
async def chat(request: Request):
    try:
        data = await request.json()
        query = data['query']

        results = query_pinecone(query)
        context = build_context(results)

        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(generate_response, context, query),
                timeout=60.0  # Increase timeout if necessary
            )
            print("response:", response)
        except asyncio.TimeoutError:
            response = "I'm sorry, but the response is taking too long to generate. Please try again with a simpler query."

        # Optionally include the retrieved documents in the response for debugging
        retrieved_docs = [{"content": r['content'], "metadata": r['metadata'], "score": r['score']} for r in results]

        return {
            "response": response,
            "retrieved_docs": retrieved_docs  # Include this if you want to see retrieved content
        }
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))