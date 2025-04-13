# Investly - Simulador de Rentabilidade de Investimentos

## 📌 Descrição

O **Investly** é um sistema para simulação e análise de investimentos. Ele calcula a rentabilidade mensal, compara diferentes investimentos e sugere o tempo ou valor necessário para atingir uma meta financeira.

Ao baixar o projeto localmente é importante entrar na pasta do projeto (investly/investhere) e rodar o código: python manage.py runserver 

## 🚀 Tecnologias Utilizadas

- **Python 3**
- **Django** (Back-end)
- **Django REST Framework (DRF)** (API RESTful)
- **PostgreSQL** (Banco de dados)

## 📂 Estrutura do Projeto

```
investly/
│── investhere/        # Código principal do projeto
│── venv/              # Ambiente virtual Python
│── requirements.txt   # Dependências do projeto
│── manage.py          # Comando para administrar o Django
│── README.md          # Documentação do projeto
```

## ⚙️ Como Executar

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/rayssarrsilva/investly.git
   cd investly
   ```

2. **Criar e ativar o ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar migrações e rodar o servidor:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. **Acessar no navegador:**
   - API: `http://127.0.0.1:8000/`

## 📄 Licença

Projeto sob licença **MIT**. Contribuições são bem-vindas! 🚀
