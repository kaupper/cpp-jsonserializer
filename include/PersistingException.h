#ifndef SKYFORGE_EXCEPTION_H_
#define SKYFORGE_EXCEPTION_H_

#include <string>
#include <exception>
#include <stdexcept>

class PersistingException : public std::runtime_error
{
public:
    PersistingException(std::string message) : std::runtime_error(message) {}
};

#endif // SKYFORGE_EXCEPTION_H_