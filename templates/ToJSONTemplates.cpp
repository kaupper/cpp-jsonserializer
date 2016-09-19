#include "telegram/structures/StructConverter.h"

// templates to make conversion code more readable
template <typename T> 
static typename std::enable_if<telegram::structures::isPrimitive<T>, void>::type SET(Serializable &s, std::string &jsonKey, const T *obj) {
    s[jsonKey] = *(obj);
}

template <typename T> 
static typename std::enable_if<!telegram::structures::isPrimitive<T>, void>::type SET(Serializable &s, std::string &jsonKey, const T *obj) {
    s[jsonKey] = telegram::structures::Converter::ToJSON(obj);
}

template <typename T> 
static void REQ(Serializable &s, std::string &&jsonKey, const T *obj) {
    if(obj == nullptr) {
        throw telegram::TelegramException("Required argument \"" + jsonKey + "\" is missing!");
    }
    SET(s, jsonKey, obj);
}

template <typename T> 
static void OPT(Serializable &s, std::string &&jsonKey, const T *obj) {
    if(obj != nullptr) {
        SET(s, jsonKey, obj);
    }
}