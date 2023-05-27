{% import 'line_chart_step_wise_conversion.sql' as line_chart_step_wise_conversion %}

{% for (event_name1, event_name2) in event_name_pairs %}
  {% if not loop.first %}
union all
  {% endif %}
(

{{ line_chart_step_wise_conversion.line_chart_step_wise_conversion(event_name1, event_name2, date1, date2) }}

)
{% endfor %}
