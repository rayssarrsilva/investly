# Investly — Simulador Financeiro Premium  
Simulador financeiro para projetar rentabilidade e calcular o tempo necessário para atingir metas.

## Demo
<img width="1920" height="881" alt="investlycheck" src="https://github.com/user-attachments/assets/fc79bfe8-6d17-486f-8677-05ac4622e7a7" />

## Funcionalidades
1. Simulação de investimentos com diferentes taxas de retorno
2. Cálculo do tempo necessário para atingir metas financeiras com base na taxa de juros, porcentagem de taxa e investimento (Selic, cdi, cdb)
3. Projeção de rentabilidade ao longo dos anos
4. Cdastro/Login simples e persistente
5. Banco de dados persistente para salvar simulações

## Tech Stack
- Database: PostgreSQL
- Backend: Django + Django REST Framework (API RESTful)
- Frontend: Bootstrap
- Auth/Security: Autenticação padrão do Django, CSRF, JWT Tokens, Swaggger para documentação da API
- Testing/CI: Django Test Framework, Github Actions (pipeline de CI/CD)

  ## Setup
1. Clone o repositório
```
git clone https://github.com/rayssarrsilva/investly.git
cd investly
```
2. Instale as dependências
```
pip install -r requirements.txt
```
3. Configure as variáveis de ambiente (veja .env.example):
```
DATABASE_URL
SECRET_KEY
DEBUG
```
4. Rode localmente
```
uvicorn app.main:app --reload
```

## O que aprendi
- Migração de deploy de AWS para Render, reduzindo custos e simplificando setup.
- Decisão de usar FastAPI pela performance e facilidade de integração com frontend.
- Trade-off entre usar Docker e runtime nativo do Render (optando por Python direto).
- Aprimoramento da segurança no fluxo de autenticação com JWT.
- Desenvolvimento em Django
- Investimentos com base na Selic
- Criação e integração de PostgreSQL render no web server do render
