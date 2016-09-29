#ifndef TYPE_CHECK_TEMPLATES_H_
#define TYPE_CHECK_TEMPLATES_H_

#include <vector>
#include <string>

namespace jsonserializer::structures
{
    // check for "primitives"
    template <typename T> const bool isPrimitive =  std::is_same<T, int>::value || 
                                                std::is_same<T, float>::value ||
                                                std::is_same<T, bool>::value ||
                                                std::is_same<T, long>::value ||
                                                std::is_same<T, std::string>::value;
                                                
    // check for vector
    template <typename T>             const bool isVector = false;
    template <typename T, typename U> const bool isVector<std::vector<T, U>> = true;

    template <typename T> const bool isKnownStructure = false;
}
#endif // TYPE_CHECK_TEMPLATES_H_