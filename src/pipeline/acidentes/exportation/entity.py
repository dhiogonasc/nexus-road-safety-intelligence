from settings import postgres_settings
from src.shared.model.entity import Table, Column

agg_condicoes_via = Table(
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

agg_sazonalidade = Table(
    catalog=postgres_settings.DB_NAME,
    schema="analytics",
    name="agg_sazonalidade",
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
            name="causa_acidente",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="tipo_acidente",
            data_type="VARCHAR",
            attribute="NOT NULL",
        ),
        Column(
            name="classificacao_acidente",
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

agg_trechos_criticos = Table(
    catalog=postgres_settings.DB_NAME,
    schema="analytics",
    name="agg_trechos_criticos",
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
