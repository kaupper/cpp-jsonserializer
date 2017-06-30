#include "StructConverter.h"

using namespace jsonserializer;


// templates to make conversion code more readable
template <typename T>
static typename std::enable_if<isPrimitive<T>, void>::type
SET(json &j, const std::string &jsonKey, const T *const obj)
{
    j[jsonKey] = *obj;
}

template <typename T>
static typename std::enable_if<isKnownStructure<T>, void>::type
SET(json &j, const std::string &jsonKey, const T *const obj)
{
    auto json = Converter::ToJSON(obj);
    
    if (T::__transient) {
        for (auto it = json.begin(); it != json.end(); ++it) {
            if (j.find(it.key()) != j.end()) {
                throw ConverterException("Field \"" + it.key() + "\" does already exist!");
            }
            
            j[it.key()] = *it;
        }
    } else {
        j[jsonKey] = json;
    }
}

template <typename T>
static typename std::enable_if<isVector<T>, void>::type
SET(json &s, const std::string &jsonKey, const T *const obj)
{
    s[jsonKey] = Converter::ToJSON<T>(obj);
}

template <typename T>
static void
REQ(const T *const obj, const std::string &jsonKey, json &s)
{
    if (obj == nullptr) {
        throw ConverterException("Required field \"" + jsonKey + "\" is missing!");
    }
    
    SET(s, jsonKey, obj);
}

template <typename T>
static void
OPT(const T *const obj, const std::string &jsonKey, json &s)
{
    if (obj != nullptr) {
        SET(s, jsonKey, obj);
    }
}
