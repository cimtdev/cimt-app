# Arquitetura e Ops

### Atualizando a estratégia de infraestrutura para o MVP

Você optou por **DigitalOcean + EasyPanel** para hospedar **tanto o backend FastAPI quanto o n8n**, mantendo **Supabase** como banco/ Auth.

Abaixo segue um guia enxuto de como isso se encaixa no plano — com checklist de Sprint 0 / Tópico C já ajustado.

* * *

## 1\. Arquitetura em alto nível

```plain
┌──────────────┐            ┌──────────────────────────────┐
│  FlutterFlow │  HTTPS     │  FastAPI  (EasyPanel app #1) │
│  / React UI  │ ─────────► │  • /chat (SSE)               │
└──────────────┘            │  • /healthz                  │
        ▲                   └──────────────────────────────┘
        │ WebSocket/SSE
        │                   ┌──────────────────────────────┐
        │                   │  n8n  (EasyPanel app #2)     │
        └──────────────────►│  • Seed ETL cron             │
                            │  • Observabilidade / alerts  │
                            └──────────────────────────────┘
                both apps on same droplet (Docker, EasyPanel)
                            │
                            ▼
                   ┌───────────────────┐
                   │  Supabase Cloud   │
                   │  • Postgres +     │
                   │    pgvector       │
                   │  • Auth MagicLink │
                   └───────────────────┘
```

* * *

## 2\. Checklist simples — Sprint 0 / **Tópico C (Infra)** _versão DigitalOcean/EasyPanel_

| # | Tarefa | Responsável | Concluído quando… |
| ---| ---| ---| --- |
| **C1. Droplet & EasyPanel** |  |  |  |
| 1 | Criar **Droplet 2 vCPU / 2 GB** (Ubuntu 22.04) | DevOps | IP público e SSH OK |
| 2 | Instalar **EasyPanel** (\`curl -fsSL [easypanel.sh](http://easypanel.sh/) | DevOps | DevOps |
| 3 | Configurar **domínio + SSL** (Cloudflare > EasyPanel) | DevOps | Cadeia SSL verde |
| **C2. Repositórios & CI** |  |  |  |
| 4 | Criar mono-repo `cimt-mvp` (`/backend`, `/frontend`, `/ops`) | Eng. Python | Repo no GitHub |
| 5 | Adicionar **GitHub Action** que:<br>• faz build Docker<br>• publica imagem no [**ghcr.io**](http://ghcr.io/) | DevOps | Build roda em push |
| **C3. Backend (App #1) no EasyPanel** |  |  |  |
| 6 | Criar app “**api**” > fonte **Docker Image** | DevOps | Container sobe e `/healthz` ⇒ 200 |
| 7 | Definir **secrets** (`OPENAI_API_KEY`, `SUPABASE_URL`, etc.) | DevOps | Variáveis listadas no painel |
| 8 | Configurar **Deploy Hook** (webhook EasyPanel) e adicionar ao workflow GitHub | DevOps | Push na `main` redeploya |
| **C4. n8n (App #2)** |  |  |  |
| 9 | Criar app “**n8n**” > imagem `n8nio/n8n` | DevOps | URL `https://n8n.<domínio>` carrega |
| 10 | Adicionar volume `/home/node/.n8n` (EasyPanel “Persistent Storage”) | DevOps | Reinício mantém workflows |
| 11 | Criar usuário admin; salvar credenciais em 1Password | DevOps | Login testado |
| **C5. Supabase** |  |  |  |
| 12 | Projeto **cimt-dev** já criado (se não, criar) | DevOps | URL & keys salvos |
| 13 | Habilitar extensão `pgvector`; criar tabelas `users`, `chat_logs`, `vectors` | Eng. Python | Migração SQL no repo |
| **C6. Documentação** |  |  |  |
| 14 | `docs/setup.md` com passo-a-passo para: • clonar repo → `make dev` • criar app no EasyPanel • variáveis obrigatórias | Tech Lead | Arquivo revisado |
| **C7. Smoke Test** |  |  |  |
| 15 | `curl -X POST /chat` → resposta “Hello, CIMT!” | QA | Output correto |
| **Critério de Aceite** | Todos os 15 itens ✅ em ≤ 48 h; pipeline CI → deploy funciona sem passo manual. |  |  |

* * *

## 3\. Como será o **fluxo de deploy**

1. **Dev local**

```plain
# backend
make dev       # uvicorn reload
# n8n
docker compose up n8n
```

1. **Commit → GitHub Pull Request**
    *   CI executa `ruff`, `pytest`, `npm test`.
2. **Merge na** **`main`**
    *   GitHub Action:
        1. `docker build backend -t` [`ghcr.io/org/cimt-api:${{sha}`](http://ghcr.io/org/cimt-api:$%7B%7Bsha%7D)`}`
        2. `docker push ...`
        3. `curl -X POST ${{ secrets.EASYPANEL_DEPLOY_HOOK_API }}`
3. **EasyPanel** puxa a nova imagem e faz _zero-downtime restart_.

> O mesmo hook é utilizado no app _n8n_ (ou você ativa **Auto-Update** pelo próprio painel).

* * *

## 4\. Custos estimados (maio / 2025)

| Item | Plano | USD/mês\* |
| ---| ---| --- |
| Droplet 2 vCPU 2 GB | $12 | **$12** |
| Armazenamento adicional (volume 10 GB p/ n8n) | $2 | **$2** |
| Supabase **Pro 8 GB** (Postgres) | $25 | **$25** |
| **Total mensal** | — | **≈ $39** |

\* Valores sem impostos; podem variar levemente.

* * *

## 5\. Por que essa combinação é boa para o MVP?

*   **Tudo em um só lugar**: EasyPanel gerencia múltiplos containers, _logs_ e volumes na mesma dashboard — menos contexto para alternar.
*   **Reprodução local = produção**: ambos via Docker, evitando “works on my machine”.
*   **Escalar é simples**: aumenta plano do droplet ou cria segundo node e usa EasyPanel Cluster.
*   **Controle de custos**: US $ ~40/mês cobre app + n8n + banco; não há surpresas pay-per-second.

* * *

### Próximos passos

1. Crie o droplet e instale EasyPanel ainda hoje.
2. Empurre o “hello world” do backend para validar pipeline.
3. Na Sprint 1, acrescente o volume `vectors` no Supabase e gere os primeiros embeddings.

Caso precise de comandos específicos de instalação ou exemplo de workflow GitHub, é só pedir!