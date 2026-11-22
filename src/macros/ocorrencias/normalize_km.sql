{% macro normalize_km(value) %}
    coalesce(
        try_cast(
            nullif(replace(
                trim(cast({{ value }} as varchar)), 
            ',', '.'), '(null)') 
        as decimal(8, 3)), 
    0.0)
{% endmacro %}