
-- 1. Verifique o total de streams por gênero
SELECT 
    dg."GenreName",
    SUM(fm."Streams_Thousands") as Total_Streams_Thousands
FROM fato_musica fm
JOIN dim_generos dg ON fm."IdGenre" = dg."IdGenre"
GROUP BY dg."GenreName"
ORDER BY Total_Streams_Thousands DESC;

-- 2. Verifique a média de streams por gênero
SELECT 
    dg."GenreName",
    AVG(fm."Streams_Thousands") as Avg_Streams_Thousands
FROM fato_musica fm
JOIN dim_generos dg ON fm."IdGenre" = dg."IdGenre"
GROUP BY dg."GenreName"
ORDER BY Avg_Streams_Thousands DESC;

-- 3. Verifique o total de streams por artista em cada ano
SELECT 
    da."ArtistName",
    fm."ReleaseYear",
    SUM(fm."Streams_Thousands") as Total_Streams_Thousands
FROM fato_musica fm
JOIN dim_artistas da ON fm."IdArtist" = da."IdArtist"
GROUP BY da."ArtistName", fm."ReleaseYear"
ORDER BY da."ArtistName", fm."ReleaseYear";

-- 4. Realize uma consulta da tabela completa anonimizando artista e gênero, a partir dos IDs
SELECT 
    fm."IdTrack",
    fm."Title",
    fm."IdArtist",    -- Anonimizado (apenas ID)
    fm."IdGenre",     -- Anonimizado (apenas ID)
    fm."ReleaseYear",
    fm."Streams_Thousands",
    fm."Energy",
    fm."Danceability",
    fm."Loudness_dB",
    fm."Liveness",
    fm."Valence",
    fm."Duration",
    fm."Acousticness",
    fm."Speechiness",
    fm."Popularity"
FROM fato_musica fm;
