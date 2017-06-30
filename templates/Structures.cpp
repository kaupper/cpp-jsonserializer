#include "{{header}}"

using namespace {{namespace}};

template <typename T> T *deepCopyPointer(T *pointer) {
    if (pointer == nullptr) {
        return nullptr;
    }
    return new T(*pointer);
}


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
    {%- for field in struct.fields %}
    {{field.name}} = deepCopyPointer(src.{{field.name}});
    {%- endfor %}
}

{{struct.name}} &{{struct.name}}::operator =(const {{struct.name}} &src)
{
    {%- for field in struct.fields %}
    {{field.name}} = deepCopyPointer(src.{{field.name}});
    {%- endfor %}
    return *this;
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
{{field.type}} *{{struct.name}}::Get{{field.ccName}}() const
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

void {{struct.name}}::Set{{field.ccName}}(const {{field.type}} &new{{field.name}})
{
    if({{field.name}} != nullptr) {
        delete {{field.name}};
    }
    {{field.name}} = new {{field.type}}(new{{field.name}});
}

bool {{struct.name}}::Has{{field.ccName}}() const
{
    return {{field.name}} != nullptr;
}


{% endfor %}
{% endfor %}