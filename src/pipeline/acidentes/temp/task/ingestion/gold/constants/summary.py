TABLES = [
    {
        "table_name": "agg_categorizacao_local",
        "source_fact_table": "ft_ocorrencia",
        "source_dimension_tables": [
            "dim_local",
            "dim_categoria",
        ],
    }
]
