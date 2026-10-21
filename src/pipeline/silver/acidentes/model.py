from src.shared.model.table import Table, Column

dim_causa = Table(
    schema="silver",
    name="dim_causa",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            identity=True,
        ),
        Column(
            name="id_carga",
            data_type="VARCHAR",
            attribute="NOT NULL",
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
    schema="silver",
    name="dim_tipo",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            identity=True,
        ),
        Column(
            name="id_carga",
            data_type="VARCHAR",
            attribute="NOT NULL",
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
    schema="silver",
    name="dim_classificacao",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            identity=True,
        ),
        Column(
            name="id_carga",
            data_type="VARCHAR",
            attribute="NOT NULL",
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
    schema="silver",
    name="dim_condicao_metereologica",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            identity=True,
        ),
        Column(
            name="id_carga",
            data_type="VARCHAR",
            attribute="NOT NULL",
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
    schema="silver",
    name="dim_coordenada",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            identity=True,
        ),
        Column(
            name="id_carga",
            data_type="VARCHAR",
            attribute="NOT NULL",
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
    schema="silver",
    name="dim_tempo",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            attribute="NOT NULL",
            identity=True,
        ),
        Column(
            name="id_carga",
            data_type="VARCHAR",
            attribute="NOT NULL",
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
    schema="silver",
    name="dim_pista",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            attribute="NOT NULL",
            identity=True,
        ),
        Column(
            name="id_carga",
            data_type="VARCHAR",
            attribute="NOT NULL",
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
    schema="silver",
    name="dim_localizacao",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            attribute="NOT NULL",
            identity=True,
        ),
        Column(
            name="id_carga",
            data_type="VARCHAR",
            attribute="NOT NULL",
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
