from src.rag.retriever import retrieve_chunks
from src.rag.index import create_rag_index
from src.data.documents import load_documents, chunk_documents
from src.rag.embeddings import load_embedding_model
from src.rag.retriever import build_index, retrieve_chunks
from src.analytics.sales import get_business_summary
import json
import ollama


MODEL_NAME = "qwen3:4b"


def generate_response(prompt):
    """Generate a response using the local Qwen3 model."""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]
    
def extract_business_parameters(question):
    """Extract structured business parameters from a natural-language question."""

    prompt = f"""
Extract the business parameters from the following question.

Question:
{question}

Return ONLY valid JSON with exactly these fields:
{{
    "quarter": "...",
    "region": "...",
    "category": "..."
}}

Valid quarters: Q1, Q2, Q3, Q4
Valid regions: North, South, East, West
Valid categories: Electronics, Fashion & Lifestyle

Do not calculate or invent any business metrics.
"""

    response = generate_response(prompt)

    return json.loads(response)

def answer_business_question(question):
    """Answer a business question using LLM extraction, analytics, and LLM explanation."""

    parameters = extract_business_parameters(question)

    summary = get_business_summary(
        quarter=parameters["quarter"],
        region=parameters["region"],
        category=parameters["category"],
    )

    return generate_business_answer(
        question=question,
        summary=summary,
    )
    
def generate_business_answer(question, summary):
    """Generate a business-friendly answer grounded in deterministic analytics."""

    prompt = f"""
You are a business analytics assistant for NovaRetail, a fictional omnichannel retail company.

Answer the user's question using ONLY the metrics provided below.

User question:
{question}

Business metrics:
{json.dumps(summary, indent=2)}

Important:
- Monetary values are provided in the metrics.
- Preserve the currency and values provided.
- Do not invent or recalculate any numbers.
- Keep the answer concise and business-friendly.
"""

    return generate_response(prompt)
    

def answer_knowledge_question(question, rag_index, top_k=3):
    """Answer a business knowledge question using RAG and the local LLM."""

    results = retrieve_chunks(
        query=question,
        chunks=rag_index["chunks"],
        document_embeddings=rag_index["document_embeddings"],
        model=rag_index["model"],
        top_k=top_k,
    )

    context = "\n\n".join(
        [
            f"Source: {result['source']}\n{result['content']}"
            for result in results
        ]
    )

    prompt = f"""
You are a business analytics assistant for NovaRetail,
a fictional omnichannel consumer retailer.

Answer the user's question using ONLY the business context provided below.

User question:
{question}

Business context:
{context}

Important:
- Do not invent facts.
- Do not introduce information that is not supported by the business context.
- Keep the answer concise and business-friendly.
"""

    return generate_response(prompt)