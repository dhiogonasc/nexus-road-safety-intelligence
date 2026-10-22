from src.shared.model.entity import Table, Column

agg_condicoes_via = Table(
    schema="gold",
    name="agg_condicoes_via",
    columns=[
        Column(
            name="id",
            data_type="INTEGER",
            attribute="NOT NULL",
            identity=True,
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
            name="dia_semana",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="fase_dia",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="condicao_metereologica",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="sentido_via",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="tracado_via",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="tipo_via",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="solo_via",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="total_ocorrencias",
            data_type="BIGINT",
            attribute="NOT NULL",
        ),
        Column(
            name="total_pessoas",
            data_type="BIGINT",
            attribute="NOT NULL",
        ),
        Column(
            name="total_veiculos",
            data_type="BIGINT",
            attribute="NOT NULL",
        ),
        Column(
            name="total_mortos",
            data_type="BIGINT",
            attribute="NOT NULL",
        ),
        Column(
            name="total_feridos",
            data_type="BIGINT",
            attribute="NOT NULL",
        ),
        Column(
            name="total_feridos_graves",
            data_type="BIGINT",
            attribute="NOT NULL",
        ),
        Column(
            name="total_feridos_leves",
            data_type="BIGINT",
            attribute="NOT NULL",
        ),
        Column(
            name="total_ilesos",
            data_type="BIGINT",
            attribute="NOT NULL",
        ),
        Column(
            name="pct_mortalidade",
            data_type="DOUBLE",
            attribute="NOT NULL",
        ),
    ],
    unique_constraint=["id"],
)
