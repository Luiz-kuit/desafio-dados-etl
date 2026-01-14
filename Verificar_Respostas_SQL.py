
import sqlite3
import pandas as pd
import os

# Caminho do Banco de Dados (está uma pasta acima, na raiz do projeto)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "analytics.db")

def run_queries():
    print(f"--- VERIFICADOR DE RESPOSTAS SQL ---")
    print(f"Lendo banco de dados em: {DB_PATH}\n")

    if not os.path.exists(DB_PATH):
        print(f"ERRO: Banco de dados não encontrado. Execute o script de ETL primeiro!")
        return

    conn = sqlite3.connect(DB_PATH)
    
    queries = [
        ("3. Total streams por gênero", """
        SELECT 
            dg.GenreName AS Genero,
            SUM(fm.Streams_Thousands) AS Total_Streams
        FROM fato_musica fm
        JOIN dim_generos dg ON fm.IdGenre = dg.IdGenre
        GROUP BY dg.GenreName
        ORDER BY Total_Streams DESC
        LIMIT 10;
        """),
        ("4. Média de streams por gênero", """
        SELECT 
            dg.GenreName AS Genero,
            ROUND(AVG(fm.Streams_Thousands), 2) AS Media_Streams
        FROM fato_musica fm
        JOIN dim_generos dg ON fm.IdGenre = dg.IdGenre
        GROUP BY dg.GenreName
        ORDER BY Media_Streams DESC
        LIMIT 10;
        """),
        ("5. Total streams por artista em cada ano (Top 5)", """
        SELECT 
            da.ArtistName AS Artista,
            fm.ReleaseYear AS Ano,
            SUM(fm.Streams_Thousands) AS Total_Streams
        FROM fato_musica fm
        JOIN dim_artistas da ON fm.IdArtist = da.IdArtist
        GROUP BY da.ArtistName, fm.ReleaseYear
        ORDER BY Total_Streams DESC
        LIMIT 5;
        """),
        ("6. Consulta anonimizada (Apenas IDs)", """
        SELECT 
            IdTrack, Title, IdArtist, IdGenre, ReleaseYear, Streams_Thousands
        FROM fato_musica
        LIMIT 10;
        """)
    ]

    for title, sql in queries:
        print(f"\n>> {title}")
        try:
            df = pd.read_sql_query(sql, conn)
            print(df.to_string(index=False))
        except Exception as e:
            print(f"Erro ao executar query: {e}")
        print("-" * 50)

    conn.close()
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    run_queries()
