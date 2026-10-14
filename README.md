# Nexus Road Safety Intelligence

Este projeto implementa uma arquitetura de engenharia de dados moderna combinando **DuckDB** e **PostgreSQL**, orquestrada com **Prefect**, estruturada em camadas (Bronze, Silver, Gold) e orientada a perfis de ambiente (`dev`, `prod`).

---

## 1. Visão Geral da Arquitetura e Organização de Pastas

A estrutura do projeto separa a infraestrutura de orquestração (`pipeline/`), a lógica de negócio e transformação de dados (`src/pipeline/`), e as utilidades compartilhadas de banco de dados e sistema (`src/shared/`).

```text
dhiogonasc-nexus-road-safety-intelligence/
├── config.py                 # Configurações globais e Pydantic Settings
├── constants.py              # Definições de caminhos e constantes globais
├── docker-compose.yml        # Subida do PostgreSQL local via Docker
├── requirements.txt          # Dependências do projeto Python
├── test_connection.py        # Script de validação da conexão DuckDB -> PostgreSQL
├── .env.example              # Template de variáveis de ambiente
├── data/
│   └── db/                   # Armazenamento local do DuckDB (.db)
├── pipeline/                 # DAGs e fluxos principais do Prefect
│   ├── dag_bronze.py         # Ingestão de arquivos CSV (Stage)
│   ├── dag_silver.py         # Transformação e modelagem dimensional
│   ├── dag_gold.py           # Agregações e sincronização com PostgreSQL
│   ├── dag_main.py           # Execução completa da pipeline end-to-end
│   ├── dag_setup.py          # Configuração inicial de extensões e schemas
│   └── setup/                # Tarefas de infraestrutura inicial
└── src/                      # Código fonte da lógica de engenharia
    ├── pipeline/             # Módulos de pipelines divididos por domínio (acidentes)
    │   ├── index.py          # Configuração dos schemas e mapeamento das tabelas
    │   ├── bronze/           # Extração e DDLs da camada Bronze
    │   ├── silver/           # Tabelas dimensionais e fatos (Silver)
    │   └── gold/             # Tabelas agregadas e lógica de upsert/merge (Gold)
    └── shared/               # Utilitários globais reutilizáveis
        ├── db/               # Gestão de conexões DuckDB e operações SQL
        ├── pipeline/         # Tarefas base do Prefect
        └── system/           # Funções auxiliares de sistema e carregamento de arquivos SQL

```

---

## 2. Dependências e Configuração do Ambiente

### Pré-requisitos

* **Python 3.10+** instalado.
* **Docker** e **Docker Compose** (para provisionar o PostgreSQL de desenvolvimento).

### Instalação de Dependências

Para configurar o ambiente de desenvolvimento e instalar todas as bibliotecas necessárias listadas em `requirements.txt`:

* **Linux (Bash):**
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```


* **Windows (PowerShell / Command Prompt):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

```



### Configuração das Variáveis de Ambiente

O projeto utiliza perfis de configuração por meio de arquivos `.env.{profile}` (controlados pela variável de ambiente `ENV`).

1. Copie o arquivo de exemplo `.env.example` para criar os arquivos de perfil desejados (por exemplo, `.env.dev` ou `.env.prod`):
```bash
cp .env.example .env.dev

```


2. Edite os arquivos de configuração com as credenciais reais do seu banco de dados PostgreSQL.

Para iniciar a base PostgreSQL local via Docker Compose:

```bash
docker compose up -d

```

Para validar se o DuckDB consegue se conectar corretamente ao PostgreSQL utilizando o perfil ativo:

```bash
ENV=dev .venv/bin/python test_connection.py

```

*(No Windows PowerShell, use `$env:ENV="dev"; python test_connection.py`)*

---

## 3. Instruções de Execução

As execuções utilizam a especificação de perfil por variável de ambiente (`ENV={profile}`).

### Execução Geral (Pipeline Completa End-to-End)

Executa a configuração inicial (`dag_setup`), seguida pelas camadas Bronze, Silver e Gold para todos os schemas configurados no índice do projeto (`PIPELINE_CONFIG` em `src/pipeline/index.py`).

* **Linux (Bash):**
```bash
ENV=dev .venv/bin/python -m pipeline.dag_main

```


* **Windows (PowerShell):**
```powershell
$env:ENV="dev"; .venv\Scripts\python -m pipeline.dag_main

```



---

### Execução Isolada por DAG e Schema

Cada camada/DAG pode ser executada de forma independente informando o argumento `--schema`.

#### 1. Camada Setup (Configuração de Extensões e Schema Analytics no Postgres)

* **Linux:**
```bash
ENV=dev .venv/bin/python -m pipeline.dag_setup

```


* **Windows:**
```powershell
$env:ENV="dev"; .venv\Scripts\python -m pipeline.dag_setup

```



#### 2. Camada Bronze (Extração de CSVs para Stage)

* **Linux:**
```bash
ENV=dev .venv/bin/python -m pipeline.dag_bronze --schema acidentes

```


* **Windows:**
```powershell
$env:ENV="dev"; .venv\Scripts\python -m pipeline.dag_bronze --schema acidentes

```



#### 3. Camada Silver (Transformação, Normalização e Modelagem Fato/Dimensão)

* **Linux:**
```bash
ENV=dev .venv/bin/python -m pipeline.dag_silver --schema acidentes

```


* **Windows:**
```powershell
$env:ENV="dev"; .venv\Scripts\python -m pipeline.dag_silver --schema acidentes

```



#### 4. Camada Gold (Agregações de Negócio e Sincronização/Upsert para o PostgreSQL)

* **Linux:**
```bash
ENV=dev .venv/bin/python -m pipeline.dag_gold --schema acidentes

```


* **Windows:**
```powershell
$env:ENV="dev"; .venv\Scripts\python -m pipeline.dag_gold --schema acidentes

```



---

## 4. Convenção de Escrita e Organização

Para garantir manutenibilidade e padronização, o projeto segue rígidas convenções:

* **Separação de Lógica e SQL:** Todo o código SQL reside em arquivos `.sql` dentro de subpastas chamadas `sql/` correspondentes ao módulo Python. O carregamento é feito de forma dinâmica utilizando `load_module_queries` (`src/shared/system/file.py`).
* **Tratamento de Dados em DuckDB:** O uso de funções como `strip_accents`, padronização para minúsculas (`LOWER`), remoção de caracteres especiais via `REGEXP_REPLACE`, e tratamento de chaves substitutas (`MD5` hash de concatenação) é aplicado de forma consistente na camada Silver.
* **Orquestração com Prefect:** Cada etapa lógica e atômica da pipeline é decorada com `@task` ou `@flow`, permitindo controle de dependências explícitas (`depends_on`) e paralelismo gerenciado.
* **Padronização de Nomes:** Nomes de tabelas de stage começam com `stg_`, dimensões com `dim_`, fatos com `fato_`, e agregações analíticas com `agg_`.

---

## 5. Como Evoluir o Desenvolvimento do Projeto

Para expandir o projeto com novos domínios de dados ou novas tabelas, siga os passos abaixo estruturados sobre a arquitetura base:

### Passo 1: Adicionar Dados Brutos

Insira os novos arquivos de origem (por exemplo, novos CSVs) na estrutura de diretórios em `data/raw/{novo_dominio}/`. Atualize as constantes globais de caminhos em `constants.py`.

### Passo 2: Configurar o Domínio no Índice (`src/pipeline/index.py`)

Adicione o novo schema ao dicionário `PIPELINE_CONFIG`, especificando:

* O mapeamento do arquivo na chave `bronze`.
* As tabelas dimensionais e fatos ordenadas por dependência na chave `silver`.
* As tabelas de agregação analítica e suas chaves primárias (`primary_keys`) na chave `gold`.

### Passo 3: Criar os Scripts e Consultas SQL das Camadas

1. **Bronze:** Crie a lógica de leitura caso necessite de parâmetros customizados, reutilizando `create_stage_table_from_csv`.
2. **Silver:** Crie uma nova pasta em `src/pipeline/silver/{novo_dominio}/`, adicione o arquivo `transform.py` e crie a subpasta `sql/` contendo os scripts `.sql` de criação das dimensões e fatos utilizando instruções `CREATE OR REPLACE TABLE`.
3. **Gold:** Crie uma nova pasta em `src/pipeline/silver/...` ou `src/pipeline/gold/{novo_dominio}/`, implementando as agregações de negócio e consultas de carga.

### Passo 4: Registrar e Executar

Como as DAGs (`dag_bronze.py`, `dag_silver.py`, `dag_gold.py`) são dinâmicas e iteram sobre o `PIPELINE_CONFIG`, qualquer novo schema ou tabela adicionado no índice será automaticamente integrado e executado ao rodar as pipelines gerais ou isoladas com o parâmetro `--schema {novo_schema}`.