# Enterprise Business Copilot

An enterprise-oriented GenAI business copilot that combines **structured business analytics, Retrieval-Augmented Generation (RAG), deterministic question routing, and a local Large Language Model (LLM)** to answer business questions and provide concise, context-aware insights.

The project demonstrates how an AI copilot can combine **exact numerical analysis from structured data** with **qualitative business knowledge from enterprise documents** rather than relying on an LLM alone.

---

## 1. Project Overview

Enterprise users often need answers that require multiple types of business knowledge.

For example:

* "What was Q4 revenue for South Electronics?"
* "Why did Fashion & Lifestyle underperform in East?"
* "Why did East Fashion & Lifestyle underperform in Q4, and what should management prioritize?"

These questions may require:

* Exact calculations from structured datasets
* Business context from reports and strategy documents
* Retrieval of relevant information
* Reasoning across multiple information sources
* A concise business-oriented response

A pure LLM approach is not appropriate for this use case because the model should not be responsible for calculating business metrics that can be deterministically derived from source data.

This MVP therefore separates responsibilities:

**Python performs deterministic analytics.**

**RAG retrieves relevant business context.**

**The LLM interprets and communicates the result.**

---

## 2. Business Scenario — NovaRetail

NovaRetail is a **fictional omnichannel consumer retailer** created for this project.

The synthetic business environment contains:

* Four regions: North, South, East, West
* Physical Store and E-commerce channels
* Sales
* Inventory
* Marketing
* Customer Insights
* Supply Chain
* Business Strategy

The project intentionally uses synthetic data so that the architecture can be demonstrated without exposing confidential enterprise information.

The MVP uses USD as its reporting currency assumption. In a production implementation, currency would be configurable based on the client, tenant, or business geography.

---

## 3. Business Problem

A traditional business reporting workflow may require users to:

1. Find the relevant dataset.
2. Filter the correct business dimensions.
3. Calculate metrics.
4. Locate relevant reports.
5. Interpret the business context.
6. Formulate an executive-level conclusion.

The copilot brings these activities together through a single natural-language interface.

### Example

A user asks:

> Why did East Fashion & Lifestyle underperform in Q4, and what should management prioritize?

The system combines:

**Structured analytics**

* Revenue
* Inventory availability
* Stockout rate
* Marketing spend
* Conversion rate
* Attributed revenue

with:

**Business context**

* Customer preferences
* Product-level observations
* Marketing performance
* Management priorities
* Strategic recommendations

The LLM then produces a concise business answer.

---

# 4. High-Level Architecture

```text
                         USER
                           │
                           ▼
                  Natural Language
                     Question
                           │
                           ▼
                    Question Router
                    /      |       \
                   /       |        \
                  ▼        ▼         ▼
            Analytics      RAG       Both
            Path           Path      Paths
               │            │          │
               ▼            ▼          ▼
        Structured Data   Business   Structured +
        & Python          Documents  Business Context
        Analytics         Retrieval
               │            │          │
               └────────────┴──────────┘
                            │
                            ▼
                         Qwen3
                         (LLM)
                            │
                            ▼
                  Business-Oriented Answer
```

The architecture deliberately separates **calculation, retrieval, and language generation**.

---

# 5. Core Design Principle

The project follows a core enterprise AI design principle:

> **Use deterministic systems for tasks that require exactness, and use the LLM for language understanding, contextual reasoning, synthesis, and communication.**

The LLM is therefore **not treated as the source of truth for numerical calculations**.

Instead, the system separates responsibilities based on the type of information being handled.

```text
                    User Question
                         │
                         ▼
               Question Understanding
                  /              \
                 /                \
                ▼                  ▼
       Structured Data      Business Documents
              │                    │
              ▼                    ▼
       Python Analytics            RAG
              │                    │
              ▼                    ▼
         Exact Metrics       Relevant Context
                 \                /
                  \              /
                   └──────┬─────┘
                          ▼
                         LLM
                          │
                          ▼
                Executive Answer
```

## Why this separation matters

Structured business data such as sales, inventory, marketing spend, conversion rates, and revenue should be handled using deterministic analytics logic.

For example:

```text
Sales Data
   ↓
Filter: Q4 + South + Electronics
   ↓
Python aggregation
   ↓
Revenue = 43,708,184
```

The calculation is performed by Python rather than asking the LLM to derive the result.

This provides:

* deterministic calculations
* repeatable results
* easier validation
* clearer debugging
* reduced hallucination risk
* better auditability

The LLM can then convert the verified result into a natural business response.

```text
User Question
   ↓
Understand requested business parameters
   ↓
{
  "quarter": "Q4",
  "region": "South",
  "category": "Electronics"
}
   ↓
Python Analytics
   ↓
43,708,184
   ↓
LLM
   ↓
"Q4 revenue for South Electronics was approximately $43.7M."
```

In this architecture, the LLM understands **what the user is asking**, while deterministic analytics determines **what the correct numerical answer is**.

## Role of RAG

Some business questions cannot be answered from numerical data alone.

Questions such as:

```text
Why did East Fashion & Lifestyle underperform in Q4?
```

require business context from documents such as:

* business strategy
* customer insights
* quarterly business reviews
* management observations

For these questions, the system retrieves the most relevant document chunks using semantic search.

```text
User Question
      ↓
Embedding
      ↓
Similarity Search
      ↓
Relevant Business Context
      ↓
LLM
      ↓
Business Explanation
```

The LLM therefore reasons over **retrieved business evidence**, rather than relying only on its pretrained knowledge.

## Combining Analytics and RAG

The most valuable business questions often require both quantitative and qualitative information.

For example:

```text
Why did East Fashion & Lifestyle underperform in Q4,
and what should management prioritize?
```

The system can use both paths:

```text
                         User Question
                              │
                              ▼
                         Question Router
                        /       |       \
                       /        |        \
                      ▼         ▼         ▼
               Analytics      RAG     Analytics + RAG
                      │         │          │
                      │         │      ┌───┴─────────┐
                      │         │      │             │
                      ▼         ▼      ▼             ▼
                 Exact Metrics Context          Exact Metrics
                                           + Retrieved Context
                      │         │              │
                      └─────────┴──────┬───────┘
                                      ▼
                                     LLM
                                      │
                                      ▼
                             Executive Answer
```

This allows the final response to combine:

```text
Deterministic facts
        +
Retrieved business context
        +
LLM synthesis
        =
Grounded business answer
```

For example, Python may establish that:

```text
Inventory availability: 51.48%
Stockout rate:           48.52%
Conversion rate:          1.60%
```

while RAG retrieves business context describing:

```text
Changing customer preferences
Weaker promotional engagement
Product-level demand weakness
Management priorities
```

The LLM then combines these inputs into a concise executive explanation.

## Responsibility Boundaries

The architecture deliberately assigns different responsibilities to different components.

### Python / Deterministic Systems

Used for:

* filtering structured data
* aggregations
* calculations
* KPI generation
* validation
* business rules
* exact numerical outputs

### RAG

Used for:

* retrieving relevant business knowledge
* strategy documents
* customer insights
* management commentary
* qualitative explanations
* contextual evidence

### LLM

Used for:

* understanding natural-language questions
* extracting business parameters
* interpreting retrieved context
* combining structured and unstructured information
* summarization
* reasoning over supplied evidence
* producing business-friendly responses

This separation is important because an LLM is probabilistic, while many enterprise calculations require deterministic and reproducible results.

The design therefore follows the principle:

```text
LLM for understanding and synthesis
            +
Deterministic tools for facts and calculations
            +
RAG for enterprise knowledge
            =
Reliable AI-assisted business decision support
```

This architecture also makes the solution easier to evolve into a production system because individual components—analytics functions, retrieval, routing, models, validation, and user interfaces—can be improved independently without redesigning the entire application.

# 6. Structured Analytics Architecture

Structured business questions are handled using deterministic Python analytics.

```text
User Question
      │
      ▼
LLM Parameter Extraction
      │
      ▼
Structured Parameters
      │
      ├── Quarter
      ├── Region
      └── Category
      │
      ▼
Python Analytics Function
      │
      ▼
Filtered Business Data
      │
      ▼
Exact Metric Calculation
      │
      ▼
Structured Result
      │
      ▼
LLM
      │
      ▼
Business-Friendly Answer
```

For example:

```text
"What was Q4 revenue for South Electronics?"
```

is converted into:

```json
{
  "quarter": "Q4",
  "region": "South",
  "category": "Electronics"
}
```

Python then calculates the revenue directly from the sales dataset.

This prevents the LLM from having to perform the underlying business calculation.

---

# 7. RAG Architecture

Business documents contain qualitative information that is not naturally represented as structured metrics.

The RAG pipeline handles this information.

```text
Business Documents
       │
       ▼
Document Loading
       │
       ▼
Paragraph-Aware Chunking
       │
       ▼
Metadata Assignment
       │
       ▼
Local Embedding Model
       │
       ▼
Document Embeddings
       │
       ▼
In-Memory Index
       │
       ▼
Semantic Similarity Search
       │
       ▼
Top-K Relevant Chunks
       │
       ▼
LLM
       │
       ▼
Grounded Business Answer
```

---

# 8. Document Chunking

The initial implementation considered simple character-based chunking.

The MVP uses **paragraph-aware chunking** instead.

The objective is to preserve meaningful business statements rather than arbitrarily splitting text in the middle of a concept.

Each chunk also retains metadata:

```text
filename
chunk_id
source
content
```

For example:

```text
business_strategy.txt#chunk-1
```

This provides traceability and makes retrieval results easier to inspect and debug.

---

# 9. Embeddings and Retrieval

The project uses:

**Embedding model:** `all-MiniLM-L6-v2`

The model runs locally and produces **384-dimensional embeddings**.

The retrieval process is:

```text
User Question
      │
      ▼
Question Embedding
      │
      ▼
Cosine Similarity
      │
      ▼
Rank Document Chunks
      │
      ▼
Top-K Results
```

The MVP currently uses `top_k=3`.

The embeddings and metadata are held in memory during the application process.

---

# 10. In-Memory RAG Lifecycle

The application initializes the RAG index once when it starts.

```text
Application Starts
        │
        ▼
create_rag_index()
        │
        ├── Load documents
        ├── Create chunks
        ├── Load embedding model
        └── Build embedding index
        │
        ▼
RAG Index Held in Memory
        │
        ├── Question 1
        ├── Question 2
        ├── Question 3
        └── ...
```

This avoids repeatedly loading the embedding model for every question during the same application session.

The current implementation intentionally does **not** persist the vector index across application restarts.

A persistent vector store is a future enhancement.

---

# 11. Analytics + RAG Architecture

The most important capability demonstrated by the MVP is the ability to combine structured analytics and qualitative business knowledge.

```text
                    USER QUESTION
                         │
                         ▼
                   Question Router
                         │
                         ▼
                    Analytics + RAG
                    /            \
                   /              \
                  ▼                ▼
        Python Analytics       Semantic Retrieval
                  │                │
                  ▼                ▼
          Exact Metrics       Relevant Context
                  │                │
                  └───────┬────────┘
                          ▼
                         Qwen3
                          │
                          ▼
                 Executive Answer
```

For example:

> Why did East Fashion & Lifestyle underperform in Q4, and what should management prioritize?

The system can combine:

* Stockout rate: 48.52%
* Conversion rate: 1.595%
* Product-level observations
* Customer preference changes
* Promotional engagement
* Management recommendations

The LLM's responsibility is to synthesize these inputs into a concise business explanation.

---

# 12. Question Routing

The MVP uses deterministic keyword-based routing.

```text
                         USER
                           │
                           ▼
                  Business Question
                           │
                           ▼
                    Simple Router
                     /     |      \
                    /      |       \
                   ▼       ▼        ▼
              Analytics   RAG      Both
                   │       │        │
                   ▼       ▼        ▼
             Exact Data  Context  Data + Context
                   │       │        │
                   └───────┴────────┘
                           │
                           ▼
                          LLM
                           │
                           ▼
                   Business Answer
```

Examples:

| Question                                                                               | Route     |
| -------------------------------------------------------------------------------------- | --------- |
| "What was Q4 revenue for South Electronics?"                                           | Analytics |
| "Why did Fashion & Lifestyle underperform in East?"                                    | Both      |
| "What should management prioritize?"                                                   | RAG       |
| "Why did East Fashion & Lifestyle underperform and what should management prioritize?" | Both      |

The routing approach is deliberately simple for the MVP because it is:

* Predictable
* Easy to test
* Low cost
* Fast
* Easy to understand and debug

A production system could use dynamic intent classification, tool calling, or an agentic orchestration layer.

---

# 13. LLM Responsibility

The LLM is used for:

* Natural-language parameter extraction
* Business-context interpretation
* Combining structured metrics and retrieved context
* Producing concise business-oriented responses

The LLM is deliberately not responsible for:

* Directly querying arbitrary databases
* Performing trusted financial calculations
* Acting as the authoritative source of business metrics
* Inventing unsupported facts

This separation improves reliability and makes the system easier to reason about.

---

# 14. Local LLM Architecture

The MVP uses:

**Ollama + Qwen3 4B**

The model runs locally.

```text
Python Application
       │
       ▼
Ollama Python Client
       │
       ▼
Local Ollama Runtime
       │
       ▼
Qwen3 4B
       │
       ▼
Generated Response
```

A local model was selected for the MVP because it:

* Avoids API costs
* Allows the project to run without external LLM credentials
* Keeps business data local
* Demonstrates the application architecture independently of a specific cloud LLM provider

A production deployment could replace the local model with a managed enterprise LLM without fundamentally changing the surrounding analytics/RAG architecture.

---

# 15. Grounding and Hallucination Control

The project follows a basic grounding strategy.

For analytics questions:

```text
LLM
 ↓
Parameters
 ↓
Python
 ↓
Exact Metrics
```

For knowledge questions:

```text
Question
 ↓
RAG Retrieval
 ↓
Relevant Business Context
 ↓
LLM
```

For combined questions:

```text
Exact Metrics + Retrieved Context
              ↓
             LLM
              ↓
       Business Answer
```

The LLM prompts explicitly instruct the model not to invent facts or numbers.

---

# 16. Out-of-Scope Question Behavior

The MVP does not yet contain a dedicated out-of-domain classifier.

Instead, unsupported questions currently fall through to the RAG path.

For example:

> What is the current share price of Apple?

The business context contains no information about Apple stock prices.

The grounded RAG prompt therefore causes the model to state that the information is unavailable rather than inventing a stock price.

This provides a basic anti-hallucination behavior.

### Current limitation

This is not equivalent to explicit scope detection.

A production system should distinguish:

```text
Question
   │
   ▼
Intent / Scope Detection
   ├── Analytics
   ├── RAG
   ├── Analytics + RAG
   └── Unsupported / Out of Scope
```

---

# 17. Data Architecture

The project contains both structured and unstructured business information.

```text
                    NovaRetail Data
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
      Structured Data            Business Documents
             │                         │
             ▼                         ▼
      Pandas / Python                 RAG
             │                         │
             ▼                         ▼
       Exact Metrics             Business Context
             │                         │
             └────────────┬────────────┘
                          ▼
                         LLM
```

Structured datasets include:

* `sales.csv`
* `inventory.csv`
* `marketing.csv`
* `products.csv`
* `customer_segments.csv`

Business documents include:

* `business_strategy.txt`
* `customer_insights.txt`
* `quarterly_business_review.txt`

---

# 18. Data Validation

Synthetic data is validated before being used by the application.

Validation includes:

* Required datasets exist
* Expected columns exist
* Missing-value checks
* Product master consistency
* Sales/product consistency
* Inventory/product consistency
* Revenue calculation consistency
* Quarterly coverage
* Business dimension consistency

For example:

```text
revenue = units_sold × avg_selling_price
```

is validated programmatically.

This reduces the risk of demonstrating an AI system using internally inconsistent sample data.

---

# 19. Important Design Lesson — Aggregation Scope

During development, an aggregation-scope issue was identified.

For example:

```text
South region revenue
```

is not the same metric as:

```text
South + Electronics revenue
```

The deterministic analytics layer made this distinction explicit.

This illustrates an important principle for enterprise AI:

> The LLM should not be trusted to infer the intended aggregation scope when deterministic business logic can define it explicitly.

---

# 20. Error Handling

The analytics layer validates:

* Quarter
* Region
* Category
* Availability of matching data

Invalid parameters result in explicit errors rather than silently returning misleading results.

The application entry point catches runtime exceptions and reports that the question could not be answered.

---

# 21. Current Technology Stack

| Component           | Technology                  |
| ------------------- | --------------------------- |
| Language            | Python 3.11                 |
| Data Processing     | Pandas                      |
| Numerical Computing | NumPy                       |
| Embeddings          | Sentence Transformers       |
| Embedding Model     | all-MiniLM-L6-v2            |
| Vector Search       | In-memory cosine similarity |
| LLM Runtime         | Ollama                      |
| LLM                 | Qwen3 4B                    |
| Structured Data     | CSV                         |
| Business Documents  | TXT                         |
| Application         | Python CLI                  |

---

# 22. Project Structure

```text
enterprise-business-copilot/
│
├── data/
│   └── raw/
│       ├── business_strategy.txt
│       ├── customer_insights.txt
│       ├── customer_segments.csv
│       ├── inventory.csv
│       ├── marketing.csv
│       ├── products.csv
│       ├── quarterly_business_review.txt
│       └── sales.csv
│
├── scripts/
│   ├── generate_data.py
│   ├── inspect_data.py
│   └── validate_data.py
│
├── src/
│   ├── analytics/
│   │   └── sales.py
│   │
│   ├── data/
│   │   ├── documents.py
│   │   └── loader.py
│   │
│   ├── llm/
│   │   ├── ollama_client.py
│   │   ├── orchestrator.py
│   │   └── router.py
│   │
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── index.py
│   │   └── retriever.py
│   │
│   └── app.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 23. How to Run

## Prerequisites

Install:

* Python 3.11+
* Ollama
* Qwen3 4B

Pull the model:

```bash
ollama pull qwen3:4b
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m src.app
```

The application initializes the RAG index and then accepts business questions interactively.

---

# 24. Example Questions

### Analytics

```text
What was Q4 revenue for South Electronics?
```

### RAG

```text
Why did Fashion & Lifestyle underperform in East in Q4?
```

### Analytics + RAG

```text
Why did East Fashion & Lifestyle underperform in Q4,
and what should management prioritize?
```

### Unsupported / external question

```text
What is the current share price of Apple?
```

The system should not invent information that is not present in the available business context.

---

# 25. Current MVP Limitations

The project is intentionally an MVP.

Current limitations include:

1. Keyword-based routing rather than dynamic intent classification.
2. No persistent vector database.
3. RAG index is rebuilt when the application restarts.
4. Simple JSON parsing for LLM-generated parameters.
5. No formal automated evaluation framework.
6. No dedicated out-of-domain classifier.
7. No production authentication or authorization.
8. No multi-tenant configuration.
9. No production monitoring/observability.
10. CLI interface rather than a production UI.
11. Local LLM runtime rather than enterprise model serving.

These limitations are deliberate opportunities for future development rather than hidden shortcomings.

---

# 26. Production Evolution

The MVP architecture can evolve toward a production enterprise architecture.

```text
                    MVP
                     │
                     ▼
              Working Prototype
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
 Dynamic Routing  Vector Store  Evaluation
        │            │            │
        ▼            ▼            ▼
 Tool Calling    Persistent RAG  Quality Metrics
        │
        ▼
 Guardrails / Scope Detection
        │
        ▼
 Enterprise LLM / Model Gateway
        │
        ▼
 API + Authentication
        │
        ▼
 Web Application
        │
        ▼
 Monitoring / Observability
```

Potential future enhancements include:

* Persistent vector store such as FAISS or Chroma
* Dynamic intent classification
* Tool calling
* Explicit out-of-domain detection
* Structured output validation
* Pydantic-based schemas
* Retrieval evaluation
* Automated answer evaluation
* Source citations in responses
* Guardrail framework
* Dockerized deployment
* API layer
* Lightweight web UI
* Enterprise authentication and authorization
* Monitoring and observability

---

# 27. MVP vs Production Thinking

The project intentionally separates **proof-of-concept decisions** from **production requirements**.

| Area            | MVP               | Production Direction           |
| --------------- | ----------------- | ------------------------------ |
| Routing         | Keyword-based     | Dynamic intent/tool routing    |
| Vector storage  | In-memory         | Persistent vector database     |
| LLM             | Local Qwen3       | Enterprise LLM/model gateway   |
| Scope detection | Grounded fallback | Explicit classifier/guardrail  |
| Validation      | Basic             | Schema + automated validation  |
| Evaluation      | Manual testing    | Formal evaluation framework    |
| UI              | CLI               | Web application                |
| Deployment      | Local             | Containerized/cloud deployment |
| Currency        | USD assumption    | Configurable by client/tenant  |
| Security        | Local             | Authentication/authorization   |
| Monitoring      | None              | Production observability       |

---

# 28. Design Philosophy

The project is based on several principles:

### 1. Deterministic where possible

If Python can calculate a metric exactly, the LLM should not calculate it.

### 2. Retrieval for enterprise knowledge

If information exists in business documents, retrieve it instead of expecting the LLM to memorize it.

### 3. LLM for interpretation

The LLM adds value by understanding natural language and communicating insights clearly.

### 4. Explicit separation of responsibilities

Analytics, retrieval, routing, orchestration, and generation should remain understandable and independently testable.

### 5. MVP first, production evolution second

The goal is to validate the architecture before adding infrastructure complexity.

---

# 29. Portfolio Objective

This project demonstrates practical understanding of how GenAI can be incorporated into an enterprise business product.

The emphasis is not on building a generic chatbot.

The emphasis is on combining:

* Business problem understanding
* Structured analytics
* RAG
* LLM orchestration
* Product-oriented routing
* Grounding
* Business-context interpretation
* Architecture and trade-off decisions

The project is intentionally designed as an extensible MVP that can evolve toward a production enterprise copilot.

---

# 30. License / Usage

This project uses fictional business data created specifically for demonstration and learning purposes.

No confidential enterprise data is included.
