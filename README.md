# Orders service exercise

## High level system architecture
B2B AI-only support chatbot. Run on VPS. 
Blue nodes - are app's components. Orange - external systems

```mermaid
flowchart LR
    User(("👤<br/>Customer")) --> Authentication["Auth service<br/><span style='font-size:11px'>Authenticates requests and forwards trusted user context</span>"]
    Authentication --> Agent["AI agent service<br/><span style='font-size:11px'>Answers customer questions and calls tools</span>"]
    Agent --> Identity["Identity service<br/><span style='font-size:11px'>Maps authenticated user to customer company</span>"]
    Agent --> Knowledge["Knowledge service<br/><span style='font-size:11px'>Searches shared FAQs and policies in Confluence</span>"]
    Agent -->|Trusted customer context| Tickets["Tickets service<br/><span style='font-size:11px'>Creates complaint tickets and retrieves customer tickets</span>"]
    Agent -->|Trusted customer context| OrdersAPI
    Agent --> OpenAI[OpenAI Responses API]
    Identity --> Directory[Internal customer API]
    Knowledge --> Confluence[Confluence API]
    Tickets --> Jira[Jira API]
    subgraph Orders[Orders service]
        OrdersAPI["Order lookup API<br/><span style='font-size:11px'>Returns customer orders from local database</span>"]
        Consumer["Kafka consumer<br/><span style='font-size:11px'>Updates local order records from Kafka events</span>"]
    end
    OrdersAPI --> DB[(PostgreSQL)]
    Consumer --> DB
    Upstream[Order system] --> Kafka[Kafka broker]
    Kafka --> Consumer
    classDef application fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef external fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef infrastructure fill:#e5e7eb,stroke:#6b7280,color:#111827
    class Agent,Identity,Knowledge,Tickets,OrdersAPI,Consumer application
    class Authentication,User,OpenAI,Directory,Confluence,Jira,Upstream external
    class DB,Kafka infrastructure
```

## What do you need to do

You need to implement Orders service lookup API from the diagram above. This repo serves as a template:
- it has defined but not implemented API endpoints in `app/api.py`
- db models are not defined (`app/models.py`)
- incoming data examples you can find in `app/consumer.py`
- db session is configured for the app and tests

Focus on implementing:
- `app/api.py`
- `app/models.py`
- and anything else you think is relevant

## Setup and tests
Install uv. It installs Python 3.15 if needed.

```sh
uv sync --locked
uv run pytest -q
```
