{% macro classify_area_type(type) %}
    case {{ normalize_txt_value(type) }}
        when 'não' then 'rural'
        when 'sim' then 'urbano'
        else 'não informado'
    end
{% endmacro %}