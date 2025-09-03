import pandas as pd
import re
from collections import Counter

class SentimentAnalyzer:
    def __init__(self):
        # Palavras que indicam sentimento positivo
        self.palavras_positivas = {
            'boa', 'bom', 'excelente', 'ótimo', 'incrível', 'inovador', 'inovação', 
            'progresso', 'avanço', 'sucesso', 'positivo', 'benefício', 'beneficia',
            'melhora', 'melhor', 'eficiente', 'eficiência', 'revolucionar', 
            'transformar', 'oportunidade', 'crescimento', 'desenvolvimento',
            'modernizar', 'facilitar', 'otimizar', 'vantagem', 'promissor',
            'futuro', 'tecnológico', 'digital', 'inteligente', 'automatizar'
        }
        
        # Palavras que indicam sentimento negativo
        self.palavras_negativas = {
            'ruim', 'péssimo', 'terrível', 'problema', 'prejuízo', 'perda', 
            'ameaça', 'risco', 'perigo', 'negativo', 'preocupação', 'medo',
            'substituir', 'demitir', 'desemprego', 'eliminar', 'reduzir',
            'cortar', 'falha', 'erro', 'defeito', 'limitação', 'dificuldade',
            'complexo', 'caro', 'custoso', 'invasivo', 'privacidade', 'ética'
        }
        
    def preparar_texto(self, texto):
        """Prepara o texto para análise"""
        if not texto:
            return ""
        
        texto = texto.lower()
        # Remove pontuação mantendo acentos
        texto = re.sub(r'[^\w\sáéíóúâêîôûàèìòùãõçÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÃÕÇ]', ' ', texto)
        # Remove espaços múltiplos
        texto = re.sub(r'\s+', ' ', texto).strip()
        return texto
    
    def analisar_sentimento(self, texto):
        """Analisa o sentimento do texto baseado em palavras-chave"""
        if not texto:
            return 'neutro'
            
        texto_limpo = self.preparar_texto(texto)
        palavras = set(texto_limpo.split())
        
        pontos_positivos = len(palavras.intersection(self.palavras_positivas))
        pontos_negativos = len(palavras.intersection(self.palavras_negativas))
        
        if pontos_positivos > pontos_negativos:
            return 'positivo'
        elif pontos_negativos > pontos_positivos:
            return 'negativo'
        else:
            return 'neutro'
    
    def extrair_palavras_chave(self, lista_textos, tamanho_min=3, top_n=20):
        """Extrai as palavras mais frequentes dos textos"""
        todas_palavras = []
        
        for texto in lista_textos:
            if texto:
                texto_limpo = self.preparar_texto(texto)
                palavras = [palavra for palavra in texto_limpo.split() 
                           if len(palavra) >= tamanho_min and palavra not in self.obter_stop_words()]
                todas_palavras.extend(palavras)
        
        # Conta a frequência das palavras
        contagem_palavras = Counter(todas_palavras)
        return contagem_palavras.most_common(top_n)
    
    def obter_stop_words(self):
        """Lista de palavras comuns que devem ser ignoradas"""
        return {
            'para', 'com', 'uma', 'dos', 'das', 'que', 'por', 'como', 
            'mais', 'ter', 'ser', 'ter', 'sua', 'seu', 'seus', 'suas',
            'este', 'esta', 'isto', 'esse', 'essa', 'isso', 'aquele',
            'aquela', 'aquilo', 'todo', 'toda', 'todos', 'todas',
            'muito', 'muita', 'muitos', 'muitas', 'sobre', 'entre',
            'durante', 'depois', 'antes', 'ainda', 'também', 'assim',
            'onde', 'quando', 'porque', 'pois', 'mas', 'porém', 'contudo',
            'entretanto', 'então', 'agora', 'hoje', 'ontem', 'amanhã',
            'ano', 'anos', 'dia', 'dias', 'vez', 'vezes', 'pode', 'podem',
            'deve', 'devem', 'vai', 'vão', 'está', 'estão', 'foi', 'foram'
        }
    
    def analyze_dataframe(self, df):
        """Analisa o sentimento das notícias no DataFrame"""
        if df.empty:
            return df
        
        # Garante que as colunas necessárias existam
        if 'title' not in df.columns:
            df['title'] = ""
        if 'description' not in df.columns:
            df['description'] = ""
        
        # Combina título e descrição para uma análise mais completa
        df['full_text'] = df['title'].fillna('') + ' ' + df['description'].fillna('')
        
        # Aplica a análise de sentimento
        df['sentiment'] = df['full_text'].apply(self.analisar_sentimento)
        
        return df
    
    def gerar_dados_wordcloud(self, df):
        """Prepara dados para gerar nuvem de palavras"""
        if df.empty:
            return {}
        
        todos_textos = df['full_text'].dropna().tolist()
        palavras_chave = self.extrair_palavras_chave(todos_textos)
        
        return dict(palavras_chave)

def processar_sentimentos(arquivo_csv='noticias_ia_piaui.csv'):
    """Processa a análise de sentimento das notícias"""
    try:
        # Carrega o arquivo CSV
        df = pd.read_csv(arquivo_csv, encoding='utf-8-sig', sep=',')
        print(f"Carregadas {len(df)} notícias do arquivo {arquivo_csv}")
        
        analisador = SentimentAnalyzer()
        df_analisado = analisador.analyze_dataframe(df)
        
        # Organiza as colunas
        ordem_colunas = ['title', 'link', 'description', 'pub_date', 'search_term', 'collected_at', 'full_text', 'sentiment']
        colunas_existentes = [col for col in ordem_colunas if col in df_analisado.columns]
        df_analisado = df_analisado[colunas_existentes]
        
        # Salva o resultado
        arquivo_saida = 'noticias_com_sentimento.csv'
        df_analisado.to_csv(arquivo_saida, index=False, encoding='utf-8-sig', sep=',', quotechar='"', quoting=1)
        print(f"\nResultados salvos em {arquivo_saida}")
        
        # Mostra estatísticas
        contagem_sentimentos = df_analisado['sentiment'].value_counts()
        print("\nDistribuição de Sentimentos:")
        for sentimento, quantidade in contagem_sentimentos.items():
            porcentagem = (quantidade / len(df_analisado)) * 100
            print(f"{sentimento.capitalize()}: {quantidade} ({porcentagem:.1f}%)")
        
        # Gera dados para wordcloud
        dados_wordcloud = analisador.gerar_dados_wordcloud(df_analisado)
        palavras_top = list(dados_wordcloud.keys())[:10]
        print(f"\nPalavras mais mencionadas: {palavras_top}")
        
        return df_analisado, dados_wordcloud
        
    except FileNotFoundError:
        print(f"Arquivo {arquivo_csv} não encontrado. Execute primeiro o coletor de notícias.")
        return pd.DataFrame(), {}
    except Exception as e:
        print(f"Erro ao processar análise de sentimento: {e}")
        return pd.DataFrame(), {}

if __name__ == "__main__":
    df_resultado, dados_wordcloud = processar_sentimentos()
    
    if not df_resultado.empty:
        print("\nPrévia das notícias analisadas:")
        print(df_resultado[['title', 'sentiment']].head())