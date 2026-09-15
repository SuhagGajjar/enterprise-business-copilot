import json

from src.analytics.sales import get_business_summary
from src.llm.ollama_client import generate_response
from src.llm.router import route_question
from src.rag.retriever import retrieve_chunks


def generate_combined_answer(question, summary, rag_results):
    """Generate a business answer using analytics and RAG context."""

    context = "\n\n".join(
        [
            f"Source: {result['source']}\n{result['content']}"
            for result in rag_results
        ]
    )

    prompt = f"""
You are a business analytics assistant for NovaRetail,
a fictional omnichannel consumer retailer.

Answer the user's question using ONLY the structured metrics
and business context provided below.

User question:
{question}

Structured business metrics:
{json.dumps(summary, indent=2)}

Business context:
{context}

Important:
- Use the structured metrics for relevant numerical facts.
- Use the business context for explanations and recommendations.
- When relevant, include the key metrics in the answer to support the explanation.
- Do not invent facts or numbers.
- Do not perform new calculations.
- Do not add a currency symbol unless the metrics provide one.
- Keep the answer concise and business-friendly.
"""

    return generate_response(prompt)


def answer_question(question, rag_index):
    """Route and answer a NovaRetail business question."""

    route = route_question(question)

    if route == "analytics":
        # For now, use the existing known business dimensions.
        # We will make parameter extraction more dynamic later.
        from src.llm.ollama_client import extract_business_parameters

        parameters = extract_business_parameters(question)

        summary = get_business_summary(
            quarter=parameters["quarter"],
            region=parameters["region"],
            category=parameters["category"],
        )

        return generate_response(
            f"""
You are a business analytics assistant for NovaRetail.

Answer the user's question using ONLY the structured metrics below.

User question:
{question}

Structured business metrics:
{json.dumps(summary, indent=2)}

Do not invent or recalculate numbers.
Do not add a currency symbol or currency name unless the metric explicitly provides one.
Keep the answer concise and business-friendly.
"""
        )

    if route == "rag":
        from src.llm.ollama_client import answer_knowledge_question

        return answer_knowledge_question(
            question=question,
            rag_index=rag_index,
        )

    if route == "both":
        from src.llm.ollama_client import extract_business_parameters

        parameters = extract_business_parameters(question)

        summary = get_business_summary(
            quarter=parameters["quarter"],
            region=parameters["region"],
            category=parameters["category"],
        )

        rag_results = retrieve_chunks(
            query=question,
            chunks=rag_index["chunks"],
            document_embeddings=rag_index["document_embeddings"],
            model=rag_index["model"],
            top_k=3,
        )

        return generate_combined_answer(
            question=question,
            summary=summary,
            rag_results=rag_results,
        )

    raise ValueError(f"Unsupported route: {route}")