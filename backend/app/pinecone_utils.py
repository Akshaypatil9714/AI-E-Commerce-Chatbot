import os
from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as LangChainPinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from .embeddings import embedding_model
import traceback
import numpy as np
from sklearn.preprocessing import normalize

# Use the model name instead of the embedding model object
model_name = 'sentence-transformers/all-MiniLM-L6-v2'

# Create HuggingFaceEmbeddings using the model name
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# Set the API key as an environment variable
os.environ['PINECONE_API_KEY'] = "your-secret-key"

# Initialize the Pinecone instance
pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])

index_name = "ecommerce-chatbot"

# Create the index once and store it
pinecone_index = None

def get_pinecone_index():
    global pinecone_index
    if pinecone_index is None:
        try:
            if index_name not in pc.list_indexes().names():
                pc.create_index(
                    name=index_name, 
                    dimension=384, 
                    metric='cosine',
                    spec=ServerlessSpec(cloud='aws', region='us-east-1')
                )
            pinecone_index = pc.Index(index_name)
            print(f"Index {index_name} created and loaded successfully.")
        except Exception as e:
            print(f"Error creating Pinecone index: {e}")
    return pinecone_index

def load_knowledge_base(knowledge_base):
    try:
        documents = []
        for item in knowledge_base['knowledge_base']:
            if isinstance(item['content'], list):
                for content in item['content']:
                    documents.append(Document(page_content=content['message'], metadata=item['metadata']))
            elif isinstance(item['content'], dict):
                combined_content = []
                for k, v in item['content'].items():
                    if isinstance(v, str):
                        combined_content.append(f"{k}: {v}")
                    elif isinstance(v, list):
                        features = [f"{feat.get('feature', '')}: {feat.get('description', '')}" for feat in v]
                        combined_content.append(f"{k}: {', '.join(features)}")
                combined_content = "\n".join(combined_content)
                documents.append(Document(page_content=combined_content.strip(), metadata=item['metadata']))

        vector_store = LangChainPinecone.from_documents(documents, embeddings, index_name=index_name)
        print(f"Documents successfully added to index: {len(documents)}")
        return vector_store
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        traceback.print_exc()
        return None

def query_pinecone(query):
    try:
        index = get_pinecone_index()
        if index is None:
            raise ValueError("Pinecone index is None.")

        query_embedding = embeddings.embed_query(query)
        query_embedding = normalize(np.array(query_embedding, dtype=np.float32).reshape(1, -1))[0].tolist()
        
        vector_store = LangChainPinecone.from_existing_index(index_name, embeddings)
        
        results = vector_store.similarity_search_with_score(query, k=5)
        
        return [{'content': doc.page_content, 'metadata': doc.metadata, 'score': float(score)} for doc, score in results]
    except Exception as e:
        print(f"Error querying Pinecone: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return []

def build_context(results):
    try:
        return "\n\n".join(f"Content: {r['content']}\nCategory: {r['metadata'].get('category', 'N/A')}\nTags: {', '.join(r['metadata'].get('tags', []))}\nRelevance Score: {r['score']}" for r in results)
    except Exception as e:
        print(f"Error building context: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return ""