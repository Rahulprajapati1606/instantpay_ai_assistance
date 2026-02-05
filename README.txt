InstantPay AI Assistant

AI-Powered Customer Support Assistant for InstantPay

This project is a mini knowledge-base assistant that indexes internal documents and answers user queries with grounded, source-backed responses. Built using Streamlit, FAISS, and LangChain Community, the app provides a simple UI to ask questions about InstantPay’s services, policies, and careers.

Demo / Live URL
[https://instantpayaiassistance-ezagum8vbepmypo2qhiwob.streamlit.app]

Project Structure

instantpay_ai_assistance/
myapp.py - Main Streamlit application
requirements.txt - Python dependencies
faiss_index/ - FAISS vector store for document embeddings
documents/ - Text documents for knowledge base
company_overview.txt
refund_and_safety_policy.txt
services_and_features.txt
account_kyc_security.txt
careers_and_work_with_us.txt
README.md - Project documentation

Technical Overview

1.Document Ingestion

Each document is in the instantpay_ai_assistant folder and in code each file's name has been specified so that assistant will load only required files.

2.Document Chunking

Large documents are split into smaller chunks (500 characters with 50-character overlap).

This allows better similarity search performance.

3.Embeddings & Vector Store

Uses FakeEmbeddings (free, no API key required) to generate vector representations.

FAISS vector store is used for fast similarity search.

FAISS index is persisted locally to avoid rebuilding on each run.

4.Query & Retrieval

User queries are matched to top 3 relevant document chunks using vector similarity.

Responses combine retrieved text and include source filenames for reference.

5.UI & Interaction

Streamlit UI with:
Sidebar for guidance and examples
Text input for user queries
Answer box with context and sources

Styled for readability and engagement.

6.Usage

Clone the repository:

git clone https://github.com/Rahulprajapati1606/instantpay_ai_assistance.git

Create a virtual environment:

python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on Mac/Linux)

Install dependencies:

pip install -r requirements.txt

Run the app:

streamlit run myapp.py

Ask questions about InstantPay policies, services, or careers.

No OpenAI API key is required because the app uses FakeEmbeddings.

Optionally, an API key can be added for OpenAI embeddings if you upgrade the app.

Key Design Decisions

Streamlit chosen for quick, interactive UI and easy deployment.

FAISS + FakeEmbeddings used to avoid API key issues and simplify local testing.

Real Api Key is paid ad uses credits and therefore to show that it is working model FakeEmbeddings were used which finds the answer 
but because no thinking process it cannot mold the answers into logical form.

Document chunking ensures relevant sections are retrieved efficiently.

Source citation included in responses to provide credibility.

App structure is modular and easily extendable for future LLM integration.

7.Limitations & Future Improvements

Currently uses FakeEmbeddings – responses are based on simple similarity, not semantic understanding.

Could integrate OpenAI or other LLMs for smarter AI-generated answers.

Deployment can include authentication for internal use.

Could add file upload to allow dynamic document ingestion.

Contact / Collaboration

GitHub username: [Rahulprajapati1606]


Collaborator access granted to: 7A7cell
