import os
import json
import shutil


path = os.path.dirname(os.path.abspath(__file__)) + "/"
filePath = path + "generated/"

def upper(s):
    l = list(s)
    l[0] = l[0].upper()
    return ''.join(l)

def generateHeader(file, deps):
    file = filePath + file
    prefix = """#ifndef TELEGRAM_BOT_DATA_STRUCTURES_H_
#define TELEGRAM_BOT_DATA_STRUCTURES_H_

#include <vector>
#include <string>
#include <map>

namespace telegram::structures
{
"""
   
    postfix = """
}

#endif // TELEGRAM_BOT_DATA_STRUCTURES_H_
"""
    tab = "    "
    linebreak = "\n"
    names = []
    buffer = []
    with open(file, "w") as f:
        f.write(prefix)
        with open(jsonFile) as data_file:    
            structures = json.load(data_file)

        
        for struct in structures:
            names.append(struct["name"])
            
            buff = "struct "
            buff = buff + struct["name"] + linebreak + tab + "{" + linebreak + tab + tab
            # constructor
            buff = buff + struct["name"] + "();" + linebreak + tab + tab
            # destructor
            buff = buff + "virtual ~" + struct["name"] + "();" + linebreak + tab + tab
            # copy constructor
            buff = buff + struct["name"] + "(const " + struct["name"] + " &);" + linebreak + tab + tab
            # assignment
            buff = buff + struct["name"] + " & operator=(const " + struct["name"] + " &);" + linebreak + tab + tab
            # move constructor
            buff = buff + struct["name"] + "(" + struct["name"] + " &&);" + linebreak + tab + tab
            # move assignment
            buff = buff + struct["name"] + " & operator=(" + struct["name"] + " &&);" + linebreak + tab + tab

            requiredCount = 0
            
            # constructor for required members
            if len(struct["fields"]) > 0:
                buff = buff + "%s(" % (struct["name"])
                first = True
                for field in struct["fields"]:
                    if field["required"] == "true":
                        requiredCount += 1
                        if not first:
                            buff = buff + ", " 
                        buff = buff + "%s %s" % (field["type"], field["cppName"])
                        first = False
                buff = buff + ");" + linebreak + tab 
 
            if requiredCount != len(struct["fields"]):
                # constructor for all members
                buff = buff + tab + "%s(" % (struct["name"])
                first = True
                for field in struct["fields"]:
                    if not first:
                        buff = buff + ", " 
                    buff = buff + "%s %s" % (field["type"], field["cppName"])
                    first = False
                buff = buff + ");" + linebreak + tab 

            if len(struct["fields"]) > 0:
                buff = buff + linebreak + tab
           
            # field definitions
            for field in struct["fields"]:
                buff = buff + tab + field["type"] + " *" + field["cppName"] + ";" + linebreak + tab
            
            buff = buff + linebreak + tab + tab + "std::map<std::string, void*> map;" + linebreak + linebreak + tab

            # getter and setter
            for field in struct["fields"]:
                n = field["cppName"]
                t = field["type"]
                buff = buff + tab + "%s * Get%s();" % (t, upper(n)) + linebreak + tab
                buff = buff + tab + "%s & Get%sValue();" % (t, upper(n)) + linebreak + tab

            buff = buff + "};"
            buffer.append(buff);
        
        for name in names:
            f.write(tab + "struct " + name + ";" + linebreak)
                
        for buff in buffer:
            f.write(linebreak + tab + buff + linebreak)
        
        f.write(postfix)
        
def generateImplementation(file, deps):
    file = filePath + file
    includes = ""
    for d  in deps:
        includes = includes + "#include \"%s\"\n" % (d) 
    
    prefix = includes + "\n"
    prefix = prefix + """using namespace telegram::structures;

template <typename T> T * deepCopyPointer(T * pointer) {
    if (pointer == nullptr) {
        return nullptr;
    }
    return new T(*pointer);
}

"""
    postfix = ""
    
    tab = "    "
    linebreak = "\n"
    with open(file, "w") as f:
        f.write(prefix)
        
        with open(jsonFile) as data_file:    
            structures = json.load(data_file)

        # generate copy functions
        for struct in structures:
            buff = "static " + struct["name"] + " & copy(" + struct["name"] + " &lhs, const " + struct["name"] + " &rhs)" + linebreak
            buff = buff + "{" + linebreak
            for field in struct["fields"]:
                buff = buff + tab + "lhs." + field["cppName"] + " = deepCopyPointer(rhs." + field["cppName"] + ");" + linebreak
            buff = buff + tab + "return lhs;" + linebreak
            buff = buff + "}" + linebreak + linebreak
            f.write(buff)
            
        # generate move functions
        for struct in structures:
            buff = "static %s & move(%s &lhs, %s &rhs)" % (struct["name"], struct["name"], struct["name"]) + linebreak
            buff = buff + "{" + linebreak
            for field in struct["fields"]:
                #buff = buff + tab + "delete lhs.%s;\n lhs.%s = std::move(rhs.%s);\n rhs.%s = nullptr;" % (field["cppName"], field["cppName"], field["cppName"], field["cppName"]) + linebreak
                buff = buff + tab + "std::swap(lhs.%s, rhs.%s);" % (field["cppName"], field["cppName"]) + linebreak
            buff = buff + tab + "return lhs;" + linebreak
            buff = buff + "}" + linebreak + linebreak
            f.write(buff)
            
        # generate constructors etc
        for struct in structures:
            n = struct["name"]
            
            # constructor
            buff = "%s::%s()" % (n, n) + linebreak
            buff = buff + "{" + linebreak
            for field in struct["fields"]:
                fi = field["cppName"]
                buff = buff + tab + fi + " = nullptr;"+ linebreak
            buff = buff + "}" + linebreak + linebreak
            
            # destructor
            buff = buff + "%s::~%s()" % (n, n) + linebreak
            buff = buff + "{" + linebreak
            for field in struct["fields"]:
                fi = field["cppName"]
                buff = buff + tab + "delete %s; %s = nullptr;" % (fi, fi) + linebreak
                buff = buff + tab + "if(map.find(\"%s\") != map.end()) {" % (fi) + linebreak 
                buff = buff + tab + tab + "delete (%s *) map[\"%s\"];" % (field["type"], fi) + linebreak
                buff = buff + tab + "}" % () + linebreak 
            buff = buff + "}" + linebreak + linebreak
            
            # copy constructor
            buff = buff + "%s::%s(const %s &src)" % (n, n, n) + linebreak
            buff = buff + "{" + linebreak + tab
            buff = buff + "copy(*this, src);" + linebreak
            buff = buff + "}" + linebreak + linebreak
            
            # assignment operator
            buff = buff + "%s & %s::operator=(const %s &src)" % (n, n, n) + linebreak
            buff = buff + "{" + linebreak + tab
            buff = buff + "return copy(*this, src);" + linebreak
            buff = buff + "}" + linebreak + linebreak 
            
            # move constructor
            buff = buff + "%s::%s(%s &&src) : %s()" % (n, n, n, n) + linebreak
            buff = buff + "{" + linebreak + tab
            buff = buff + "move(*this, src);" + linebreak
            buff = buff + "}" + linebreak + linebreak
            
            # move assignment operator
            buff = buff + "%s & %s::operator=(%s &&src)" % (n, n, n) + linebreak
            buff = buff + "{" + linebreak + tab
            buff = buff + "return move(*this, src);" + linebreak
            buff = buff + "}" + linebreak + linebreak
           
            requiredCount = 0
            # constructor for required members
            if len(struct["fields"]) > 0:
                buff = buff + "%s::%s(" % (n, n)
                first = True
                for field in struct["fields"]:
                    if field["required"] == "true":
                        requiredCount += 1
                        if not first:
                            buff = buff + ", " 
                        buff = buff + "%s %s" % (field["type"], field["cppName"])
                        first = False
                buff = buff + ") : %s()" % (struct["name"]) + linebreak 
                buff = buff + "{" + linebreak 
                for field in struct["fields"]:
                    if field["required"] == "true":
                        buff = buff + tab + "this->%s = new %s(%s);" % (field["cppName"], field["type"], field["cppName"]) + linebreak
                buff = buff + "}" + linebreak + linebreak 
 
            # constructor for all members
            if len(struct["fields"]) != requiredCount:
                buff = buff + "%s::%s(" % (n, n)
                first = True
                for field in struct["fields"]:
                    if not first:
                        buff = buff + ", " 
                    buff = buff + "%s %s" % (field["type"], field["cppName"])
                    first = False
                buff = buff + ") : %s(" % (struct["name"])
                first = True
                for field in struct["fields"]:
                    if field["required"] == "true":
                        requiredCount += 1
                        if not first:
                            buff = buff + ", " 
                        buff = buff + "%s" % (field["cppName"])
                        first = False
                buff = buff + ")" + linebreak
                
                buff = buff + "{" + linebreak
                for field in struct["fields"]:
                    buff = buff + tab + "this->%s = new %s(%s);" % (field["cppName"], field["type"], field["cppName"]) + linebreak
                buff = buff + "}" + linebreak + linebreak
 
            # getter
            for field in struct["fields"]:
                fn = field["cppName"]
                buff = buff + "%s * %s::Get%s()" % (field["type"], n, upper(fn)) + linebreak
                buff = buff + "{" + linebreak + tab
                buff = buff + "if(%s == nullptr) {" % (fn) + linebreak + tab + tab
                buff = buff + "if(map.find(\"%s\") == map.end()) {" % (fn) + linebreak + tab + tab + tab
                buff = buff + "map.emplace(\"%s\", (void *) new %s);" % (fn, field["type"]) + linebreak + tab + tab
                buff = buff + "}" + linebreak + tab + tab 
                buff = buff + "return (%s *) map[\"%s\"];" % (field["type"], fn) + linebreak + tab
                buff = buff + "}" + linebreak + tab
                buff = buff + "return %s;" % (fn) + linebreak
                buff = buff + "}" + linebreak + linebreak
            # value getter
            for field in struct["fields"]:
                fn = field["cppName"]
                buff = buff + "%s & %s::Get%sValue()" % (field["type"], n, upper(fn)) + linebreak
                buff = buff + "{" + linebreak + tab
                buff = buff + "return *%s;" % (fn) + linebreak
                buff = buff + "}" + linebreak + linebreak
            f.write(buff)
            
        f.write(postfix)
        
def generateStructureToJSONConverter(file, deps):
    file = filePath + file
    includes = ""
    for d  in deps:
        includes = includes + "#include \"%s\"\n" % (d) 
   
    prefix = includes + "\n" + """namespace telegram::structures
{
"""
    postfix = """
}
"""
    
    tab = "    "
    linebreak = "\n" 
    with open(file, "w") as f:
        f.write(prefix)
        
        with open(jsonFile) as data_file:    
            structures = json.load(data_file)
        for struct in structures:
            buff = tab + "template <> Serializable Converter::ToJSON(const %s &obj)" % (struct["name"]) + linebreak
            buff = buff + tab + "{" + linebreak + tab
            buff = buff + tab + "Serializable s;" + linebreak
            
            for field in struct["fields"]:
                if field["required"] == "true":
                    func = "REQ"
                else:
                    func = "OPT"
                buff = buff + tab + tab + "%s(s, \"%s\", obj.%s);" % (func, field["jsonName"], field["cppName"]) + linebreak
            
            buff = buff + tab + tab + "return s;" + linebreak
            buff = buff + tab + "}" + linebreak
            if struct != structures[-1]:
                buff = buff + linebreak
            f.write(buff)
        
        f.write(postfix)
        
def generateStructureFromJSONConverter(file, deps):
    file = filePath + file
    includes = ""
    for d  in deps:
        includes = includes + "#include \"%s\"\n" % (d) 
    
    prefix = includes + "\n" + """namespace telegram::structures
{
"""
    postfix = """
}
"""
    
    tab = "    "
    linebreak = "\n"
    with open(file, "w") as f:
        f.write(prefix)
        
        with open(jsonFile) as data_file:    
            structures = json.load(data_file)
        for struct in structures:
            buff = tab + "template <> %s Converter::FromJSON(const Serializable &json)" % (struct["name"]) + linebreak
            buff = buff + tab + "{" + linebreak 
            buff = buff + tab + tab + "%s obj;" % (struct["name"]) + linebreak
            
            for field in struct["fields"]:
                if field["required"] == "true":
                    func = "REQ"
                else:
                    func = "OPT"
                buff = buff + tab + tab + "%s(json, \"%s\", obj.%s);" % (func, field["jsonName"], field["cppName"]) + linebreak
            
            buff = buff + tab + tab + "return std::move(obj);" + linebreak
            buff = buff + tab + "}" + linebreak
            if struct != structures[-1]:
                buff = buff + linebreak 
            f.write(buff)
        
        f.write(postfix)
        

def generateCommonHeader(file, deps):
    content = """#ifndef GENERATED_SOURCES_H_
#define GENERATED_SOURCES_H_

"""
    includes = ""
    for d  in deps:
        includes = includes + "#include \"%s\"\n" % (d) 
    content = content + includes
    content = content + """
    
#endif // GENERATED_SOURCES_H_
"""
    with open(path + file, "w") as f:
        f.write(content)


jsonFile = path + "json/DataStructureDefinitions.json"

converterHeaderFile = "telegram/StructConverter.h"
headerFile = "DataStructures.h"
implFile = "DataStructures.cpp"
toJSONFile = "StructConverterToJSON.cpp"
fromJSONFile = "StructConverterFromJSON.cpp"
toJSONTemplates = "../templates/ToJSONTemplates.cpp"
fromJSONTemplates = "../templates/FromJSONTemplates.cpp"
commonHeader = "generated.h"


if os.path.isdir(filePath):
    shutil.rmtree(filePath)
    os.makedirs(filePath) 
if os.path.exists(path + commonHeader):
    os.remove(path + commonHeader)

generateHeader(headerFile, [converterHeaderFile])
generateImplementation(implFile, [headerFile])
generateStructureToJSONConverter(toJSONFile, [headerFile, toJSONTemplates])
generateStructureFromJSONConverter(fromJSONFile, [headerFile, fromJSONTemplates])

relativePath = filePath.replace(path, "")

generateCommonHeader(commonHeader, [relativePath + headerFile])
