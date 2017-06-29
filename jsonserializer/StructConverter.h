#ifndef STRUCT_CONVERTER_H
#define STRUCT_CONVERTER_H

#include <algorithm>

#include "json.h"

#include "ConverterException.h"
#include "TypeCheckTemplates.h"


namespace jsonserializer
{
    class Converter
    {
        public:
            // to JSON templates
            template <typename T, typename = typename std::enable_if<not isVector<T>, json>::type>
            static json ToJSON(const T &obj);
            
            template <typename T>
            static typename std::enable_if<isVector<T>, json>::type ToJSON(const T &obj);
            
            template <typename T>
            static json ToJSON(const T *obj);
            
            
            // from JSON templates
            template<typename T, typename = typename std::enable_if<not isVector<T>, T>::type>
            static T FromJSON(const json &json);
            
            template<typename T>
            static typename std::enable_if<isVector<T>, T>::type FromJSON(const json &json);
    };
    
    template <typename T> typename std::enable_if<isVector<T>, json>::type
    Converter::ToJSON(const T &obj)
    {
        json json = json::array();
        
        for (unsigned int i = 0; i < obj.size(); i++) {
            json[i] = ToJSON<typename T::value_type>(obj.at(i));
        }
        
        return json;
    }
    
    template <typename T> json
    Converter::ToJSON(const T *obj)
    {
        return ToJSON(*obj);
    }
    
    template<typename T> typename std::enable_if<isVector<T>, T>::type
    Converter::FromJSON(const json &json)
    {
        T vector;
        
        for (auto &e : json) {
            vector.push_back(FromJSON<typename T::value_type>(e));
        }
        
        return vector;
    }
}

#endif // STRUCT_CONVERTER_H
