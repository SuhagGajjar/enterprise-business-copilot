```mermaid
flowchart TB

    T["ENTERPRISE BUSINESS AI COPILOT<br/><b>Product Evolution</b>"]

    V1["<b>V1.0.0</b><br/>MVP<br/><br/>User Query<br/>↓<br/>LLM<br/>↓<br/>Analytics + RAG<br/>↓<br/>Answer"]

    V2["<b>V2.0.0</b><br/>Engineering Foundation<br/><br/>API<br/>↓<br/>LangGraph<br/>↓<br/>Tools<br/>↓<br/>Guardrails<br/>↓<br/>Evaluation + Logging<br/>↓<br/>Answer"]

    V3["<b>V3.0.0</b><br/>Platform Foundation<br/><br/>Multi-client Platform<br/>↓<br/>Config / Data<br/>↓<br/>Analytics + RAG + SQL<br/>↓<br/>Client Extensions"]

    V4["<b>V4.0.0</b><br/>Agentic AI<br/><br/>Agent / Planner<br/>↓<br/>Dynamic Tool Selection<br/>↓<br/>Multi-step Execution<br/>↓<br/>Validation<br/>↓<br/>Actionable Answer"]

    P1["PROVE"]
    P2["PRODUCTIONIZE"]
    P3["REUSE"]
    P4["REASON"]

    T --> V1
    T --> V2
    T --> V3
    T --> V4

    V1 -.-> P1
    V2 -.-> P2
    V3 -.-> P3
    V4 -.-> P4

    V1 ~~~ V2
    V2 ~~~ V3
    V3 ~~~ V4

    P1 ~~~ P2
    P2 ~~~ P3
    P3 ~~~ P4
```

---

```mermaid
flowchart TD
    A["V1.0.0 — ENTERPRISE BUSINESS COPILOT<br/>Proof-of-Concept MVP<br/>NovaRetail"]
    B["User Query<br/>Natural Language"]
    C["LLM<br/>Intent / Params"]
    D["Business Analytics<br/><br/>Sales<br/>Inventory<br/>Marketing<br/><br/>Deterministic calculations"]
    E["RAG<br/>Knowledge Retrieval<br/><br/>Documents<br/>→ Chunks<br/>→ Embeddings<br/>→ Similarity<br/>→ Top-K chunks"]
    F["LLM<br/>Answer synthesis"]
    G["Business Answer"]

    A --> B
    B --> C
    C --> D
    C --> E
    D --> F
    E --> F
    F --> G
```
---

```mermaid
flowchart TB

    A["V2.0.0 — PRODUCTION-ORIENTED ARCHITECTURE"]

    C["Configuration<br/><br/>LLM Model &nbsp; | &nbsp; Embedding Model &nbsp; | &nbsp; Top-K &nbsp; | &nbsp; Environment"]

    A --> C

    C --> O
    C --> R

    subgraph O["OFFLINE / INGESTION"]
        direction TB
        O1["Documents"]
        O2["Load"]
        O3["Chunk"]
        O4["Embeddings Model"]
        O5["Persistent Vector Index"]

        O1 --> O2 --> O3 --> O4 --> O5
    end

    subgraph R["RUNTIME"]
        direction TB

        R1["User Query"]
        R2["FastAPI<br/>/ask"]
        R3["LangGraph<br/>Orchestrator"]

        R1 --> R2 --> R3

        R3 --> A1["Analytics Tool"]
        R3 --> R4["RAG Retriever"]

        A1 --> V["Validation / Guardrails"]
        R4 --> V

        V --> L["LLM Response"]
        L --> U["User"]
    end

    X["Cross-cutting<br/><br/>Logging • Evaluation • Error Handling • Health Checks • Configuration"]

    X -.-> R3
    X -.-> O4
    X -.-> L``` 
```


---


```mermaid
flowchart TB

    A["V3.0.0 — REUSABLE BUSINESS AI PLATFORM"]

    B["Client / User"]
    C["API / UI"]
    D["PLATFORM CORE<br/><br/>Query Understanding<br/>Orchestration<br/>Tool Registry<br/>Guardrails<br/>Response Generation<br/>Evaluation / Observability"]

    A --> B
    B --> C
    C --> D

    D --> T1
    D --> T2
    D --> T3

    T1["Analytics<br/>Tools"]
    T2["RAG<br/>Tool"]
    T3["SQL / Data<br/>Tools"]

    T1 --> K
    T2 --> K
    T3 --> K

    K["Client Data & Knowledge<br/><br/>Structured Data<br/>Documents<br/>Business Definitions<br/>Metrics / KPIs<br/>Client-specific Tools"]

    X["CLIENT CONFIGURATION<br/><br/>Client A → terminology + models + data<br/>Client B → terminology + models + data<br/>Client C → terminology + models + data"]

    X -.-> D
    X -.-> K
```


---


```mermaid
flowchart TB

    A["V4.0.0 — AGENTIC BUSINESS AI PLATFORM"]

    B["User<br/><br/>Why did sales fall and what should we do?"]

    C["Agent / Planner<br/><br/>Understand goal<br/>Plan steps<br/>Select tools"]

    A --> B
    B --> C

    C --> T1
    C --> T2
    C --> T3

    T1["Analytics<br/>Agent"]
    T2["RAG<br/>Agent"]
    T3["SQL / Data<br/>Agent"]

    T1 --> V
    T2 --> V
    T3 --> V

    V["Evaluate /<br/>Validate"]

    V --> D{"Need another<br/>step?"}

    D -->|Yes| C
    D -->|Complete| F["Final Business<br/>Recommendation"]
