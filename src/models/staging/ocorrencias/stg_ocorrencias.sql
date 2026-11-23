{{ config(materialized='table') }}

with raw as (
    select * 
    from read_csv_auto(
        '{{ var("raw_ocorrencias_csv_path") }}', 
        delim = ';', 
        encoding='ISO-8859-1',
        header = true, 
        all_varchar=true,
        union_by_name=true,
    )
),

staging as (
    select
        try_cast(id as bigint) as id_ocorrencia,
        
        {{ normalize_txt_value('tipo_acidente') }} as tipo_acidente,
        {{ normalize_txt_value('causa_acidente') }} as causa_acidente,
        {{ normalize_txt_value('classificacao_acidente') }} as classificacao_acidente,

        {{ normalize_txt_value('condicao_metereologica') }} as condicao_metereologica,

        {{ transcript_br('br') }} as br,
        {{ normalize_km('km') }} as km,
        {{ normalize_txt_value('sentido_via') }} as sentido_via,
        {{ normalize_txt_value('tipo_pista') }} as tipo_pista,

        {{ normalize_txt_value('uf') }} as uf,
        {{ classify_zone('uso_solo') }} as tipo_area,

        coalesce(
            try_cast(try_strptime(data_inversa, '%d/%m/%Y') as date),
            try_cast(try_strptime(data_inversa, '%Y-%m-%d') as date),
            try_cast(data_inversa as date)
        ) as data,
        {{ normalize_txt_value('fase_dia') }} as fase_dia,
        
        try_cast(coalesce(pessoas, '0') as integer) as total_envolvidos,
        try_cast(coalesce(ilesos, '0') as integer) as total_ilesos,
        try_cast(coalesce(mortos, '0') as integer) as total_mortos,
        try_cast(coalesce(feridos, '0') as integer) as total_feridos
    from raw

    qualify row_number() over (
        partition by id_ocorrencia
        order by 
            total_mortos desc, 
            total_envolvidos desc
    ) = 1
)

select * from staging