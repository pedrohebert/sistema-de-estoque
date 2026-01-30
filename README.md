Projeto de estudo focado em **banco de dados**, **programação assíncrona**, **APIs web** e integração **frontend + backend**.  
O objetivo é explorar boas práticas no desenvolvimento de aplicações modernas usando Python e FastAPI.

> ⚠️ Este é um projeto educacional, não destinado a uso em produção.

---

## Objetivos do Projeto

- Praticar operações assíncronas com banco de dados
- Construir uma API REST com FastAPI
- Trabalhar com SQLModel em modo assíncrono
- Utilizar PostgreSQL em ambiente containerizado
- Integrar backend com frontend simples
- Aprender organização de projetos e arquitetura

---

## Tecnologias

- Python 3.14
- FastAPI
- SQLModel (Async)
- PostgreSQL
- Docker e Docker Compose
- HTML, CSS e JavaScript (frontend)

---

## Instalação e Execução

### Pré-requisitos

- Docker
- Docker Compose

### Passos

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```

crie um arquivo .env na raiz com base no exemplo .env.exmple substituindo os campos com valores validos 

suba os conteiner do projeto com:
```bash
docker compose up --build
```

a aplicação subira na em:
- API: localhost:8000/ 
- Documentação (Swagger): localhost:8000/docs
- Documentação (Redoc): localhost:8000/redocs

## Estrutura do Projeto
```
app/
 ├── main.py          # Ponto de entrada da aplicação
 ├── api/             # Rotas da API
 ├── models/          # Modelos do banco de dados
 ├── schemas/         # Schemas de validação
 ├── services/        # Regras de negócio
 └── db/              # Configuração do banco
```

## Aprendizados

Este projeto aborda conceitos como:
- Async / Await no Python
- Arquitetura de APIs REST
- Separação de responsabilidades
- Integração backend e frontend
- Containers e isolamento de ambiente
