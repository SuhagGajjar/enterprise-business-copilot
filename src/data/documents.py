from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


DOCUMENT_FILES = [
    "business_strategy.txt",
    "customer_insights.txt",
    "quarterly_business_review.txt",
]


def load_documents():
    """Load NovaRetail business narrative documents."""

    documents = []

    for filename in DOCUMENT_FILES:
        file_path = RAW_DATA_DIR / filename

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        documents.append(
            {
                "filename": filename,
                "content": content,
            }
        )

    return documents

def chunk_text(text, chunk_size=500):
    """Split text into paragraph-based chunks."""

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if len(current_chunk) + len(paragraph) <= chunk_size:
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph

        else:
            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def chunk_documents(documents, chunk_size=500):
    """Create metadata-aware chunks from multiple documents."""

    all_chunks = []

    for document in documents:
        text_chunks = chunk_text(
            document["content"],
            chunk_size=chunk_size
        )

        for chunk_id, chunk in enumerate(text_chunks, start=1):
            all_chunks.append(
                {
                    "filename": document["filename"],
                    "chunk_id": chunk_id,
                    "source": f"{document['filename']}#chunk-{chunk_id}",
                    "content": chunk,
                }
            )

    return all_chunks 