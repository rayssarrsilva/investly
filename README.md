# Investly — Simulador Financeiro Premium  
Objetivo: entregar uma aplicação web de simulação financeira com foco em **clareza, usabilidade e interface premium**, permitindo ao usuário projetar cenários de investimento e calcular o tempo necessário para atingir metas.

---

🧩 **Problema**  
Muitos simuladores online são confusos, apresentam interfaces antiquadas e, frequentemente, utilizam dados genéricos ou não transparentes. Isso gera **desconfiança** e reduz a adoção da ferramenta.

---

💡 **Motivação**  
Construir um sistema que:  
- Oferece **transparência** (sem números falsos).  
- Tem **UI premium e responsiva**, similar a plataformas profissionais.  
- Ajuda o usuário a **planejar objetivos financeiros reais**.  
- Fornece **histórico de simulações** para acompanhamento contínuo.  

---

✅ **Solução**  
- Interface limpa, elegante e responsiva.  
- Dois simuladores principais:  
  - **Simulação de Investimentos** (crescimento futuro do capital).  
  - **Cálculo de Tempo até a Meta** (prazo necessário para atingir um valor-alvo).  
- Histórico organizado e exportável.  
- Fluxo de autenticação seguro (login, logout, cadastro).  

---

🔎 **Principais funcionalidades**  
- Registro e login de usuários.  
- Simulação de valor futuro de investimentos com base em CDI.  
- Estimativa de tempo até a meta com aportes mensais.  
- Histórico individual de simulações.  
- Exclusão de simulações ou de todo o histórico.  
- Design premium, inspirado em interfaces modernas.  

---

🧱 **Tecnologias & Decisões (por que usei)**  
- **Django + DRF** → robustez no backend, autenticação pronta e API REST para futuras expansões.  
- **SQLite** (dev) → simples e ágil no ambiente local.  
- **Templates Django + CSS custom** → controle total do design, garantindo estilo premium.  
- **Bootstrap Icons** → ícones leves e responsivos.  
- **Mensageria nativa Django** → feedback direto ao usuário.  

---

📈 **Boas práticas aplicadas**  
- Estrutura de templates reaproveitável (`base.html`).  
- Formulários estilizados com `widget_tweaks`.  
- Navegação intuitiva (Menu → Simulações → Histórico).  
- Layout responsivo (desktop e mobile).  
- Sem dados falsos → apenas cálculos baseados em entradas do usuário.  

---

🛠️ **Como rodar localmente**  
1. Clone este repositório  
   ```bash
   git clone https://github.com/seu-usuario/investly.git
   cd investly
