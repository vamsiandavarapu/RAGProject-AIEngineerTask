from pathlib import Path
import fitz
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def extract_pdf(pdf_path: str):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    document = fitz.open(pdf_path)
    extracted_pages = []
    for page_number, page in enumerate(document, start=1):
        text = page.get_text().strip()
        if text:
            extracted_pages.append(
                {
                    "page": page_number,
                    "source": pdf_path.name,
                    "text": text,
                }
            )
    document.close()
    return extracted_pages


def create_chunks(extracted_pages):
    """Split extracted pages into smaller chunks while preserving metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = []
    chunk_id = 1

    for page in extracted_pages:
        split_texts = splitter.split_text(page["text"])
        for text in split_texts:
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "page": page["page"],
                    "source": page["source"],
                    "text": text,
                }
            )
            chunk_id += 1
    return chunks


def load_embedding_model():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    return embeddings



def generate_embeddings(chunks, embedding_model):
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_model.embed_documents(texts)
    vectors = []
    for chunk, embedding in zip(chunks, embeddings):
        vectors.append(
            {
                "id": f"chunk_{chunk['chunk_id']}",
                "values": embedding,
                "metadata": {
                    "page": chunk["page"],
                    "source": chunk["source"],
                    "text": chunk["text"],
                },
            }
        )

    return vectors