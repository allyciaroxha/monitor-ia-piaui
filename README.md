Monitor de IA no Piauí

Sistema de monitoramento de percepção pública sobre Inteligência Artificial no estado do Piauí, desenvolvido como projeto educacional.

Descrição do Projeto

Este projeto coleta, analisa e visualiza notícias relacionadas à Inteligência Artificial no Piauí através de:
- **Coleta automatizada** de notícias via RSS feeds do Google Notícias  
- **Análise de sentimento** baseada em regras com palavras-chave
- **Dashboard interativo** construído com Streamlit
- **Visualizações** incluindo gráficos de pizza e nuvem de palavras

Como Executar

Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd monitor-ia-piaui
```

2. Instale as dependências
```bash
py -m pip install -r requirements.txt
```

3. Execute o dashboard
```bash
py -m streamlit run dashboard.py
```

4. Acesse no navegador
O sistema será aberto automaticamente em: `http://localhost:8501`
