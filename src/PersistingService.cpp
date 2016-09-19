#include "PersistingService.h"

void PersistingService::Load()
{
    std::string fileName = get("fileName", "").asString();
    if(fileName == "") {
        return;
    }
    
    std::ifstream file(fileName);
    if(file.is_open()) {
        long int length = 0;
        file.seekg(0, file.end);
        length = file.tellg();
        file.seekg(0, file.beg);
        
        char *buffer = new char[length + 1];
        buffer[length] = 0;
        
        file.read(buffer, length);
        
        Json::Reader reader;
        bool successful = reader.parse(buffer, *this);
        if(!successful) {
            std::string json(buffer);
            delete[] buffer;
            file.close();
            throw SerializableException("Failed to parse JSON: (" + json + ")");
        }
        
        delete[] buffer;
        file.close();
    } else {
        throw SerializableException("Failed to open file: (" + fileName + ")");
    }
}

void PersistingService::Save()
{
    std::string fileName = get("fileName", "").asString();
    if(fileName == "") {
        return;
    }
    
    std::ofstream file(fileName);
    if(file.is_open()) {
        std::string json = Serialize();
        file.write(json.c_str(), (long int) json.size());
        file.close();
    } else {
        throw SerializableException("Failed to open file: (" + fileName + ")");
    }
}

PersistingService PersistingService::LoadFromFile(std::string fileName)
{
    PersistingService service (fileName);
    service.Load();
    return service;
}