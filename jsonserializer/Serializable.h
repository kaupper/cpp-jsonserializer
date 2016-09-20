#ifndef SERIALIZABLE_H_
#define SERIALIZABLE_H_

#include <iostream>
#include <map>
#include <string>
#include <memory>

#include "json/json.h"

#include "SerializableException.h"

namespace jsonserializer
{
    class Serializable : public Json::Value
    {
    public:
        static Serializable Deserialize(const std::string& serializedString);
        
        Serializable(const Json::Value& json) : Serializable()
        {
            Json::Value v(json);
            this->swap(v);
        }
        
        Serializable() : Json::Value() {}
        std::string Serialize() const;   
    };
}

#endif // SERIALIZABLE_H_
