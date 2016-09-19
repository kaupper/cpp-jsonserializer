#ifndef PERSISTING_SERVICE_H_
#define PERSISTING_SERVICE_H_

#include <iostream>
#include <fstream>

#include "PersistingException.h"
#include "Serializable.h"

class PersistingService : public Serializable
{
public:
    static std::shared_ptr<PersistingService> LoadFromFile(std::string fileName);
        
    PersistingService() { }
    PersistingService(std::string fileName) : PersistingService() { (*this)["fileName"] = fileName; } 


    void Load();
    void Save();

    void SetFileName(std::string fileName) { (*this)["fileName"] = fileName; }
    std::string GetFileName() { return get("fileName", "").asString(); }
};

#endif // PERSISTING_SERVICE_H_
