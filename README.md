# AI Customer Service Chatbot with Google Gemini API Integration

This project is an AI-powered customer service chatbot that uses the Google Gemini API to generate context-aware responses based on queries. The system leverages a Retrieval-Augmented Generation (RAG) approach, integrating a knowledge base stored in Pinecone with the generative capabilities of Google Gemini.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The AI Customer Service Chatbot is designed to provide quick and accurate responses to customer queries by combining a knowledge base with the generative power of Google Gemini. The chatbot retrieves relevant information from a Pinecone vector store and uses Google Gemini to generate responses based on the retrieved context.

## Features

- **Context-Aware Responses**: Generates responses based on the context retrieved from the knowledge base.
- **RAG Integration**: Combines retrieval from Pinecone with generative responses from Google Gemini.
- **Flexible Deployment**: Can be run locally or deployed on a server.
- **Interactive Frontend**: Simple and user-friendly chat interface built with React.

## Architecture

The system follows a Retrieval-Augmented Generation (RAG) architecture:
1. **User Query**: A query is sent from the frontend to the backend.
2. **Document Retrieval**: The backend queries Pinecone to retrieve the most relevant documents from the knowledge base.
3. **Response Generation**: The retrieved context is sent to Google Gemini API, which generates a contextually relevant response.
4. **Response Delivery**: The generated response is sent back to the frontend and displayed to the user.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- Google Cloud account with Vertex AI API enabled
- Service account with access to Google Gemini API

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-customer-service-chatbot.git
   cd ai-customer-service-chatbot/backend

2. Set up a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

3. Set up your Google Cloud credentials:
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

4. Configure environment variables:
    - Create a .env file in the backend directory and add your configuration:
        ```bash
        GOOGLE_PROJECT_ID=your-google-cloud-project-id
        GEMINI_ENDPOINT_ID=your-gemini-endpoint-id

5. Run the backend:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000

### Frontend Setup

1. Navigate to the frontend directory:
    ```bash
    cd ../frontend

2. Install dependencies:
    ```bash
    npm install

3. Run the frontend:
    ```bash
    npm start

4. Access the chatbot at http://localhost:3000.


### Deployment

## Frontend Deployment on Vercel
The frontend is deployed on Vercel for seamless deployment, scalability, and speed. Visit the Vercel deployment URL to access the chatbot's user interface.

## Backend Deployment on Google Cloud Platform (GCP)
The backend is deployed on Google Cloud Platform (GCP) using Cloud Run, which handles API requests, integrates with Google Gemini and Pinecone, and ensures a reliable backend environment.

To deploy the backend on GCP:

1. Set Up Google Cloud
- Create a Google Cloud account if you haven't already.
- Install the Google Cloud SDK on your local machine.
- Initialize the SDK and authenticate
    ```bash
    gcloud init
    gcloud auth login

2. Create Dockerfile for the FastAPI backend

3. Create a .dockerignore file to exclude unnecessary files

4. Create Dockerfile for the Node.js server

5. Create a .dockerignore file for the Node.js server

6. Build and push the fast API Docker image to Google Container Registry (GCR):
    ```bash
    gcloud builds submit --tag gcr.io/[PROJECT_ID]/ai-chatbot-fastapi-backend

7. Deploy to Cloud Run
    ```bash
    gcloud run deploy ai-chatbot-fastapi-backend --image gcr.io/[PROJECT_ID]/ai-chatbot-fastapi-backend --platform managed --allow-unauthenticated

8. Note the URL provided after deployment

10. Build and push the Node.JS server Docker image to Google Container Registry (GCR):
    ```bash
    gcloud builds submit --tag gcr.io/[PROJECT_ID]/nodejs-server

11. Deploy to Cloud Run
    ```
    gcloud run deploy nodejs-server \                                            
  --image gcr.io/gen-lang-client-0128515741/nodejs-server \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars="FASTAPI_BASE_URL=[FASTAPI_URL]" \
  --region us-central1
    ```

### Usage
- Open the chat interface in your browser.
- Type your query and press "Send".
- The chatbot will display a response generated based on the context retrieved from the knowledge base.

### Technologies Used
- Python: Backend logic, API integration, and data processing.
- FastAPI: Backend framework for building the API.
- React: Frontend library for building the user interface.
- Google Gemini API: Language model API for generating responses.
- Pinecone: Vector store for storing and retrieving knowledge base documents.
- Google Cloud: Hosting and infrastructure for the AI model.

### Screenshots

![User Interface Screenshot](https://github.com/Akshaypatil9714/AI-E-Commerce-Chatbot/blob/main/images/Screenshot%202024-09-02%20at%2012.07.31.png)
![Conversations Screenshot](https://github.com/Akshaypatil9714/AI-E-Commerce-Chatbot/blob/main/images/Screenshot%202024-09-02%20at%2012.07.45.png) 
![Conversation Screenshot](https://github.com/Akshaypatil9714/AI-E-Commerce-Chatbot/blob/main/images/Screenshot%202024-09-02%20at%2012.09.25.png)