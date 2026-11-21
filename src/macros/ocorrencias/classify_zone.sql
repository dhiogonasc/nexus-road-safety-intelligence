{% macro classify_zone(used_ground) %}
    {% set value = normalize_txt_value(used_ground) %}
    case 
        when {{ value }} in ('não', 'rural') then 'rural'
        when {{ value }} in ('sim', 'urbano') then 'urbano'
        else 'não informado'
    end
{% endmacro %}