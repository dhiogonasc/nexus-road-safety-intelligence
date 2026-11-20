{{
    config(
        materialized='incremental',
        unique_key='id',    
    )
}}

with 

tempo as (
    select 
        sk_tempo,
        mes,
        mes_nome,
        dia_semana,
        dia_semana_nome,
        fase_dia,
        fase_dia_desc
    from {{ ref('dim_tempo') }}
),

categoria as (
    select * from {{ ref('dim_categoria') }}
),

aggregation as (
    select
        tempo.sk_tempo,
        categoria.sk_categoria,
        cast(sum(fato.total_mortos) as bigint) as total_mortos,
        cast(sum(fato.total_envolvidos) as bigint) as total_envolvidos,
        cast(count(fato.id) as bigint) as total_ocorrencias,

        cast(
            round(sum(fato.total_mortos)/ nullif(sum(fato.total_envolvidos), 0), 2) 
            as decimal(5, 2)
        ) as taxa_mortalidade,
        cast(
            round(sum(fato.total_mortos) / nullif(count(fato.id), 0), 2)
            as decimal(5, 2)
        ) as indice_mortalidade_ocorrencia,
        cast(
            round(sum(fato.total_envolvidos) / nullif(count(fato.id), 0), 2)
            as decimal(5, 2)
        ) as indice_envolvimento_ocorrencia

    from {{ ref('fct_ocorrencia') }} fato
    join tempo on fato.sk_tempo = tempo.sk_tempo
    join categoria on fato.sk_categoria = categoria.sk_categoria

    group by
        tempo.sk_tempo,
        categoria.sk_categoria,
),

description as (
    select
        md5(aggregation.sk_tempo || '-' || aggregation.sk_categoria) as id,

        tempo.mes,
        tempo.mes_nome,
        tempo.dia_semana,
        tempo.dia_semana_nome,
        tempo.fase_dia,
        tempo.fase_dia_desc,
        categoria.tipo_acidente,
        categoria.causa_acidente,
        categoria.classificacao_acidente,

        total_envolvidos,
        total_mortos,
        total_ocorrencias,
        taxa_mortalidade,
        indice_mortalidade_ocorrencia,
        indice_envolvimento_ocorrencia

    from aggregation
    join tempo on aggregation.sk_tempo = tempo.sk_tempo
    join categoria on aggregation.sk_categoria = categoria.sk_categoria
)

select * from description

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} 
        where {{ this }}.id = description.id
    )
{% endif %}