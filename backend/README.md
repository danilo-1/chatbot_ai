backend/
├── app/
│ ├── **init**.py # Cria a instância FastAPI no método create_app()
│ ├── core/
│ │ ├── config.py # Settings com Pydantic BaseSettings
│ │ └── logging_conf.py # Configuração de logs (Loguru ou std‑logging)
│ ├── api/
│ │ ├── **init**.py # Inclui versões + Middleware global
│ │ └── v1/
│ │ ├── **init**.py # Inclui todos os routers da versão
│ │ ├── routes_chat.py # /chat, /chat/stream, /history, /suggestion
│ │ ├── routes_agents.py # /agents
│ │ └── routes_health.py # /ping (health‑check)
│ ├── models/ # (Opcional) ORMs ou ODMs futuramente
│ ├── schemas/ # Pydantic (BaseModel) ➜ contrato de I/O
│ │ ├── message.py
│ │ ├── chat.py
│ │ └── agent.py
│ ├── services/
│ │ ├── openai_service.py # Wrapper síncrono/assíncrono OpenAI
│ │ ├── conversation_svc.py # Persistência em cache/DB
│ │ └── agent_service.py # Orquestração Runner/triage_agent()
│ ├── deps.py # Funções _Depends_ (injeção)
│ └── main.py # Ponto de entrada (uvicorn app.main:create_app())
├── tests/
│ ├── conftest.py # Fixtures (cliente FastAPI, dotenv fake)
│ ├── test_chat.py
│ └── test_agents.py
├── Dockerfile
├── docker-compose.yml # Redis / Postgres opcional
├── requirements.txt # Versões travadas via pip‑tools
├── .env.example # Variáveis obrigatórias
└── README.md
