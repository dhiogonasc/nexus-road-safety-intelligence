{% macro transcript_month_number(date_column) %}
    case extract(month from {{ date_column }})
        when 1 then 'janeiro'
        when 2 then 'fevereiro'
        when 3 then 'março'
        when 4 then 'abril'
        when 5 then 'maio'
        when 6 then 'junho'
        when 7 then 'julho'
        when 8 then 'agosto'
        when 9 then 'setembro'
        when 10 then 'outubro'
        when 11 then 'novembro'
        when 12 then 'dezembro'
        else 'não informado'
    end
{% endmacro %}