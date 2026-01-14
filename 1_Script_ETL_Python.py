
import os
import pandas as pd
from sqlalchemy import create_engine
import time

# --- CONFIGURAÇÕES ---
# Conexão com Banco de Dados SQLite (cria um arquivo .db na pasta)
DB_NAME = "analytics.db"
DATABASE_URL = f"sqlite:///{DB_NAME}"

# Diretórios (caminhos das pastas)
# BASE_DIR: Onde este script está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT: Pasta raiz do projeto (um nível acima)
PROJECT_ROOT = os.path.dirname(BASE_DIR)
# DATA_DIR: Onde estão os arquivos originais (doc e excel)
DATA_DIR = os.path.join(PROJECT_ROOT, "Exercícios")
# CURATED_DIR: Onde vamos salvar os arquivos Excel tratados
CURATED_DIR = os.path.join(PROJECT_ROOT, "curated_data")

# Garante que a pasta de arquivos tratados exista
os.makedirs(CURATED_DIR, exist_ok=True)

def get_engine():
    print(f"Conectando ao Banco SQLite: {DB_NAME}...")
    engine = create_engine(DATABASE_URL)
    return engine

def process_commercial(engine):
    print("\n--- Processando Dados COMERCIAIS ---")
    comm_dir = os.path.join(DATA_DIR, "Comercial")
    
    # 1. Lojas (Lojas.xlsx)
    print("Lendo arquivo: Lojas.xlsx...")
    df_lojas = pd.read_excel(os.path.join(comm_dir, "Lojas.xlsx"))
    # Remove espaços em branco dos nomes das colunas
    df_lojas.columns = [c.strip() for c in df_lojas.columns] 
    
    # Salva no Banco de Dados
    df_lojas.to_sql("dim_lojas", engine, if_exists="replace", index=False)
    # Salva em Excel Tratado (para Power BI)
    df_lojas.to_excel(os.path.join(CURATED_DIR, "dim_lojas.xlsx"), index=False)
    print("Sucesso: dim_lojas carregada e exportada.")

    # 2. Consultores / Vendedores (Consultores.xlsx)
    print("Lendo arquivo: Consultores.xlsx...")
    df_cons = pd.read_excel(os.path.join(comm_dir, "Consultores.xlsx"))
    df_cons.columns = [c.strip() for c in df_cons.columns]
    
    # IMPORTANTE: Ordena por Salário (Maior para Menor)
    # Isso garante que se houver ID duplicado, mantemos o cargo mais alto (ex: Gerente)
    df_cons = df_cons.sort_values(by='Wage', ascending=False)
    
    # Remove duplicatas (mantendo apenas o primeiro, que é o de maior salário)
    df_cons = df_cons.drop_duplicates(subset=['IdSeller'], keep='first')
    
    df_cons.to_sql("dim_consultores", engine, if_exists="replace", index=False)
    df_cons.to_excel(os.path.join(CURATED_DIR, "dim_consultores.xlsx"), index=False)
    print("Sucesso: dim_consultores carregada e exportada (Duplicatas resolvidas).")

    # 3. Metas (Metas.xlsx)
    print("Lendo arquivo: Metas.xlsx...")
    df_metas = pd.read_excel(os.path.join(comm_dir, "Metas.xlsx"))
    df_metas.columns = [c.strip() for c in df_metas.columns]
    df_metas.to_sql("fatos_metas", engine, if_exists="replace", index=False)
    df_metas.to_excel(os.path.join(CURATED_DIR, "fatos_metas.xlsx"), index=False)
    print("Sucesso: fatos_metas carregada e exportada.")

    # 4. Vendas (Unificando Trimestres)
    print("Lendo arquivos de Vendas...")
    df_v1 = pd.read_excel(os.path.join(comm_dir, "Vendas.xlsx"))
    df_v2 = pd.read_excel(os.path.join(comm_dir, "Vendas_2T.xlsx"))
    
    # Unifica (Concatena) os arquivos um embaixo do outro
    df_vendas = pd.concat([df_v1, df_v2], ignore_index=True)
    df_vendas.columns = [c.strip() for c in df_vendas.columns]
    
    # Garante que a coluna de Data seja entendida corretamente
    if 'Date' in df_vendas.columns:
        df_vendas['Date'] = pd.to_datetime(df_vendas['Date'])
        
    df_vendas.to_sql("fatos_vendas", engine, if_exists="replace", index=False)
    df_vendas.to_excel(os.path.join(CURATED_DIR, "fatos_vendas.xlsx"), index=False)
    print(f"Sucesso: fatos_vendas carregada ({len(df_vendas)} linhas).")


def process_musical(engine):
    print("\n--- Processando Dados MUSICAIS ---")
    mus_dir = os.path.join(DATA_DIR, "Musical")
    csv_path = os.path.join(mus_dir, "Music Test.csv")
    
    # Tenta ler o CSV (tratando problemas de codificação)
    try:
        df_music = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='skip')
    except:
        df_music = pd.read_csv(csv_path, encoding='latin1', on_bad_lines='skip')
    
    # Limpeza Básica: Remove caracteres estranhos (;;)
    df_music.columns = [c.strip().replace(';;', '') for c in df_music.columns]
    
    for col in df_music.select_dtypes(include='object').columns:
        df_music[col] = df_music[col].str.replace(';;', '', regex=False)

    # 1. Cria Dimensão Artistas (Normalização)
    artists = df_music['Artist'].unique()
    df_artists = pd.DataFrame(artists, columns=['ArtistName'])
    # Cria ID numérico para cada artista
    df_artists['IdArtist'] = range(1, len(df_artists) + 1)
    
    df_artists.to_sql("dim_artistas", engine, if_exists="replace", index=False)
    df_artists.to_excel(os.path.join(CURATED_DIR, "dim_artistas.xlsx"), index=False)
    print("Sucesso: dim_artistas carregada.")

    # 2. Cria Dimensão Gêneros (Normalização)
    genres = df_music['Top Genre'].unique()
    df_genres = pd.DataFrame(genres, columns=['GenreName'])
    df_genres['IdGenre'] = range(1, len(df_genres) + 1)
    
    df_genres.to_sql("dim_generos", engine, if_exists="replace", index=False)
    df_genres.to_excel(os.path.join(CURATED_DIR, "dim_generos.xlsx"), index=False)
    print("Sucesso: dim_generos carregada.")

    # 3. Cria Tabela Fato Musical (Substituindo nomes por IDs)
    df_fact = df_music.merge(df_artists, left_on='Artist', right_on='ArtistName')
    df_fact = df_fact.merge(df_genres, left_on='Top Genre', right_on='GenreName')
    
    # Seleciona e Renomeia apenas as colunas necessárias
    cols_to_keep = {
        'Index': 'IdTrack',
        'Title': 'Title',
        'IdArtist': 'IdArtist',
        'IdGenre': 'IdGenre',
        'Year': 'ReleaseYear',
        'Streams (Thousand)': 'Streams_Thousands',
        'Energy': 'Energy',
        'Danceability': 'Danceability',
        'Loudness (dB)': 'Loudness_dB',
        'Liveness': 'Liveness',
        'Valence': 'Valence',
        'Length (Duration)': 'Duration',
        'Acousticness': 'Acousticness',
        'Speechiness': 'Speechiness',
        'Popularity': 'Popularity'
    }
    
    # Filtra colunas que realmente existem
    available_cols = {k: v for k, v in cols_to_keep.items() if k in df_fact.columns}
    df_final = df_fact[list(available_cols.keys())].rename(columns=available_cols)
    
    df_final.to_sql("fato_musica", engine, if_exists="replace", index=False)
    df_final.to_excel(os.path.join(CURATED_DIR, "fato_musica.xlsx"), index=False)
    print(f"Sucesso: fato_musica carregada ({len(df_final)} linhas).")

if __name__ == "__main__":
    print(f"Raiz do Projeto: {DATA_DIR}")
    print("Iniciando Processo de ETL (Modo Local)...")
    start_time = time.time()
    
    try:
        engine = get_engine()
        process_commercial(engine)
        process_musical(engine)
        print(f"\nETL Concluído com Sucesso em {time.time() - start_time:.2f} segundos.")
        print(f"Banco de Dados criado em: {os.path.join(PROJECT_ROOT, DB_NAME)}")
        print(f"Arquivos Excel Tratados em: {CURATED_DIR}")
    except Exception as e:
        print(f"\nERRO CRÍTICO NO ETL: {e}")
