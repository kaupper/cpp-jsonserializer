#include "{{header}}"

using namespace {{namespace}};

template <typename T> T *deepCopyPointer(T *pointer) {
    if (pointer == nullptr) {
        return nullptr;
    }
    return new T(*pointer);
}

{% for struct in structures %}
static {{struct.name}} &copy({{struct.name}} &lhs, const {{struct.name}} &rhs)
{
    {%- for field in struct.fields %}
    lhs.{{field.name}} = deepCopyPointer(rhs.{{field.name}});
    {%- endfor %}
    return lhs;
}
{%- endfor %}


{% for struct in structures -%}
{{struct.name}}::{{struct.name}}()
{
    {%- for field in struct.fields %}
    {{field.name}} = nullptr;
    {%- endfor %}
}

{{struct.name}}::~{{struct.name}}()
{
    {%- for field in struct.fields %}
    delete {{field.name}}; {{field.name}} = nullptr;
    {%- endfor %}
}

{{struct.name}}::{{struct.name}}(const {{struct.name}} &src) : {{struct.name}}()
{
    copy(*this, src);
}

{{struct.name}} &{{struct.name}}::operator =(const {{struct.name}} &src)
{
    return copy(*this, src);
}

{% set requiredFields = struct.fields | selectattr("required") | list -%}
{%- if struct.fields | length !=  requiredFields | length and requiredFields | length != 0 %}
{{struct.name}}::{{struct.name}}(
{%- for field in requiredFields -%}
{% if field != (requiredFields | last) %}
    const {{field.type}} &{{field.name}},
{%- else %}
    const {{field.type}} &{{field.name}}
{%- endif %}
{%- endfor %}
)
{
{%- for field in struct.fields -%}
{% if field.required %}
    this->{{field.name}} = new {{field.type}}({{field.name}});
{%- endif %}
{%- endfor %}
}
{%- endif %}

{%- if struct.fields | length !=  0 %}
{{struct.name}}::{{struct.name}}(
{%- for field in struct.fields -%}
{% if field != (struct.fields | last) %}
    const {{field.type}} &{{field.name}},
{%- else %}
    const {{field.type}} &{{field.name}}
{%- endif %}
{%- endfor %}
)
{
{%- for field in struct.fields %}
    this->{{field.name}} = new {{field.type}}({{field.name}});
{%- endfor %}
}
{%- endif %}

{% for field in struct.fields -%}
{{field.type}} *{{struct.name}}::Get{{field.ccName}}()
{
    if ({{field.name}} == nullptr) {
        {{field.name}} = new {{field.type}};
    }
    return {{field.name}}; 
}

{{field.type}} &{{struct.name}}::Get{{field.ccName}}Value() const
{
    return *{{field.name}}; 
}

{% endfor %}
{% endfor %}