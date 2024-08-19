import numpy as np
from pinecone import Pinecone, Index, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.preprocessing import normalize

# Initialize the Pinecone instance with the API key
pc = Pinecone(
    api_key="3ee8f782-0d78-4e7a-a904-5c1fcbfca973"
)

# Define the model name for embeddings
model_name = 'sentence-transformers/all-MiniLM-L6-v2'

# Initialize the HuggingFace embeddings
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# Pinecone index initialization with the correct host and region
index_name = "ecommerce-chatbot"

# Ensure the index exists and is correctly initialized
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name, 
        dimension=384, 
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',  
            region='us-east-1'
        )
    )

# Get the index object
index = pc.Index(index_name)

# Describe the index to get its details
index_info = index.describe_index_stats()
print(f"Index dimension: {index_info['dimension']}")

try:
    # Create the query and generate its embedding
    query = "What is the return policy?"
    query_embedding = embeddings.embed_query(query)
    
    # Convert the embedding to a NumPy array of type float32
    query_embedding = np.array(query_embedding, dtype=np.float32)
    
    # Normalize the embedding to ensure all values are between -1 and 1
    query_embedding = normalize(query_embedding.reshape(1, -1), norm='l2')[0]
    
    # Convert the embedding to a list of floats
    query_embedding = query_embedding.tolist()
    
    print(f"Query embedding generated for: '{query}'")
    print(f"Query embedding shape: {len(query_embedding)}")

    # Perform the query on the Pinecone index
    results = index.query(vector=query_embedding, top_k=5, include_metadata=True)
    print(f"Test results: {results}")
except Exception as e:
    print(f"Error during test query: {type(e).__name__}: {e}")
