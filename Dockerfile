
FROM python:3.9-slim

WORKDIR /app

# Instala dependências do SO (se necessário) e limpa cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os scripts para o container
COPY 1_Script_ETL_Python.py .

# Comando padrão ao iniciar o container
CMD ["python", "1_Script_ETL_Python.py"]
