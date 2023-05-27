{% macro line_chart_step_wise_conversion(event_name1, event_name2, date1, date2) %}

with

event as (

-- 두 event 를 union 하고,

select
  _date,
  user_id,
  '{{ event_name1 }}' as event_name,
  created_at,
from
  event.{{ event_name1 }}

union all

select
  _date,
  user_id,
  '{{ event_name2 }}' as event_name,
  created_at,
from
  event.{{ event_name2 }}

)

, event_augmented as (

-- 직후 event name 을 달고,

select
  _date,
  user_id,
  event_name,
  lead(event_name, 1) over (partition by user_id order by created_at) as event_name_next,
from
  event

)

, aggregated_by_date_and_user as (

-- date, user 에 대해 aggregate 하고,

select
  _date,
  user_id,
  logical_or(event_name_next = '{{ event_name2 }}') as is_converted,
from
  event_augmented
where
  event_name = '{{ event_name1 }}'
  and _date between '{{ date1 }}' and '{{ date2 }}'
group by
  _date, user_id

)

select
  _date,
  countif(is_converted) / count(1) as value,
from
  aggregated_by_date_and_user
group by
  _date

{% endmacro %}
