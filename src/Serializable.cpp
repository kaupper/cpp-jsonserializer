#include "Serializable.h"

using namespace jsonserializer;

std::string Serializable::Serialize() const
{
    Json::StyledWriter writer;
    std::string output = writer.write(*this);
    return output;
}

std::shared_ptr<Serializable> Serializable::Deserialize(const std::string& serializedString)
{
    Json::Value root;
    Json::Reader reader;
    bool parsingSuccessful = reader.parse(serializedString, root);
    
    if(!parsingSuccessful) {
        return nullptr;
        throw SerializableException("Deserializing failed! JSON string has bad format!");
    }

    return std::make_shared<Serializable>(root);
}