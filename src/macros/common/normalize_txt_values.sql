{% macro normalize_txt_value(value) %}
    case  
        when {{ value }} 
            is null 
            or lower(trim(cast({{ value }} as varchar))) in ('na', 'n/a', 'nan', 'null', '(null)', 'none', '-', '') 
                then 'não informado'
        else  
            regexp_replace(
                regexp_replace(
                    lower(trim(cast({{ value }} as varchar))),  
                    '[\s\-_/,]+', ' ', 'g'
                ),  
                '[^\p{L}\p{N}\s]', '', 'g'
            )
    end
{% endmacro %}