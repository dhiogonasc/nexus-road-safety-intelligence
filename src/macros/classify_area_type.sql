{% macro classify_area_type(type) %}
    case {{ normalize_txt_value(type) }}
        when 'nao' then 'rural'
        when 'sim' then 'urbano'
        else 'nao informado'
    end
{% endmacro %}