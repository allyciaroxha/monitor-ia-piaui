import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Importa os módulos locais
try:
    from coletor_rss import RSSNewsCollector
    from analise_sentimento import SentimentAnalyzer, processar_sentimentos
except ImportError as e:
    import streamlit as st
    st.error(f"Erro ao importar módulos: {e}")
    st.error("Certifique-se de que os arquivos coletor_rss.py e analise_sentimento.py estão no mesmo diretório.")
    st.stop()

# Configuração da página
st.set_page_config(
    page_title="Monitor IA Piauí",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Cards de métricas */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    
    /* Seções */
    .section-header {
        background: #f8f9fc;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1.5rem 0 1rem 0;
    }
    
    .section-header h3 {
        margin: 0;
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fc;
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Footer */
    .footer {
        margin-top: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        border: 1px solid #e0e6ed;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .footer h4 {
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    /* Tabela */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Alertas personalizados */
    .custom-warning {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #fdcb6e;
    }
    
    .custom-success {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Carrega dados das notícias analisadas"""
    if os.path.exists('noticias_com_sentimento.csv'):
        try:
            return pd.read_csv('noticias_com_sentimento.csv', encoding='utf-8-sig', sep=',')
        except:
            return pd.read_csv('noticias_com_sentimento.csv', encoding='utf-8')
    elif os.path.exists('noticias_ia_piaui.csv'):
        # Se não existe arquivo com sentimento, processa
        df, _ = processar_sentimentos()
        return df
    else:
        return pd.DataFrame()

def collect_fresh_data():
    """Coleta notícias atualizadas"""
    with st.spinner("Buscando notícias..."):
        collector = RSSNewsCollector()
        news_data = collector.coletar_todas_noticias()
        
        if news_data:
            collector.save_to_csv(news_data)
            
            analyzer = SentimentAnalyzer()
            df = pd.DataFrame(news_data)
            df_processed = analyzer.analyze_dataframe(df)
            df_processed.to_csv('noticias_com_sentimento.csv', index=False, encoding='utf-8-sig', sep=',', quotechar='"', quoting=1)
            
            return df_processed
        else:
            return pd.DataFrame()

def create_sentiment_chart(df):
    """Cria gráfico de distribuição de sentimentos"""
    if df.empty:
        return go.Figure()
    
    sentiment_counts = df['sentiment'].value_counts()
    
    colors = {
        'positivo': '#27AE60',
        'negativo': '#E74C3C', 
        'neutro': '#F39C12'
    }
    
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title="Como as notícias estão sendo percebidas",
        color=sentiment_counts.index,
        color_discrete_map=colors
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        textfont_size=12,
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    
    fig.update_layout(
        height=400,
        showlegend=True,
        font=dict(size=12),
        title_font_size=16,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    
    return fig

def generate_wordcloud(text_data):
    """Gera nuvem de palavras das notícias"""
    if not text_data:
        return None
    
    combined_text = ' '.join([str(text) for text in text_data if pd.notna(text)])
    
    if not combined_text.strip():
        return None
    
    wordcloud = WordCloud(
        width=800, 
        height=400,
        background_color='white',
        max_words=50,
        colormap='plasma',
        relative_scaling=0.6,
        min_font_size=10
    ).generate(combined_text)
    
    return wordcloud

def apply_date_filter(df, dias_filtro):
    """Aplica filtro de data ao dataframe"""
    if dias_filtro == "Todas":
        return df
    
    try:
        dias = int(dias_filtro.split()[0])
        data_limite = datetime.now() - timedelta(days=dias)
        
        # Converte coluna de data se necessário
        if 'published' in df.columns:
            df_filtered = df.copy()
            df_filtered['published'] = pd.to_datetime(df_filtered['published'], errors='coerce')
            return df_filtered[df_filtered['published'] >= data_limite]
        elif 'pub_date' in df.columns:
            df_filtered = df.copy()
            df_filtered['pub_date'] = pd.to_datetime(df_filtered['pub_date'], errors='coerce')
            return df_filtered[df_filtered['pub_date'] >= data_limite]
        else:
            return df
    except Exception as e:
        st.warning(f"Erro ao aplicar filtro de data: {e}")
        return df

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Monitor de IA no Piauí</h1>
        <p>Acompanhamento das notícias sobre Inteligência Artificial no estado</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Controles na barra lateral
    st.sidebar.markdown("### ⚙️ Controles")
    
    # Botão de coleta
    if st.sidebar.button("🔄 Buscar Notícias", type="primary"):
        df = collect_fresh_data()
        if not df.empty:
            st.sidebar.success(f"✅ Encontradas {len(df)} notícias!")
            st.rerun()
        else:
            st.sidebar.error("❌ Nenhuma notícia encontrada")
    
    # Carrega dados existentes
    df = load_data()
    
    if df.empty:
        st.markdown("""
        <div class="custom-warning">
            <strong>📋 Primeiro uso?</strong><br>
            Clique em <strong>"Buscar Notícias"</strong> na barra lateral para começar.
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Filtros
    st.markdown('<div class="section-header"><h3>🔍 Filtros</h3></div>', unsafe_allow_html=True)
    
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        sentimento_filtro = st.selectbox(
            "Filtrar por sentimento:",
            ["Todas"] + list(df['sentiment'].unique()) if 'sentiment' in df.columns else ["Todas"]
        )
    
    with col_filter2:
        if 'search_term' in df.columns:
            termo_filtro = st.selectbox(
                "Filtrar por termo de busca:",
                ["Todos"] + list(df['search_term'].unique())
            )
        else:
            termo_filtro = "Todos"
            st.selectbox("Filtrar por termo de busca:", ["Todos"], disabled=True)
    
    with col_filter3:
        # Filtro por data (últimos N dias)
        dias_filtro = st.selectbox(
            "Mostrar notícias dos últimos:",
            ["Todas", "7 dias", "15 dias", "30 dias"]
        )
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if sentimento_filtro != "Todas" and 'sentiment' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['sentiment'] == sentimento_filtro]
    
    if termo_filtro != "Todos" and 'search_term' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['search_term'] == termo_filtro]
    
    # Aplicar filtro de data
    df_filtrado = apply_date_filter(df_filtrado, dias_filtro)
    
    # Mostrar estatísticas dos dados filtrados
    if len(df_filtrado) != len(df):
        st.info(f"📊 Mostrando {len(df_filtrado)} de {len(df)} notícias após aplicar filtros")
    
    # Resumo dos dados
    st.markdown('<div class="section-header"><h3>📊 Resumo dos Dados</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(df_filtrado)
        st.metric("Total", total)
    
    with col2:
        if 'sentiment' in df_filtrado.columns:
            positivas = len(df_filtrado[df_filtrado['sentiment'] == 'positivo'])
            st.metric("Positivas", positivas)
        else:
            st.metric("Positivas", "N/A")
    
    with col3:
        if 'sentiment' in df_filtrado.columns:
            negativas = len(df_filtrado[df_filtrado['sentiment'] == 'negativo'])
            st.metric("Negativas", negativas)
        else:
            st.metric("Negativas", "N/A")
    
    with col4:
        if 'sentiment' in df_filtrado.columns:
            neutras = len(df_filtrado[df_filtrado['sentiment'] == 'neutro'])
            st.metric("Neutras", neutras)
        else:
            st.metric("Neutras", "N/A")
    
    # Visualizações principais
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown('<div class="section-header"><h3>📈 Análise de Sentimentos</h3></div>', unsafe_allow_html=True)
        if 'sentiment' in df_filtrado.columns and not df_filtrado.empty:
            chart = create_sentiment_chart(df_filtrado)
            st.plotly_chart(chart, width='stretch')
        else:
            st.info("Dados de sentimento não disponíveis")
    
    with col_right:
        st.markdown('<div class="section-header"><h3>☁️ Termos Mais Mencionados</h3></div>', unsafe_allow_html=True)
        if 'full_text' in df_filtrado.columns and not df_filtrado.empty:
            wordcloud = generate_wordcloud(df_filtrado['full_text'].tolist())
            if wordcloud:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.info("Aguardando mais dados para gerar a nuvem de palavras")
        else:
            st.info("Dados de texto não disponíveis")
    
    # Novo gráfico - Distribuição por termo de busca
    if 'search_term' in df_filtrado.columns and len(df_filtrado['search_term'].unique()) > 1:
        st.markdown('<div class="section-header"><h3>🔍 Distribuição por Termo de Busca</h3></div>', unsafe_allow_html=True)
        
        # Gráfico de barras por termo de busca
        termo_counts = df_filtrado['search_term'].value_counts()
        fig_bar = px.bar(
            x=termo_counts.index,
            y=termo_counts.values,
            title="Quantidade de notícias por termo de pesquisa",
            labels={'x': 'Termo de Busca', 'y': 'Quantidade de Notícias'},
            color=termo_counts.values,
            color_continuous_scale='viridis'
        )
        fig_bar.update_layout(
            showlegend=False,
            height=400,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_bar, width='stretch')
    
    # Novo gráfico - Timeline de notícias (se houver dados de data)
    if ('published' in df_filtrado.columns or 'pub_date' in df_filtrado.columns) and not df_filtrado.empty:
        st.markdown('<div class="section-header"><h3>📅 Timeline de Notícias</h3></div>', unsafe_allow_html=True)
        
        try:
            df_timeline = df_filtrado.copy()
            date_col = 'published' if 'published' in df_filtrado.columns else 'pub_date'
            df_timeline[date_col] = pd.to_datetime(df_timeline[date_col], errors='coerce')
            df_timeline = df_timeline.dropna(subset=[date_col])
            
            if not df_timeline.empty:
                # Agrupa por data
                timeline_data = df_timeline.groupby(df_timeline[date_col].dt.date).size().reset_index()
                timeline_data.columns = ['data', 'quantidade']
                
                fig_timeline = px.line(
                    timeline_data,
                    x='data',
                    y='quantidade',
                    title="Volume de notícias ao longo do tempo",
                    labels={'data': 'Data', 'quantidade': 'Número de Notícias'}
                )
                fig_timeline.update_layout(height=400)
                st.plotly_chart(fig_timeline, width='stretch')
        except Exception as e:
            st.warning(f"Não foi possível criar timeline: {e}")
    
    # Tabela de notícias
    st.markdown('<div class="section-header"><h3>📰 Notícias</h3></div>', unsafe_allow_html=True)
    
    # Mostrar tabela
    if not df_filtrado.empty:
        # Determinar quais colunas mostrar
        colunas_disponiveis = df_filtrado.columns.tolist()
        colunas_exibir = []
        
        if 'title' in colunas_disponiveis:
            colunas_exibir.append('title')
        if 'sentiment' in colunas_disponiveis:
            colunas_exibir.append('sentiment')
        if 'search_term' in colunas_disponiveis:
            colunas_exibir.append('search_term')
        if 'pub_date' in colunas_disponiveis:
            colunas_exibir.append('pub_date')
        elif 'published' in colunas_disponiveis:
            colunas_exibir.append('published')
        
        # Se não temos as colunas padrão, mostra as primeiras disponíveis
        if not colunas_exibir:
            colunas_exibir = colunas_disponiveis[:4]
        
        st.dataframe(
            df_filtrado[colunas_exibir],
            width='stretch',
            height=400
        )
        
        # Download
        csv_data = df_filtrado.to_csv(index=False, encoding='utf-8-sig', sep=',', quotechar='"', quoting=1)
        st.download_button(
            label="📥 Baixar dados (CSV)",
            data=csv_data,
            file_name=f"noticias_ia_piaui_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Nenhuma notícia corresponde aos filtros selecionados")
    
    # Rodapé informativo
    st.markdown("""
    <div class="footer">
        <h4>ℹ️ Sobre este Sistema</h4>
                
        Este monitoramento utiliza análise automatizada de sentimentos baseada em palavras-chave para:
            Buscar notícias no Google Notícias sobre IA no Piauí
            Analisar o tom das notícias (positivo, negativo, neutro)
            Gerar visualizações dos dados coletados
            Permitir exportar os resultados
            Filtrar dados por sentimento, termo e período
        
        ⚠️ Limitações: A análise é baseada em regras simples e pode não capturar nuances como ironia ou contextos complexos.
                
        Sistema desenvolvido para fins educacionais - Projeto de Monitoramento de IA no Piauí.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()