import os
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.fake import FakeEmbeddings
from langchain_community.vectorstores import FAISS

# -----------------------------
# 0️⃣ Initialize session state for chat history
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# 1️⃣ Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="InstantPay AI Assistant", page_icon="💬", layout="wide")

# -----------------------------
# 2️⃣ Sidebar
# -----------------------------
with st.sidebar:
    st.title("InstantPay AI Assistant ⚡")
    st.markdown("This AI assistant answers questions about **InstantPay policies, services, and careers**.")
    st.markdown("---")
    
    st.subheader("Settings")
    model_choice = st.selectbox(
        "Select Embedding Model",
        ["FakeEmbeddings (default, free)"]  # You can add OpenAI later
    )
    
    if st.button("Reset Chat History"):
        st.session_state.history = []
        st.success("Chat history cleared!")

# -----------------------------
# 3️⃣ Custom CSS for styling
# -----------------------------
st.markdown("""
    <style>
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }
    .query-box {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 10px;
    }
    .answer-box {
        background-color: #cce6ff;  /* slightly darker light blue */
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        color: #000000;  /* make text black for readability */
        font-weight: 500;
    }
    .source-box {
        font-size: 12px;
        color: #333333;  /* darker grey for sources */
    }
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-header">💬 InstantPay AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Get instant answers about policies, services, and careers!</div>', unsafe_allow_html=True)

# -----------------------------
# 2️⃣ Load Documents (Only allowed files)
# -----------------------------
DOCUMENTS_PATH = os.path.dirname(__file__)  # all text files in same folder
ALLOWED_FILES = [
    "refund_and_safety_policy.txt",
    "services_and_features.txt",
    "account_kyc_security.txt",
    "careers_and_work_with_us.txt",
    "company_overview.txt"
]

def load_documents():
    docs = []
    files = os.listdir(DOCUMENTS_PATH)
    st.write("📂 Files detected:", files)

    for file in files:
        if file in ALLOWED_FILES:
            path = os.path.join(DOCUMENTS_PATH, file)
            try:
                loader = TextLoader(path, encoding="utf-8")
                loaded = loader.load()
                for doc in loaded:
                    doc.metadata["source_file"] = file  # store source filename
                    docs.append(doc)
            except Exception as e:
                st.error(f"Error loading {file}: {e}")
    return docs

documents = load_documents()
st.success(f"{len(documents)} documents loaded successfully.")


# -----------------------------
# 5️⃣ Split documents into chunks
# -----------------------------
def simple_splitter(docs, chunk_size=500, overlap=50):
    chunks = []
    for doc in docs:
        text = doc.page_content
        start = 0
        while start < len(text):
            chunk_text = text[start:start+chunk_size]
            chunk_doc = type(doc)(page_content=chunk_text, metadata=doc.metadata.copy())
            chunks.append(chunk_doc)
            start += chunk_size - overlap
    return chunks

chunks = simple_splitter(documents)

# -----------------------------
# 6️⃣ Create embeddings and FAISS vector store
# -----------------------------
if model_choice == "FakeEmbeddings (default, free)":
    embeddings = FakeEmbeddings(size=1536)

if os.path.exists("faiss_index"):
    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
else:
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")

# -----------------------------
# 7️⃣ Function to answer queries
# -----------------------------
def answer_query(query):
    relevant_docs = vectorstore.similarity_search(query, k=3)
    
    context = "\n".join([doc.page_content for doc in relevant_docs])
    sources = ", ".join(list(set(doc.metadata.get("source_file","Unknown") for doc in relevant_docs)))
    
    answer = f"{context}"
    return answer, sources

# -----------------------------
# 8️⃣ Streamlit Chat Interface with columns
# -----------------------------
col1, col2 = st.columns([2,1])

with col1:
    query = st.text_area("💡 Type your question here:", height=100, key="query_input")
    if st.button("Get Answer"):
        if query.strip():
            with st.spinner("Fetching answer..."):
                answer, sources = answer_query(query)
                st.session_state.history.append((query, answer, sources))
                query = ""  # clear input

with col2:
    st.markdown("### Example Questions")
    st.markdown("- What is InstantPay refund policy?")
    st.markdown("- How do I apply for a job?")
    st.markdown("- Is InstantPay safe for payments?")
    st.markdown("- Tell me about InstantPay services")
    st.markdown("- What are InstantPay's career opportunities?")

# -----------------------------
# 9️⃣ Display chat history
# -----------------------------
for q, a, sources in reversed(st.session_state.history):
    with st.expander(f"💬 {q}", expanded=True):
        st.markdown(f'<div class="answer-box">{a}</div>', unsafe_allow_html=True)
        st.markdown("**Source file(s):**")
        for src in sources.split(", "):
            st.markdown(f'<div class="source-box">🗂️ {src}</div>', unsafe_allow_html=True)

# -----------------------------
# 🔟 Footer
# -----------------------------
st.markdown("""
    <hr>
    <p style='text-align:center; color:#888; font-size:12px'>
    Powered by Streamlit + FAISS • InstantPay AI Assistant Demo
    </p>
""", unsafe_allow_html=True)
