import os
from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as LangChainPinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import traceback
import numpy as np
from sklearn.preprocessing import normalize
from dotenv import load_dotenv
from pinecone.core.openapi.shared.exceptions import PineconeApiException

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'config.env'))

# Use the model name instead of the embedding model object
model_name = 'sentence-transformers/all-MiniLM-L6-v2'

# Create HuggingFaceEmbeddings using the model name
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# Set the API key as an environment variable
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

if PINECONE_API_KEY is None:
    raise ValueError("PINECONE_API_KEY environment variable not set")

# Initialize the Pinecone instance
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "ecommerce-chatbot"

# Create the index once and store it
pinecone_index = None

def get_pinecone_index():
    global pinecone_index
    if pinecone_index is None:
        try:
            # Check if the index already exists
            indexes = pc.list_indexes()
            if index_name not in indexes:
                print(f"Index {index_name} not found. Creating a new index.")
                pc.create_index(
                    name=index_name, 
                    dimension=384, 
                    metric='cosine',
                    spec=ServerlessSpec(cloud='aws', region='us-east-1')
                )
                print(f"Index {index_name} created successfully.")
            else:
                print(f"Index {index_name} already exists, loading it.")

            # Load the existing index
            pinecone_index = pc.Index(index_name)
            print(f"Index {index_name} loaded successfully.")
        except PineconeApiException as e:
            # Handle the specific conflict error
            if e.status == 409:
                print(f"Index {index_name} already exists, conflict error handled.")
                pinecone_index = pc.Index(index_name)
            else:
                print(f"Error during Pinecone index creation or loading: {e}")
                traceback.print_exc()
                pinecone_index = None
        except Exception as e:
            print(f"Unexpected error during Pinecone index creation or loading: {e}")
            traceback.print_exc()
            pinecone_index = None
    return pinecone_index


def load_knowledge_base(knowledge_base):
    index = get_pinecone_index()
    if index is None:
        raise ValueError("Pinecone index is None.")

    # Check if index already contains vectors, if so, skip reloading
    stats = index.describe_index_stats()
    if stats['total_vector_count'] > 0:
        print("Index already contains vectors, skipping loading knowledge base.")
        return LangChainPinecone.from_existing_index(index_name, embeddings)
    
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
        
        # Log the retrieved content and metadata
        print("Retrieved Documents:")
        for doc, score in results:
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")
            print(f"Relevance Score: {score}")
            print("-" * 50)
        
        return [{'content': doc.page_content, 'metadata': doc.metadata, 'score': float(score)} for doc, score in results]
    except Exception as e:
        print(f"Error querying Pinecone: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return []

def build_context(results, max_length=500):
    try:
        # Sort results by relevance score
        results = sorted(results, key=lambda x: x['score'], reverse=True)
        
        # Collect content until we reach the max length
        context_pieces = []
        current_length = 0
        for r in results:
            content = r['content']
            if current_length + len(content) > max_length:
                break
            context_pieces.append(content)
            current_length += len(content)
        
        # Join selected content pieces
        context = "\n\n".join(context_pieces)
        return context
    except Exception as e:
        print(f"Error building context: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return ""
