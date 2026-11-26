{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

with staging as (
    select distinct
        id_ocorrencia,

        classificacao_acidente,
        condicao_metereologica,
        uf, 
        br,
        tipo_area,
        data,

        total_envolvidos,
        total_mortos
    from {{ ref('stg_ocorrencias') }}
),

fact as (
    select
        md5(cast(staging.id_ocorrencia as varchar)) as id,

        categoria.sk_categoria,
        clima.sk_clima,
        local.sk_local,
        tempo.sk_tempo,
        
        staging.total_envolvidos,
        staging.total_mortos
    from staging

    join {{ ref('dim_categoria') }} as categoria 
        on staging.classificacao_acidente = categoria.classificacao_acidente

    join {{ ref('dim_clima') }} as clima 
        on staging.condicao_metereologica = clima.condicao_metereologica

    join {{ ref('dim_local') }} as local 
        on staging.uf = local.uf
       and staging.br = local.br
       and staging.tipo_area = local.tipo_area

    join {{ ref('dim_tempo') }} as tempo 
        on staging.data = tempo.data
)

select * from fact

{% if is_incremental() %}
    where not exists (
        select 1 from {{ this }} as this
        where this.id = fact.id
    )
{% endif %}
