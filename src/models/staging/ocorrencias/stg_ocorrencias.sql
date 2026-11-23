{{ config(materialized='table') }}

with raw as (
    select * 
    from read_csv_auto(
        '{{ var("raw_ocorrencias_csv_path") }}', 
        encoding='ISO-8859-1',
        delim = ';', 
        header = true, 
        all_varchar=true,
        union_by_name=true,
    )
),

staging as (
    select
        try_cast(id as bigint) as id_ocorrencia,

        {{ normalize_txt_value('classificacao_acidente') }} as classificacao_acidente,
        {{ normalize_txt_value('condicao_metereologica') }} as condicao_metereologica,
        {{ normalize_txt_value('br') }} as br,
        {{ normalize_txt_value('uf') }} as uf,
        {{ normalize_txt_value('uso_solo') }} as tipo_area,

        coalesce(
            try_cast(try_strptime(data_inversa, '%d/%m/%Y') as date),
            try_cast(try_strptime(data_inversa, '%Y-%m-%d') as date),
            try_cast(data_inversa as date)
        ) as data,
        
        try_cast(coalesce(pessoas, '0') as integer) as total_envolvidos,
        try_cast(coalesce(mortos, '0') as integer) as total_mortos,
    from raw

    qualify row_number() over (
        partition by id_ocorrencia
        order by 
            total_mortos desc, 
            total_envolvidos desc
    ) = 1
)

select * from staging