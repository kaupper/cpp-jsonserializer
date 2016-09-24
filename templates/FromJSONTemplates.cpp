#include "StructConverter.h"

using namespace jsonserializer;
using namespace jsonserializer::structures;

#include <iostream>

// convert "primitives"
template <typename T> static T fromString(const std::string &string);
template <> int fromString(const std::string &string) { return std::stoi(string); }
template <> long fromString(const std::string &string) { return std::stol(string); }
template <> float fromString(const std::string &string) { return std::stof(string); }
template <> std::string fromString(const std::string &string) { return std::string(string); }
template <> bool fromString(const std::string &string) { return (string == "true"); }

// create primitives
template <typename T> 
static typename std::enable_if<isPrimitive<T>, T>::type CREATE(const Serializable &value) {
    return fromString<T>(value.asString());
}

// create instance of generated data structure
template <typename T> 
static typename std::enable_if<isSomethingElse<T>, T>::type CREATE(const Serializable &value) {
    return Converter::FromJSON<T>(value);
}

// we may have a vector as type as well (so, create it)
template <typename T>
static typename std::enable_if<isVector<T>, T>::type CREATE(const Serializable &value) {
    T obj;
    for(unsigned int i = 0; i < value.size(); i++) {
        obj.push_back(CREATE<typename T::value_type>(value[i]));
    }
    return obj;
}

// create pointers from objects and set them
template <typename T> 
static void SET(const Json::Value &value, T *&obj) {
    obj = new T(CREATE<T>(value));
}


// required fields
template <typename T> 
static void REQ(const Serializable &s, const std::string &jsonKey, T *&obj) {
    if(false) {
        obj = new T(Converter::FromJSON<T>(s)); 
    } else {
	auto &tmp = s[jsonKey];
	if(tmp.isNull()) {
	    throw SerializableException("Required argument \"" + jsonKey + "\" is missing!");
	}
	SET(tmp, obj);
    }
}

// optional fields
template <typename T>
static void _OPT(const Serializable &s, const std::string &jsonKey, T *&obj) {
    auto &tmp = s[jsonKey];
    if(!tmp.isNull()) {
        SET(tmp, obj);
    }
}

template <typename T> 
static typename std::enable_if<isSomethingElse<T>, void>::type OPT(const Serializable &s, const std::string &jsonKey, T *&obj) {
    if(T::__transient) {
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
static typename std::enable_if<!isSomethingElse<T>, void>::type OPT(const Serializable &s, const std::string &jsonKey, T *&obj)
{
    _OPT(s, jsonKey, obj);
}

