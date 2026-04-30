# MagnaBook AI

Plataforma inteligente para processamento, análise e geração de conteúdo para livros usando Inteligência Artificial.

## Visão Geral

MagnaBook AI automatiza e potencializa o fluxo editorial — da ingestão de manuscritos à geração de resumos, revisão de estilo, criação de índices e exportação de publicações prontas.

## Tecnologias

| Camada | Stack |
|--------|-------|
| Backend | Python 3.12, FastAPI, Celery |
| Frontend | React 18, TypeScript, Vite |
| Banco de Dados | PostgreSQL 16, Redis |
| IA | Anthropic Claude API |
| Infraestrutura | Docker, Docker Compose |

## Estrutura

```
MagnaBook AI/
├── backend/              # API FastAPI + workers Celery
│   ├── app/
│   │   ├── api/          # Rotas e endpoints
│   │   ├── services/     # Lógica de negócio
│   │   ├── models/       # Modelos ORM (SQLAlchemy)
│   │   ├── schemas/      # Schemas Pydantic
│   │   ├── core/         # Config, segurança, dependências
│   │   ├── utils/        # Utilitários compartilhados
│   │   ├── ai/           # Integrações com Claude API
│   │   └── processors/   # Processadores de documentos
│   ├── workers/          # Workers Celery
│   └── tests/            # Testes automatizados
├── frontend/             # SPA React + TypeScript
│   └── src/
│       ├── pages/        # Páginas da aplicação
│       ├── components/   # Componentes reutilizáveis
│       ├── services/     # Clientes HTTP (API calls)
│       ├── hooks/        # Custom React hooks
│       ├── store/        # Estado global (Zustand/Redux)
│       └── styles/       # CSS / Tailwind
├── storage/              # Armazenamento local
│   ├── uploads/          # Manuscritos recebidos
│   ├── exports/          # Publicações geradas
│   └── temp/             # Arquivos temporários
├── scripts/              # Scripts de automação e CI
├── docs/                 # Documentação técnica
└── docker-compose.yml    # Orquestração local
```

## Início Rápido

```bash
# 1. Clonar e configurar variáveis
cp .env.example .env
# Edite .env com suas credenciais

# 2. Subir infraestrutura
docker compose up -d

# 3. Acessar
# API:      http://localhost:8000
# Docs API: http://localhost:8000/docs
# Frontend: http://localhost:5173
```

## Execucao do Backend

Para executar somente a API em ambiente local:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints iniciais:

```text
GET /health
GET /docs
```

APIs principais:

```text
GET    /projects
POST   /projects
GET    /projects/{id}
PUT    /projects/{id}
DELETE /projects/{id}

GET    /files
POST   /files
GET    /files/{id}
PUT    /files/{id}
DELETE /files/{id}

GET    /briefing
POST   /briefing
GET    /briefing/{id}
PUT    /briefing/{id}
DELETE /briefing/{id}

GET    /prd
POST   /prd
GET    /prd/{id}
PUT    /prd/{id}
DELETE /prd/{id}

GET    /book
POST   /book
GET    /book/{id}
PUT    /book/{id}
DELETE /book/{id}

GET    /export
POST   /export
GET    /export/{id}
PUT    /export/{id}
DELETE /export/{id}
```

Exemplo de health check:

```bash
curl http://localhost:8000/health
```

## Licença

Proprietário — Raja Khalil © 2026
