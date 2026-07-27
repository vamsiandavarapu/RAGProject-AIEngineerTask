from pinecone import Pinecone
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    GROQ_API_KEY,
    LLM_MODEL,
)

from utils import load_embedding_model

# 1. Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# 2. Load Embedding Model
embedding_model = load_embedding_model()
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=LLM_MODEL,
    temperature=0,)

# 3. Retrieve Relevant Chunks
def retrieve_chunks(query, top_k=10, score_threshold=0.65):
    """
    Retrieve the most relevant chunks from Pinecone.
    """
    query_embedding = embedding_model.embed_query(query)
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,)
    matches = [
    match
    for match in results["matches"]
    if match["score"] >= score_threshold
    ]   
    return matches


# 4. Build Context
def build_context(matches):
    """
    Convert retrieved chunks into a single context string.
    """
    context = "\n\n".join(
        match["metadata"]["text"]
        for match in matches
    )

    return context


prompt = ChatPromptTemplate.from_template("""
You are an AI assistant answering questions ONLY from the provided context.

Rules:
- Use only the provided context.
- Do not use outside knowledge.
- If the answer is not present in the context, reply:
  "I couldn't find that information in the provided document."

Keep your answers concise and easy to read:
- Definition: 2-3 sentence.
- Explanation: 4-6 sentences.
- Key Points: Maximum 5-7 bullet points.
- Keep the total answer under 300 words.
- Avoid repeating the same information.

Context:
{context}

Question:
{question}

Answer:
""")

    
    
    
def generate_from_context(question, context):
    messages = prompt.format_messages(
        context=context,
        question=question,
    )
    response = llm.invoke(messages)
    return response.content

