{% macro classify_day_period(period) %}
    case {{ normalize_txt_value(period) }}
        when 'amanhecer' then 1
        when 'pleno dia' then 2
        when 'anoitecer' then 3
        when 'plena noite' then 4
        else 5
    end
{% endmacro %}