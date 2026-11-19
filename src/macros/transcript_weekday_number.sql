{% macro transcript_weekday_number(number) %}
    case {{ number }}
        when 1 then 'segunda-feira'
        when 2 then 'terca-feira'
        when 3 then 'quarta-feira'
        when 4 then 'quinta-feira'
        when 5 then 'sexta-feira'
        when 6 then 'sabado'
        when 7 then 'domingo'
        else 'nao informado'
    end
{% endmacro %}