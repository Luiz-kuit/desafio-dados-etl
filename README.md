
# Relatório Técnico - Desafio de Dados

---

## 1. Visão Geral da Solução

Para atender aos requisitos de análise de dados (Comercial) e manipulação técnica (SQL), desenvolvi uma arquitetura automatizada utilizando **Python** como motor de ETL e **SQLite** como banco de dados analítico.

### Destaques Técnicos:
*   **Automação**: O script Python lê, trata e carrega os dados automaticamente.
*   **Modelagem**: Transformação de arquivos "flat" (CSV) em modelo **Star Schema** (Fatos e Dimensões).
*   **Tratamento de Dados**: Correção de codificação, limpeza de caracteres especiais (`;;`) e deduplicação inteligente (SCD).

---

## 2. Estrutura da Entrega

Nesta pasta, você encontrará:

1.  **`1_Script_ETL_Python.py`**: 
    *   Código Python responsável por ler as planilhas Excel (Comercial) e CSV (Musical).
    *   Realiza a unificação das Vendas (Q1 + Q2).
    *   **Destaque**: Na tabela de Consultores, foi aplicada uma lógica de de duplicação que prioriza o cargo com **maior salário**, garantindo que promoções sejam refletidas corretamente (resolvendo duplicatas de ID).

2.  **`2_Solucao_Music_Test.sql`**:
    *   Arquivo contendo as queries SQL exatas para responder às 6 perguntas do desafio musical.

3.  **`3_Evidencias_Resultados_SQL.txt`**:
    *   Output gerado pela execução das queries acima, comprovando o funcionamento (Top Streams, Médias, Anonimização).

4.  **`Dashboard_Comercial.pbix`**:
    *   Arquivo do Power BI conectado aos dados tratados.

5.  **`Verificar_Respostas_SQL.py`**:
    *   Script interativo que executa as queries SQL no banco e exibe os resultados na tela para validação imediata.

---

## 3. Detalhes da Implementação

### Desafio 1: Comercial (Power BI + ETL)
*   **Problema**: Arquivos de vendas separados por trimestre e sujeira nos dados.
*   **Solução ETL**: 
    *   Unificação automática via Pandas (`concat`).
    *   Geração de arquivos limpos (`curated_data`) para consumo performático no Power BI.
    *   Cálculo de *Meta Estimada de Unidades* (Meta Financeira / Ticket Médio) para permitir análise de volume vs meta.

### Desafio 2: Music Test (SQL)
*   **Problema**: Arquivo CSV não normalizado e com erros de formatação (`;;`).
*   **Solução SQL**: 
    *   Normalização da tabela única para **Fato Música**, **Dimensão Artistas** e **Dimensão Gêneros**.
    *   Query de Anonimização (Questão 6) expondo apenas os IDs relacionais.

---

## 4. Como Executar (Reprodução)

Caso deseje rodar a automação novamente:
1.  Instale as dependências: `pip install pandas sqlalchemy openpyxl`
2.  Execute o script: `python 1_Script_ETL_Python.py`

---

## 5. Bônus: Arquitetura "Docker Ready"

Embora a solução principal tenha sido desenhada para ser leve (Local-First), deixei o ambiente configurado para execução em containers, garantindo portabilidade e reprodutibilidade em qualquer SO.

**Arquivos Incluídos:**
*   `Dockerfile`: Receita da imagem Python com todas as dependências.
*   `docker-compose.yml`: Orquestração do serviço.

**Para rodar via Docker (Opcional):**
```bash
docker-compose up --build
```
Isso executará todo o pipeline ETL em um ambiente isolado, gerando os resultados na pasta montada.

