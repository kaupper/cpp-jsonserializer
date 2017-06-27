{% set guard = namespace.replace('::', '_') -%}
#ifndef {{ guard | upper }}_CONVERTER_H
#define {{ guard | upper }}_CONVERTER_H

#include "{{header}}"

#endif