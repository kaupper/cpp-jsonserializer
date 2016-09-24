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
    auto json = Converter::ToJSON(obj);
    if(T::__transient) {
        for(auto it = json.begin(); it != json.end(); ++it) {
	    if(s.isMember(it.name())) {
	        throw SerializableException("Field \"" + it.name() + "\" does already exist!");
	    }
	    s[it.name()] = (*it);
	}
    } else {
        s[jsonKey] = json;
    }
}

template <typename T> 
static void REQ(Serializable &s, const std::string &jsonKey, const T *const obj) {
    if(obj == nullptr) {
        throw SerializableException("Required field \"" + jsonKey + "\" is missing!");
    }
    SET(s, jsonKey, obj);
}

template <typename T> 
static void OPT(Serializable &s, const std::string &jsonKey, const T *const obj) {
    if(obj != nullptr) {
        SET(s, jsonKey, obj);
    }
}
