#ifndef CONVERTER_EXCEPTION_H
#define CONVERTER_EXCEPTION_H

#include <string>
#include <exception>
#include <stdexcept>


namespace jsonserializer
{
    class ConverterException : public std::runtime_error
    {
    public:
        ConverterException(std::string message) : std::runtime_error(message) {}
    };
}

#endif // CONVERTER_EXCEPTION_H