#ifndef CONVERTER_H_
#define CONVERTER_H_

#include "Serializable.h"
#include "TypeCheckTemplates.h"

namespace jsonserializer::structures
{
    class Converter
    {    
    public:
        // to JSON templates
        template <typename T> 
        static typename std::enable_if<!isVector<T>, Serializable>::type ToJSON(const T &obj);
              
        template <typename T> 
        static typename std::enable_if<isVector<T>, Serializable>::type ToJSON(const T &obj) { 
            Serializable json(Json::arrayValue);
            for(unsigned int i = 0; i < obj.size(); i++) {
                json[i] = ToJSON<typename T::value_type>(obj.at(i));
            }
            return json; 
        }
        
        template<typename T> 
        static Serializable ToJSON(const T *obj) { 
            return ToJSON(*obj); 
        }
      
      
        // from JSON templates
        template <typename T, typename = typename std::enable_if<!isVector<T>, T>::type> 
        static T FromJSON(const Serializable &json);
        
        template <typename T> 
        static typename std::enable_if<isVector<T>, T>::type FromJSON(const Serializable &json) {
            T vector;
            for(auto &e : json) {
                vector.push_back(FromJSON<typename T::value_type>(e));
            }
            return vector;
        }
    };
}

#include "StructConverterTemplateDefinitions.h"

#endif // CONVERTER_H_
