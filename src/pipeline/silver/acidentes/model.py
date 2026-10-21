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
    unique_constraint=["condicao_metereologica"],
)
