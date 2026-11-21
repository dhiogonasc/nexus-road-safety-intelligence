{% macro transcript_br(br) %}
    {% set value = normalize_txt_value(br) %}
    case
        when {{ value }} = 'não informado' then 'não informado'
        else 'br-' || lpad(regexp_replace({{ value }}, '[^\d]', '', 'g'), 3, '0')
    end
{% endmacro %}