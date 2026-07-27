from pinecone import Pinecone, ServerlessSpec

from config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
)

from utils import (
    extract_pdf,
    create_chunks,
    load_embedding_model,
    generate_embeddings,
)


# 1. Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# 2. Connect to Index (Index must be created manually on the Pinecone Console)
index = pc.Index(PINECONE_INDEX_NAME)

# 4. Extract PDF
pages = extract_pdf("data/Ebook-Agentic-AI.pdf")
print(f"Extracted {len(pages)} pages")

# 5. Create Chunks
chunks = create_chunks(pages)
print(f"Created {len(chunks)} chunks")

# 6. Load Embedding Model
embedding_model = load_embedding_model()
print("Embedding model loaded")

# 7. Generate Embeddings
vectors = generate_embeddings(
    chunks,
    embedding_model
)
print(f"Generated {len(vectors)} vectors")

# 8. Upload to Pinecone
index.upsert(vectors=vectors)
print("Vectors uploaded successfully!")