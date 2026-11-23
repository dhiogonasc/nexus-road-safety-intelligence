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
            uf                      || '-' || 
            tipo_area
        ) as sk_malha_geografica,

        md5(
            br                      || '-' ||
            cast(km as varchar)     || '-' || 
            sentido_via             || '-' ||
            tipo_pista
        ) as sk_malha_rodoviaria,

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
        malha_geografica.sk_malha_geografica,
        malha_rodoviaria.sk_malha_rodoviaria,
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

    inner join {{ ref('dim_malha_geografica') }} as malha_geografica 
        on staging.sk_malha_geografica = malha_geografica.sk_malha_geografica

    inner join {{ ref('dim_malha_rodoviaria') }} as malha_rodoviaria 
        on staging.sk_malha_rodoviaria = malha_rodoviaria.sk_malha_rodoviaria

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
