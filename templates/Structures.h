{% set guard = namespace.replace('::', '_') -%}
#ifndef {{ guard | upper }}_H
#define {{ guard | upper }}_H

{% for inc in global_includes -%}
#include <{{inc}}> 
{% endfor %}
{% for inc in local_includes -%}
#include "{{inc}}"
{% endfor %}
#include "StructConverter.h"
#include "TypeCheckTemplates.h"


namespace {{namespace}}
{
{%- for struct in structures %}
    class {{struct.name}};
{%- endfor -%}

{% for struct in structures %}

    class {{struct.name}}
    {
        friend class jsonserializer::Converter;
        
{% for field in struct.fields %}
        mutable {{field.type}} *{{field.name}} = nullptr;
{%- endfor %}

    public:
        static const bool __transient = {{struct.transient | lower}};
        
        {{struct.name}}();
        ~{{struct.name}}();

        {{struct.name}}(const {{struct.name}} &);
        {{struct.name}} &operator =(const {{struct.name}} &);


{% set requiredFields = struct.fields | selectattr("required") | list -%}
{%- if struct.fields | length !=  requiredFields | length and requiredFields | length != 0 %}
        {{struct.name}}(
{%- for field in requiredFields -%}
{% if field != (requiredFields | last) %}
            const {{field.type}} &,
{%- else %}
            const {{field.type}} &
{%- endif %}
{%- endfor %}
        );
{%- endif %}

{% if struct.fields | length != 0 %}
        {{struct.name}}(
{%- for field in struct.fields %}
{%- if field != (struct.fields | last) %}
            const {{field.type}} &,
{%- else %}
            const {{field.type}} &
{%- endif %}
{%- endfor %}
        );
{%- endif %}

{% for field in struct.fields %}
        {{field.type}} *Get{{field.ccName}}() const;
        {{field.type}} &Get{{field.ccName}}Value() const;
        void Set{{field.ccName}}(const {{field.type}} &);
        bool Has{{field.ccName}}() const;
{%- endfor %}
    };
{%- endfor %}
}

namespace jsonserializer
{
{%- for struct in structures %}
    template <> const bool isKnownStructure<::{{namespace}}::{{struct.name}}> = true;
{% endfor -%}
}

#endif