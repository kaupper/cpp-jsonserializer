#ifndef CONVERTER_TEMPLATE_DEFINITIONS_H_
#define CONVERTER_TEMPLATE_DEFINITIONS_H_

#include "StructConverter.h"

namespace jsonserializer::structures
{
   /* template <typename T> Serializable Converter::ToJSON(const std::vector<T> &obj) 
    { 
        Serializable json(Json::arrayValue);
        for(unsigned int i = 0; i < obj.size(); i++) {
            json[i] = ToJSON<T>(obj.at(i));
        }
        return json; 
    }
    
    template <typename T> Serializable Converter::ToJSON(const T *obj) 
    { 
        return ToJSON(*obj); 
    }
  
  
    template <typename T> 
    typename std::enable_if<isVector<T>, T>::type Converter::FromJSON(const Serializable &json) 
    {
        T vector;
        for(auto &e : json) {
            vector.push_back(FromJSON<typename T::value_type>(e));
        }
        return vector;
    }*/
}

#endif // CONVERTER_TEMPLATE_DEFINITIONS_H_
