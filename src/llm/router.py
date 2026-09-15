def route_question(question):
    """Determine which capabilities are required for a business question."""

    question_lower = question.lower()

    analytics_keywords = [
        "revenue",
        "sales",
        "units",
        "inventory availability",
        "stockout",
        "stockout rate",
        "marketing spend",
        "conversion rate",
        "attributed revenue",
        "underperform",
        "performance",
    ]

    rag_keywords = [
        "why",
        "reason",
        "reasons",
        "recommend",
        "recommendation",
        "recommendations",
        "strategy",
        "prioritize",
        "priority",
        "customer preference",
        "management",
    ]

    needs_analytics = any(
        keyword in question_lower
        for keyword in analytics_keywords
    )

    needs_rag = any(
        keyword in question_lower
        for keyword in rag_keywords
    )

    if needs_analytics and needs_rag:
        return "both"

    if needs_analytics:
        return "analytics"

    if needs_rag:
        return "rag"

    return "rag"