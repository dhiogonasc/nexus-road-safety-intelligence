{% macro classify_zone(used_ground) %}
    case {{ normalize_txt_value(used_ground) }}
        when 'não' then 'rural'
        when 'sim' then 'urbano'
        else 'não informado'
    end
{% endmacro %}