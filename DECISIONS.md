# Decisões de Desenvolvimento - Monitor de IA no Piauí

## Visão Geral do Projeto

Este documento registra as principais decisões técnicas e estratégicas tomadas durante o desenvolvimento do sistema de monitoramento de percepção pública sobre Inteligência Artificial no estado do Piauí.

## Arquitetura Escolhida

### Modularização em 3 Componentes

**Decisão:** Separar o sistema em três módulos independentes: coleta, análise e visualização.

**Justificativa:**
- **Manutenibilidade:** Cada módulo pode ser modificado independentemente
- **Testabilidade:** Permite testes isolados de cada funcionalidade
- **Escalabilidade:** Facilita futuras expansões ou substituições de componentes
- **Clareza:** Código mais organizado e fácil de entender

## Fonte de Dados

### Google News RSS Feeds

**Decisão:** Utilizar feeds RSS do Google Notícias como fonte primária de dados.

**Justificativa:**
- **Gratuito:** Sem custos de API
- **Abrangente:** Cobre múltiplas fontes de notícias
- **Atualizado:** Conteúdo sempre recente
- **Confiável:** Fonte estável e bem documentada
- **Legal:** Uso permitido para fins educacionais

**Alternativas consideradas:**
- APIs de jornais específicos: Limitado e muitas vezes pago
- Redes sociais: Dados muito ruidosos

### Termos de Busca

**Decisão:** Usar 4 termos específicos: "Inteligência Artificial Piauí", "IA Piauí", "SIA Piauí", "Artificial Intelligence Piauí".

**Justificativa:**
- **Específicos:** Garantem relevância geográfica
- **Variados:** Cobrem diferentes formas de mencionar IA
- **Bilíngues:** Incluem termos em inglês para maior abrangência
- **Limitados:** Evitam sobrecarga do sistema

## Análise de Sentimento

### Abordagem Baseada em Regras

**Decisão:** Implementar análise de sentimento usando dicionários de palavras-chave.

**Justificativa:**
- **Simplicidade:** Fácil de implementar e manter
- **Transparência:** Regras claras e auditáveis
- **Rapidez:** Processamento instantâneo
- **Controle:** Total controle sobre a classificação
- **Educacional:** Demonstra conceitos básicos de NLP

**Alternativas consideradas:**
- Modelos pré-treinados: Complexos e pesados para o escopo
- APIs de sentimento: Dependência externa e custos
- Machine Learning próprio: Requer dataset rotulado

## Interface de Usuário

### Streamlit como Framework

**Decisão:** Usar Streamlit para o dashboard web.

**Justificativa:**
- **Rapidez de desenvolvimento:** Interface web em poucas linhas
- **Python nativo:** Integração perfeita com pandas e plotly
- **Interatividade:** Componentes prontos para filtros e controles
- **Deploy simples:** Facilita publicação
- **Comunidade ativa:** Boa documentação e suporte

**Alternativas consideradas:**
- Flask/Django: Muito complexo para o escopo
- Dash: Similar ao Streamlit, mas menos intuitivo

### Visualizações Escolhidas

**Decisão:** Implementar gráfico de pizza, nuvem de palavras e tabela interativa.

**Justificativa:**
- **Gráfico de pizza:** Mostra proporções de sentimentos de forma clara
- **Nuvem de palavras:** Destaca termos principais visualmente
- **Tabela:** Permite exploração detalhada dos dados
- **Complementares:** Cada visualização oferece perspectiva diferente

## Armazenamento de Dados

### Arquivos CSV Locais

**Decisão:** Salvar dados em arquivos CSV no disco local.

**Justificativa:**
- **Simplicidade:** Sem necessidade de banco de dados
- **Portabilidade:** Arquivos facilmente transferíveis
- **Transparência:** Dados facilmente inspecionáveis
- **Backup simples:** Arquivos podem ser facilmente copiados

## Tratamento de Erros

### Estratégia Defensiva

**Decisão:** Implementar tratamento de erro em pontos críticos com mensagens informativas.

**Justificativa:**
- **Robustez:** Sistema continua funcionando mesmo com falhas parciais
- **Experiência do usuário:** Mensagens claras sobre problemas
- **Debug:** Facilita identificação de problemas

## Design e UX

### Interface Moderna com CSS Customizado

**Decisão:** Aplicar CSS customizado para melhorar a aparência padrão do Streamlit.

**Justificativa:**
- **Profissionalismo:** Visual mais polido e atrativo
- **Usabilidade:** Melhor organização visual da informação
- **Modernidade:** Gradientes e animações sutis

## Limitações Reconhecidas

### Análise de Sentimento Simplificada

**Decisão:** Manter análise baseada em regras apesar das limitações.

**Justificativa educacional:**
- **Transparência:** Usuários entendem como funciona
- **Demonstração:** Mostra conceitos básicos de NLP
- **Honestidade:** Limitações são explicitamente comunicadas
- **Aprendizado:** Base para futuras melhorias

### Volume de Dados Limitado

**Decisão:** Restringir a 15 notícias por coleta.

**Justificativa:**
- **Performance:** Evita sobrecarga do sistema
- **Qualidade:** Foco em relevância ao invés de quantidade
- **Responsabilidade:** Uso moderado de recursos externos
- **Usabilidade:** Volume gerenciável para análise manual

## Decisões de Implementação

### Encoding UTF-8 com BOM

**Decisão:** Usar UTF-8-SIG para salvar CSVs.

**Justificativa:**
- **Compatibilidade Excel:** resolve problemas de acentos
- **Universalidade:** UTF-8 é padrão internacional
- **Robustez:** Preserva caracteres especiais

---

*Este documento será atualizado conforme o projeto evolui.*
