{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

with 

raw_staging as (
    select * from {{ ref('stg_ocorrencias') }} 
),

staging as (
    select distinct
        id_ocorrencia,

        md5(
            tipo_acidente           || '-' || 
            causa_acidente          || '-' || 
            classificacao_acidente
        ) as sk_categoria,

        md5(
            cast(br as varchar)     || '-' ||
            regiao                  || '-' || 
            estado                  || '-' || 
            zona
        ) as sk_local,

        md5(
            cast(data as varchar)   || '-' || 
            fase_dia
        ) as sk_tempo,

        md5(
            condicao_metereologica
        ) as sk_clima,

        total_envolvidos,
        total_mortos,
        total_feridos,
        total_ilesos
    from raw_staging
),

fact as (
    select
        md5(
            cast(staging.id_ocorrencia as varchar)
        ) as id,

        categoria.sk_categoria,
        clima.sk_clima,
        local.sk_local,
        tempo.sk_tempo,

        staging.total_envolvidos,
        staging.total_mortos,
        staging.total_feridos,
        staging.total_ilesos

    from staging as staging

    inner join {{ ref('dim_categoria') }} as categoria 
        on staging.sk_categoria = categoria.sk_categoria

    inner join {{ ref('dim_clima') }} as clima 
        on staging.sk_clima = clima.sk_clima

    inner join {{ ref('dim_local') }} as local 
        on staging.sk_local = local.sk_local

    inner join {{ ref('dim_tempo') }} as tempo 
        on staging.sk_tempo = tempo.sk_tempo
)

select * from fact

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.id = fact.id
    )
{% endif %}
