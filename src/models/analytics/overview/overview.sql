{{
    config(
        materialized='incremental',
        unique_key='id',    
    )
}}

with 

staging as (
    select * from {{ ref('fct_ocorrencia') }} fato
),

aggregation as (
    select
        staging.id,

        categoria.classificacao_acidente,
        clima.condicao_metereologica,

        local.br,
        local.regiao,
        local.estado,
        local.tipo_area,

        tempo.ano,
        tempo.mes,
        tempo.mes_nome,
        tempo.dia_semana,
        tempo.dia_semana_nome,
        tempo.semana

        
        staging.total_envolvidos,
        staging.total_mortos
    from staging

    join {{ ref('dim_categoria') }} as categoria
        on staging.sk_categoria = categoria.sk_categoria

    join {{ ref('dim_clima') }} as clima
        on staging.sk_clima = clima.sk_clima

    join {{ ref('dim_local') }} as local
        on staging.sk_local = local.sk_local

    join {{ ref('dim_tempo') }} as tempo
        on staging.sk_tempo = tempo.sk_tempo
)

select * from aggregation

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.id = id
    )
{% endif %}