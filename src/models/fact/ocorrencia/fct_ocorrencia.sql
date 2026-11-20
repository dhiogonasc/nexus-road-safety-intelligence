{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

with fact as (
    select distinct
        md5(cast(staging.id_ocorrencia as varchar)) as id,
        
        categoria.sk_categoria,
        clima.sk_clima,
        local.sk_local,
        tempo.sk_tempo,

        staging.total_veiculos,
        staging.total_envolvidos,
        staging.total_mortos,
        staging.total_feridos,
        staging.total_ilesos

    from {{ ref('stg_ocorrencias') }} staging

    left join {{ ref('dim_categoria') }} categoria
        on md5(
            staging.tipo_acidente           || '-' || 
            staging.causa_acidente          || '-' || 
            staging.classificacao_acidente
        ) = categoria.sk_categoria

    left join {{ ref('dim_clima') }} clima
        on md5(
            staging.condicao_metereologica
        ) = clima.sk_clima

    left join {{ ref('dim_local') }} local 
        on md5(
            cast(staging.br as varchar)     || '-' || 
            cast(staging.km as varchar)     || '-' || 
            staging.sentido                 || '-' ||
            staging.uf_sigla                || '-' || 
            staging.municipio               || '-' || 
            staging.tipo_area
        ) = local.sk_local

    left join {{ ref('dim_tempo') }} tempo 
        on md5(
            cast(staging.data as varchar)   || '-' || 
            staging.fase_dia
        ) = tempo.sk_tempo
)

select * from fact

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} 
        where {{ this }}.id = fact.id
    )
{% endif %}