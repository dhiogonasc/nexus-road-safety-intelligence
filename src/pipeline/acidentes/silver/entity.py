from src.shared.model.entity import (
    Schema,
    Table,
    Column,
)

dim_causa = Table(
    name="dim_causa",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            identity=True,
        ),
        Column(
            name="causa",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
    ],
    unique_constraint=["causa"],
)

dim_tipo = Table(
    name="dim_tipo",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            identity=True,
        ),
        Column(
            name="tipo",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
    ],
    unique_constraint=["tipo"],
)

dim_classificacao = Table(
    name="dim_classificacao",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            identity=True,
        ),
        Column(
            name="classificacao",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
    ],
    unique_constraint=["classificacao"],
)

dim_condicao_metereologica = Table(
    name="dim_condicao_metereologica",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            identity=True,
        ),
        Column(
            name="condicao",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
    ],
    unique_constraint=["condicao"],
)

dim_coordenada = Table(
    name="dim_coordenada",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            identity=True,
        ),
        Column(
            name="latitude",
            data_type="DOUBLE",
            attribute="NOT NULL",
        ),
        Column(
            name="longitude",
            data_type="DOUBLE",
            attribute="NOT NULL",
        ),
    ],
    unique_constraint=["latitude", "longitude"],
)

dim_tempo = Table(
    name="dim_tempo",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            attribute="NOT NULL",
            identity=True,
        ),
        Column(
            name="data_hora",
            data_type="TIMESTAMP",
            attribute="NOT NULL",
        ),
        Column(
            name="ano",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="mes",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="dia",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="hora",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="dia_semana",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="fase_dia",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
    ],
    unique_constraint=[
        "ano",
        "mes",
        "dia",
        "hora",
        "dia_semana",
        "fase_dia",
        "data_hora",
    ],
)

dim_pista = Table(
    name="dim_pista",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            attribute="NOT NULL",
            identity=True,
        ),
        Column(
            name="sentido",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="tracado",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="tipo",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="uso_solo",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
    ],
    unique_constraint=[
        "sentido",
        "tracado",
        "tipo",
        "uso_solo",
    ],
)

dim_localizacao = Table(
    name="dim_localizacao",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            attribute="NOT NULL",
            identity=True,
        ),
        Column(
            name="uf",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="br",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="km",
            data_type="DOUBLE",
            attribute="NOT NULL",
        ),
        Column(
            name="municipio",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="regional",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="delegacia",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="uop",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
    ],
    unique_constraint=[
        "uf",
        "br",
        "km",
        "municipio",
        "regional",
        "delegacia",
        "uop",
    ],
)

fato_ocorrencia = Table(
    name="fato_ocorrencia",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            attribute="NOT NULL",
            identity=True,
        ),
        Column(
            name="id_ocorrencia",
            data_type="BIGINT",
            attribute="NOT NULL",
        ),
        Column(
            name="sk_tempo",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="sk_localizacao",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="sk_coordenada",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="sk_causa",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="sk_tipo",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="sk_classificacao",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="sk_pista",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="sk_condicao_metereologica",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="pessoas",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="mortos",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="feridos_leves",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="feridos_graves",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="feridos",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="ilesos",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="ignorados",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
        Column(
            name="veiculos",
            data_type="INTEGER",
            attribute="NOT NULL",
        ),
    ],
    unique_constraint=[
        "id_ocorrencia",
        "sk_tempo",
        "sk_localizacao",
        "sk_coordenada",
        "sk_causa",
        "sk_tipo",
        "sk_classificacao",
        "sk_pista",
        "sk_condicao_metereologica",
    ],
)
