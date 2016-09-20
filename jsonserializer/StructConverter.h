#ifndef TELEGRAM_BOT_JSON_CONVERTER_H_
#define TELEGRAM_BOT_JSON_CONVERTER_H_

#include "Serializable.h"

namespace jsonserializer::structures
{
    
    // check for "primitives"
    template <typename T> const bool isPrimitive =  std::is_same<T, int>::value || 
                                                std::is_same<T, float>::value ||
                                                std::is_same<T, bool>::value ||
                                                std::is_same<T, std::string>::value;
                                                
    // check for vector
    template <typename T> struct _isVector { static const bool value = false; };
    template <typename T, typename Alloc> struct _isVector<std::vector<T,Alloc> > { static const bool value = true; };
    template <typename T> const bool isVector = _isVector<T>::value;
    
    template <typename T> const bool isSomethingElse = !isPrimitive<T> && !isVector<T>;
    
    class Converter
    {    
    public:
        // to JSON templates
        template <typename T> 
        static typename std::enable_if<!isVector<T>, Serializable>::type ToJSON(const T &obj);
              
        template<typename T> 
        static typename std::enable_if<isVector<T>, Serializable>::type ToJSON(const T &obj) { 
            Serializable json(Json::arrayValue);
            for(unsigned int i = 0; i < obj.size(); i++) {
                json[i] = ToJSON<typename T::value_type>(obj.at(i));
            }
            return json; 
        }
        
        template<typename T> 
        static typename std::enable_if<!isVector<T>, Serializable>::type ToJSON(const T *obj) { 
            return ToJSON(*obj); 
        }
        
        template<typename T>
        static typename std::enable_if<isVector<T>, Serializable>::type ToJSON(const T *obj) { 
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

#endif // TELEGRAM_BOT_JSON_CONVERTER_H_
