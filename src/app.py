from src.llm.orchestrator import answer_question
from src.rag.index import create_rag_index


def main():
    """Run the NovaRetail Business Copilot."""

    print("Initializing NovaRetail Business Copilot...")

    rag_index = create_rag_index()

    print("RAG index ready.")
    print("Ask a business question or type 'exit' to quit.")

    while True:
        question = input("\nQuestion: ").strip()

        if question.lower() == "exit":
            print("Goodbye.")
            break

        if not question:
            continue

        try:
            answer = answer_question(
                question=question,
                rag_index=rag_index,
            )

            print(f"\nAnswer: {answer}")

        except Exception as error:
            print(f"\nUnable to answer the question: {error}")


if __name__ == "__main__":
    main()