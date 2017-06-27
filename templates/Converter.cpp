#include "{{header}}"

#include "ToJSONTemplates.cpp"
#include "FromJSONTemplates.cpp"

using namespace {{namespace}};


namespace jsonserializer
{
{%- for struct in structures %}
    template <> json Converter::ToJSON(const {{struct.name}} &obj)
    {
        json j;
{%- for field in struct.fields %}
{%- if field.required %}
        REQ(j, "{{field.jsonname}}", obj.{{field.name}});
{%- else %}
        OPT(j, "{{field.jsonname}}", obj.{{field.name}});
{%- endif %}
{%- endfor %}
        return j;
    }

    template <> {{struct.name}} Converter::FromJSON(const json &j)
    {
        {{struct.name}} obj;
{%- for field in struct.fields %}
{%- if field.required %}
        REQ(j, "{{field.jsonname}}", obj.{{field.name}});
{%- else %}
        OPT(j, "{{field.jsonname}}", obj.{{field.name}});
{%- endif %}
{%- endfor %}
        return obj;
    }
{% endfor -%}
}