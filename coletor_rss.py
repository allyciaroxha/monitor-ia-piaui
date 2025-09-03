import requests
import xml.etree.ElementTree as ET
import pandas as pd
import re
from datetime import datetime
import json
from urllib.parse import quote

class RSSNewsCollector:
    def __init__(self):
        self.base_url = "https://news.google.com/rss/search"
        self.termos_busca = [
            "Inteligência Artificial Piauí",
            "IA Piauí", 
            "SIA Piauí",
            "Artificial Intelligence Piauí"
        ]
        
    def limpar_texto(self, texto):
        """Remove tags HTML e caracteres desnecessários"""
        if not texto:
            return ""
        
        # Remove tags HTML
        texto_limpo = re.sub(r'<[^>]+>', '', texto)
        # Remove caracteres especiais mantendo acentos
        texto_limpo = re.sub(r'[^\w\sáéíóúâêîôûàèìòùãõçÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÃÕÇ]', ' ', texto_limpo)
        # Remove espaços múltiplos
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
        return texto_limpo
    
    def buscar_noticias_rss(self, termo_busca, max_resultados=5):
        """Busca notícias no feed RSS do Google News"""
        try:
            termo_codificado = quote(termo_busca)
            url = f"{self.base_url}?q={termo_codificado}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            resposta = requests.get(url, headers=headers, timeout=10)
            resposta.raise_for_status()
            
            # Processa o XML retornado
            root = ET.fromstring(resposta.content)
            
            noticias = []
            items = root.findall('.//item')[:max_resultados]
            
            for item in items:
                titulo = item.find('title')
                link = item.find('link') 
                descricao = item.find('description')
                data_pub = item.find('pubDate')
                
                noticia = {
                    'title': self.limpar_texto(titulo.text if titulo is not None else ""),
                    'link': link.text if link is not None else "",
                    'description': self.limpar_texto(descricao.text if descricao is not None else ""),
                    'pub_date': data_pub.text if data_pub is not None else "",
                    'search_term': termo_busca,
                    'collected_at': datetime.now().isoformat()
                }
                noticias.append(noticia)
                
            return noticias
            
        except Exception as e:
            print(f"Erro ao buscar notícias para '{termo_busca}': {e}")
            return []
    
    def coletar_todas_noticias(self):
        """Busca notícias para todos os termos configurados"""
        todas_noticias = []
        
        for termo in self.termos_busca:
            print(f"Buscando notícias para: {termo}")
            noticias = self.buscar_noticias_rss(termo)
            todas_noticias.extend(noticias)
        
        # Remove duplicatas baseadas no título
        titulos_vistos = set()
        noticias_unicas = []
        
        for noticia in todas_noticias:
            titulo_normalizado = noticia['title'].lower()
            if titulo_normalizado not in titulos_vistos and titulo_normalizado:
                titulos_vistos.add(titulo_normalizado)
                noticias_unicas.append(noticia)
        
        # Limita o número de notícias para não sobrecarregar
        return noticias_unicas[:15]
    
    def save_to_csv(self, news_data, filename='noticias_ia_piaui.csv'):
        """Salva os dados coletados em CSV com separador correto"""
        if not news_data:
            print("Nenhum dado para salvar")
            return
            
        df = pd.DataFrame(news_data)
        
        # Garante que todas as colunas estão presentes
        columns = ['title', 'link', 'description', 'pub_date', 'search_term', 'collected_at']
        for col in columns:
            if col not in df.columns:
                df[col] = ""
        
        # Reordena as colunas
        df = df[columns]
        
        # Salva com separador correto e codificação UTF-8
        df.to_csv(filename, index=False, encoding='utf-8-sig', sep=',', quotechar='"', quoting=1)
        print(f"Dados salvos em {filename} ({len(df)} registros)")
        
        # Mostra preview dos primeiros registros
        print("\nPreview dos dados salvos:")
        print(df.head(3).to_string())
        
    def save_to_json(self, news_data, filename='noticias_ia_piaui.json'):
        """Salva os dados coletados em JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        print(f"Dados salvos em {filename}")

if __name__ == "__main__":
    coletor = RSSNewsCollector()
    dados_noticias = coletor.coletar_todas_noticias()
    
    if dados_noticias:
        print(f"Total de notícias encontradas: {len(dados_noticias)}")
        coletor.save_to_csv(dados_noticias)
        coletor.save_to_json(dados_noticias)
        
        # Mostra prévia dos dados
        df = pd.DataFrame(dados_noticias)
        print("\nPrévia das notícias coletadas:")
        print(df[['title', 'search_term']].head())
    else:
        print("Nenhuma notícia foi encontrada.")