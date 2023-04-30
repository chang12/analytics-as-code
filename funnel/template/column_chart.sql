select
  step.name,
  countif(step.b) as value,
  lag(countif(step.b), 1) over (order by any_value(step.idx)) as value_prev,
  first_value(countif(step.b)) over (order by any_value(step.idx)) as value_init,
  any_value(step.idx) as idx,
from (
  select
    {{ entity }},
    [
      {%- for step in steps %}
      struct({{ loop.index }} as idx, '{{ step.name }}' as name, logical_or(event_name = '{{ step.name }}') as b){% if not loop.last %},{% endif %}
      {%- endfor %}
    ] as steps,
  from (
    {%- for step in steps %}
    select {{ entity }}, '{{ step.name }}' as event_name, from {{ step.get_table_id() }} where _date between '{{ date_s }}' and '{{ date_e }}'
    {% if not loop.last %}union all{% endif %}
    {%- endfor %}
  )
  group by
    {{ entity }}
)
, unnest(steps) as step
group by
  name
order by
  any_value(step.idx)
