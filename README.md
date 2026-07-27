# 🤖 Agentic AI RAG Chatbot

An AI-powered Retrieval-Augmented Generation (RAG) chatbot that answers questions from an Agentic AI eBook using semantic search and Large Language Models.

The application extracts content from a PDF, generates embeddings, stores them in Pinecone, retrieves the most relevant chunks for a user query, and generates accurate responses using the Groq LLM.

---

## 🚀 Features

- 📄 PDF document ingestion
- ✂️ Intelligent text chunking
- 🔍 Semantic search using Pinecone
- 🧠 HuggingFace Embeddings (BAAI/bge-small-en-v1.5)
- 🤖 Groq LLM integration
- 🔄 LangGraph workflow
- 🌐 Streamlit web interface
- 📚 Source page references
- ✅ Similarity score filtering to reduce hallucinations

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- LangGraph
- Pinecone
- HuggingFace Embeddings
- Groq API
- PyPDF
- Dotenv

---

## 📂 Project Structure

```
rag-agentic-ai/
│
├── app.py                 # Streamlit UI
├── graph.py               # LangGraph workflow
├── rag.py                 # Retrieval & LLM pipeline
├── ingest.py              # PDF ingestion & Pinecone upload
├── utils.py               # PDF processing & embeddings
├── config.py              # Environment configuration
├── requirements.txt
├── .env
│
├── data/
│   └── Ebook-Agentic-AI.pdf
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <repository-url>

cd rag-agentic-ai
```

### 2. Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create `.env`

```env
PINECONE_API_KEY=YOUR_API_KEY
PINECONE_INDEX_NAME=agentic-ai-rag

GROQ_API_KEY=YOUR_API_KEY
LLM_MODEL=llama-3.1-8b-instant

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

---

## 📥 Upload PDF to Pinecone

Place your PDF inside

```
data/
```

Run

```bash
python ingest.py
```

Expected output

```
Extracted 59 pages
Created 117 chunks
Embedding model loaded
Generated 117 vectors
Vectors uploaded successfully!
```

---

## ▶️ Run the Chatbot

```bash
streamlit run app.py
```

Open

```
http://localhost:8501
```

---

## 💬 Example Questions

- What is Agentic AI?
- Explain autonomous decision making.
- What are Multi-Agent Systems?
- What is the anatomy of an Agentic AI system?
- What are practical applications of Agentic AI?

---


## 🏗️ Architecture

```
                  User Question
                        │
                        ▼
                  Streamlit UI
                        │
                        ▼
               LangGraph Workflow
                        │
                        ▼
            Generate Query Embedding
                        │
                        ▼
              Pinecone Vector Search
                        │
                        ▼
             Retrieve & Filter Chunks
               (Score Threshold >= 0.80)
                        │
                        ▼
               Build Grounded Context
                        │
                        ▼
               Groq LLM Response
                        │
                        ▼
             Final Answer + Sources
```

---

## 📌 Workflow


```
[Ingest PDF] ➔ [Split Chunks] ➔ [Embed & Upload] ➔ [Ask Question] ➔ [Query Pinecone] ➔ [Score Filter] ➔ [Run LLM] ➔ [Display Output]
```

* **Ingest PDF**: Extract raw text page-by-page from `Ebook-Agentic-AI.pdf`.
* **Split Chunks**: Break text down recursively into 1000-character segments with 200-character overlaps.
* **Embed & Upload**: Vectorize text segments using `bge-small-en-v1.5` and store them in Pinecone.
* **Ask Question**: Capture user input through the Streamlit interface.
* **Query Pinecone**: Embed the question and run a cosine similarity search on the Pinecone index.
* **Score Filter**: Retain only chunks with a similarity score of `0.80` or higher to eliminate noise.
* **Run LLM**: Format context and prompt, sending them to the Groq `llama-3.3-70b` model.
* **Display Output**: Stream the grounded response, source page numbers, and similarity confidence scores to the UI.


---

## 📷 Sample Output

```
Question:
What is Agentic AI?

Definition:
Agentic AI refers to systems capable of autonomous decision-making and action to achieve specific objectives.

Explanation:
These systems perceive, reason, and act independently to accomplish long-term goals.

Key Points
• Autonomous decision-making
• Goal-oriented behavior
• Built on intelligent software agents

Sources
Page 3
Page 18
```

---

## 📈 Future Improvements

- Conversation memory
- Multiple PDF support
- Hybrid search (Dense + BM25)
- Query rewriting
- Streaming responses
- User authentication
- Docker deployment
- Cloud deployment

---

## 👨‍💻 Author

Developed as an AI Engineer Internship Assessment Project.