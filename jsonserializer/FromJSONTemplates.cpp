#include "StructConverter.h"

using namespace jsonserializer;


// convert "primitives"
template <typename T> static T fromString(const std::string &string);
template <> int fromString(const std::string &string)
{
    return std::stoi(string);
}

template <> long fromString(const std::string &string)
{
    return std::stol(string);
}

template <> float fromString(const std::string &string)
{
    return std::stof(string);
}

template <> double fromString(const std::string &string)
{
    return std::stod(string);
}

template <> std::string fromString(const std::string &string)
{
    return string.substr(1, string.size() - 2);
}

template <> bool fromString(const std::string &string)
{
    std::string tmp;
    std::transform(string.cbegin(), string.cend(), std::back_inserter(tmp), ::tolower);
    return (tmp == "true");
}


// create primitives
template <typename T>
static typename std::enable_if<isPrimitive<T>, T>::type 
CREATE(const json &value)
{
    return fromString<T>(value.dump());
}

// create instance of generated data structure
template <typename T>
static typename std::enable_if<isKnownStructure<T>, T>::type 
CREATE(const json &value)
{
    return Converter::FromJSON<T>(value);
}

// we may have a vector as type as well (so, create it)
template <typename T>
static typename std::enable_if<isVector<T>, T>::type 
CREATE(const json &value)
{
    T obj;
    
    for (unsigned int i = 0; i < value.size(); i++) {
        obj.push_back(CREATE<typename T::value_type>(value[i]));
    }
    
    return obj;
}

// create pointers from objects and set them
template <typename T>
static void 
SET(const json &value, T *&obj)
{
    obj = new T(CREATE<T>(value));
}

// required fields
template <typename T>
static void 
_REQ(const json &j, const std::string &jsonKey, T *&obj)
{
    if (j.find(jsonKey) == j.end()) {
        throw ConverterException("Required argument \"" + jsonKey +
                                    "\" is missing!");
    }
    
    SET(j[jsonKey], obj);
}

template <typename T>
static typename std::enable_if<isKnownStructure<T>, void>::type 
REQ(const json &s, const std::string &jsonKey, T *&obj)
{
    if (T::__transient) {
        obj = new T(Converter::FromJSON<T>(s));
    } else {
        _REQ(s, jsonKey, obj);
    }
}

template <typename T>
static typename std::enable_if<!isKnownStructure<T>, void>::type 
REQ(const json &s, const std::string &jsonKey, T *&obj)
{
    _REQ(s, jsonKey, obj);
}

// optional fields
template <typename T>
static void 
_OPT(const json &j, const std::string &jsonKey, T *&obj)
{
    if(j.find(jsonKey) != j.end()) {
        SET(j[jsonKey], obj);
    }
}

template <typename T>
static typename std::enable_if<isKnownStructure<T>, void>::type 
OPT(const json &s, const std::string &jsonKey, T *&obj)
{
    if (T::__transient) {
        try {
            obj = new T(Converter::FromJSON<T>(s));
        } catch (...) {
            // nothing to be done
        }
    } else {
        _OPT(s, jsonKey, obj);
    }
}

template <typename T>
static typename std::enable_if<!isKnownStructure<T>, void>::type 
OPT(const json &s, const std::string &jsonKey, T *&obj)
{
    _OPT(s, jsonKey, obj);
}

