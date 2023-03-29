select
  step.name,
  countif(step.b) as value,
  lag(countif(step.b), 1) over (order by any_value(step.idx)) as value_prev,
  first_value(countif(step.b)) over (order by any_value(step.idx)) as value_init,
  any_value(step.idx) as idx,
from (
  select
    user_id,
    [
      {%- for step in funnel.list_steps() %}
      struct({{ loop.index }} as idx, '{{ step.name }}' as name, logical_or(event_name = '{{ step.name }}') as b){% if not loop.last %},{% endif %}
      {%- endfor %}
    ] as steps,
  from (
    {%- for step in funnel.list_steps() %}
    select user_id, '{{ step.name }}' as event_name, from {{ step.get_table_id() }}
    {% if not loop.last %}union all{% endif %}
    {%- endfor %}
  )
  group by
    user_id
)
, unnest(steps) as step
group by
  name
having
  name is not null
order by
  any_value(step.idx)
