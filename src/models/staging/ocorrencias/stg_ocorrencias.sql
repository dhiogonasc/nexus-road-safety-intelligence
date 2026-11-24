{{ config(materialized='table') }}

with raw as (
    select *
    from read_csv_auto(
        '{{ var("raw_ocorrencias_csv_path") }}',
        encoding='ISO-8859-1',
        delim=';',
        header=true,
        all_varchar=true,
        union_by_name=true
    )
),

normalized as (
    select
        try_cast(id as bigint) as id_ocorrencia,

        {{ normalize_txt_value('uf') }} as uf,
        {{ normalize_txt_value('classificacao_acidente') }} as classificacao_acidente,
        {{ normalize_txt_value('condicao_metereologica') }} as clima_norm,
        {{ normalize_txt_value('br') }} as br_norm,
        {{ normalize_txt_value('uso_solo') }} as area_norm,

        coalesce(
            try_cast(try_strptime(data_inversa, '%Y-%m-%d') as date),
            try_cast(try_strptime(
                case 
                    when data_inversa LIKE '%/16' then regexp_replace(data_inversa, '/16$', '/2016') 
                    else data_inversa 
                end, 
                '%d/%m/%Y'
            ) as date)
        ) as data,

        try_cast(coalesce(pessoas, '0') as integer) as total_envolvidos,
        try_cast(coalesce(mortos, '0') as integer) as total_mortos
    from raw
),

staging as (
    select
        id_ocorrencia,
        uf,
        classificacao_acidente,

        case
            when clima_norm in ('céu claro', 'ceu claro') then 'céu claro'
            when clima_norm in ('ignorado', 'ignorada') then 'ignorado'
            else clima_norm
        end as condicao_metereologica,

        case
            when br_norm = 'não informado' then 'não informado'
            else 'br-' || lpad(regexp_replace(br_norm, '[^\d]', '', 'g'), 3, '0')
        end as br,

        case
            when area_norm in ('não', 'rural') then 'rural'
            when area_norm in ('sim', 'urbano') then 'urbano'
            else 'não informado'
        end as tipo_area,

        data,
        total_envolvidos,
        total_mortos
    from normalized
    where id_ocorrencia is not null

    qualify row_number() over (
        partition by id_ocorrencia
        order by total_mortos desc, total_envolvidos desc
    ) = 1
)

select * from staging