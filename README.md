# Monitor de IA no Piauí

Sistema de monitoramento de percepção pública sobre Inteligência Artificial no estado do Piauí, desenvolvido como projeto educacional.

## Descrição do Projeto

Este projeto coleta, analisa e visualiza notícias relacionadas à Inteligência Artificial no Piauí através de:
- **Coleta automatizada** de notícias via RSS feeds do Google Notícias  
- **Análise de sentimento** baseada em regras com palavras-chave
- **Dashboard interativo** construído com Streamlit
- **Visualizações** incluindo gráficos de pizza e nuvem de palavras

## Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd monitor-ia-piaui
```

### 2. Instale as dependências
```bash
py -m pip install -r requirements.txt
```

### 3. Execute o dashboard
```bash
py -m streamlit run dashboard.py
```

### 4. Acesse no navegador
O sistema será aberto automaticamente em: `http://localhost:8501`
```

## Como Usar

### Primeira Execução
1. Abra o dashboard no navegador
2. Clique em **"🔄 Buscar Notícias"** na barra lateral
3. Aguarde a coleta e processamento automático dos dados
4. Explore as visualizações e análises geradas

### Navegando pelo Sistema
- **Resumo**: Métricas principais na parte superior
- **Gráficos**: Visualizações interativas dos sentimentos e palavras-chave
- **Filtros**: Use os seletores para refinar os dados exibidos
- **Export**: Baixe os dados filtrados para análise externa

### Funcionalidades Disponíveis
- ** Gráfico de Sentimentos**: Visualização clara da distribuição (positivo/negativo/neutro)
- ** Nuvem de Palavras**: Destaque dos termos mais mencionados nas notícias
- ** Tabela Interativa**: Lista completa com filtros inteligentes por sentimento e termo
- ** Download**: Exportação dos dados filtrados em formato CSV compatível com Excel
- ** Interface Moderna**: Design responsivo com cores e animações suaves

## Módulos do Sistema

### `coletor_rss.py`
- Busca notícias nos feeds RSS do Google Notícias
- Termos de pesquisa: "Inteligência Artificial Piauí", "IA Piauí", "SIA Piauí"  
- Remove duplicatas automaticamente
- Limpa HTML e normaliza texto
- Exporta dados em CSV e JSON formatados

### `analise_sentimento.py`  
- Análise baseada em palavras-chave em português
- Classifica automaticamente em: positivo, negativo ou neutro
- Extrai termos mais frequentes
- Remove palavras irrelevantes (stop words)

### `dashboard.py`
- Interface web responsiva com Streamlit
- Gráficos interativos com Plotly
- Visualizações com nuvem de palavras
- Sistema de filtros e exportação de dados
- Design moderno com CSS customizado

## Limitações Conhecidas

- **Análise de Sentimento**: Baseada em regras simples, não captura sarcasmo ou contextos complexos
- **Fonte de Dados**: Dependente da disponibilidade dos feeds RSS do Google Notícias
- **Volume**: Limitado a ~15 notícias por execução para evitar sobrecarga
- **Idioma**: Otimizado para português brasileiro

## Atualizando os Dados

Para coletar notícias mais recentes:
1. No dashboard, clique em "🔄 Coletar Notícias"
2. Ou execute diretamente: `py coletor_rss.py`

## Dependências Principais

- **requests**: Requisições HTTP para APIs
- **pandas**: Manipulação e análise de dados
- **streamlit**: Framework para dashboard web  
- **plotly**: Gráficos interativos
- **wordcloud**: Geração de nuvem de palavras
- **matplotlib**: Visualizações estáticas

## Licença

Projeto desenvolvido para fins educacionais. Consulte os termos de uso das APIs utilizadas.

---s