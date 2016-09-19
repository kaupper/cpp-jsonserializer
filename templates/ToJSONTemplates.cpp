#include "StructConverter.h"

using namespace jsonserializer::structures;

// templates to make conversion code more readable
template <typename T> 
static typename std::enable_if<isPrimitive<T>, void>::type SET(Serializable &s, std::string &jsonKey, const T *obj) {
    s[jsonKey] = *(obj);
}

template <typename T> 
static typename std::enable_if<!isPrimitive<T>, void>::type SET(Serializable &s, std::string &jsonKey, const T *obj) {
    s[jsonKey] = Converter::ToJSON(obj);
}

template <typename T> 
static void REQ(Serializable &s, std::string &&jsonKey, const T *obj) {
    if(obj == nullptr) {
        throw SerializableException("Required argument \"" + jsonKey + "\" is missing!");
    }
    SET(s, jsonKey, obj);
}

template <typename T> 
static void OPT(Serializable &s, std::string &&jsonKey, const T *obj) {
    if(obj != nullptr) {
        SET(s, jsonKey, obj);
    }
}