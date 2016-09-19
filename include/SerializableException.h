#ifndef SERIALIZABLE_EXCEPTION_H_
#define SERIALIZABLE_EXCEPTION_H_

#include <string>
#include <exception>
#include <stdexcept>

namespace jsonserializer
{
    class SerializableException : public std::runtime_error
    {
    public:
        SerializableException(std::string message) : std::runtime_error(message) {}
    };
}

#endif // SERIALIZABLE_EXCEPTION_H_