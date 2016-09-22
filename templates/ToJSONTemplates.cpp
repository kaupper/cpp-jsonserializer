#include "StructConverter.h"

using namespace jsonserializer;
using namespace jsonserializer::structures;

// templates to make conversion code more readable
template <typename T> 
static typename std::enable_if<isPrimitive<T>, void>::type SET(Serializable &s, const std::string &jsonKey, const T *const obj) {
    s[jsonKey] = *(obj);
}

template <typename T> 
static typename std::enable_if<!isPrimitive<T>, void>::type SET(Serializable &s, const std::string &jsonKey, const T *const obj) {
    s[jsonKey] = Converter::ToJSON(obj);
}

template <typename T> 
static void REQ(Serializable &s, const std::string &jsonKey, const T *const obj) {
    if(obj == nullptr) {
        throw SerializableException("Required argument \"" + jsonKey + "\" is missing!");
    }
    SET(s, jsonKey, obj);
}

template <typename T> 
static void OPT(Serializable &s, const std::string &jsonKey, const T *const obj) {
    if(obj != nullptr) {
        SET(s, jsonKey, obj);
    }
}