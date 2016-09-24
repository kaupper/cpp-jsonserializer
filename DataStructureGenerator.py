import sys
import os
import json
import shutil


jsonFile = ""
includes = []

for arg in sys.argv:
    if arg.startswith("--json="):
        jsonFile = arg[len("--json="):]
    if arg.startswith("--include="):
        includes.append(arg[len("--include=")])
        
if jsonFile == "":
    print("Usage: %s --json=<struct_description_file> [--include=<include_header>]" % (os.path.basename(__file__)))
    print("\tstruct_description_file: Specifies the file which should be used as template for our structs.")
    print("\tinclude_header: If your structs need certain headers to be included you can specify one or more --include clauses (for example --include=<string> or --include=\"relativeHeader.h\")")
    sys.exit(1)
    
print("JSON file: " + jsonFile)




def upper(s):
    l = list(s)
    l[0] = l[0].upper()
    return ''.join(l)

def generateHeader(file, structures, namespace, deps):
    prefix = """#ifndef JSON_SERIALIZER_DATA_STRUCTURES_""" + namespace.upper().replace("::", "_") + """_H_
#define JSON_SERIALIZER_DATA_STRUCTURES_""" + namespace.upper().replace("::", "_") + """_H_

#include <map>
""" 
    includes = ""
    for d in deps:
        includes = includes + "#include %s\n" % (d) 
    prefix = prefix + includes
    prefix = prefix + "\nnamespace " + namespace + "\n{\n"
   
    postfix = """}

#endif // JSON_SERIALIZER_DATA_STRUCTURES_""" + namespace.upper().replace("::", "_") + """_H_
"""
    tab = "    "
    linebreak = "\n"
    names = []
    buffer = []
    with open(file, "w") as f:
        f.write(prefix)
        
        for struct in structures:
            n = struct["name"]
            names.append(struct["name"])
            
            buff = "struct %s" % (n) + linebreak + tab
            buff = buff + "{" + linebreak + tab + tab
            # constructor
            buff = buff + "%s();" % (n) + linebreak + tab + tab
            # destructor
            buff = buff + "virtual ~%s();" % (n) + linebreak + tab + tab
            # copy constructor
            buff = buff + "%s(const %s &);" % (n, n) + linebreak + tab + tab
            # assignment
            buff = buff + "%s & operator=(const %s &);" % (n, n) + linebreak + tab + tab
            # move constructor
            buff = buff + "%s(%s &&);" % (n, n) + linebreak + tab + tab
            # move assignment
            buff = buff + "%s & operator=(%s &&);" % (n, n) + linebreak + tab + tab

            requiredCount = 0
            
            for field in struct["fields"]:
                required = "true"
                if "required" in field:
                    required = field["required"]
                if required == "true":
                    requiredCount += 1
            
            # constructor for required members
            if requiredCount > 0:
                tmp = ""
                tmp = tmp + "%s(" % (struct["name"])
                first = True
                for field in struct["fields"]:
                    required = "true"
                    if "required" in field:
                        required = field["required"]
                    if required == "true":
                        if not first:
                            tmp = tmp + ", "
                        tmp = tmp + "const %s &" % (field["type"])
                        first = False
                tmp = tmp + ");" + linebreak + tab 
                buff = buff + tmp
 
            if requiredCount != len(struct["fields"]):
                # constructor for all members
                buff = buff + tab + "%s(" % (struct["name"])
                first = True
                for field in struct["fields"]:
                    if not first:
                        buff = buff + ", " 
                    buff = buff + "const %s &" % (field["type"])
                    first = False
                buff = buff + ");" + linebreak + tab 

            transient = "false"
            if "transient" in struct:
                transient = struct["transient"]

            buff = buff + linebreak + tab
            buff = buff + "static const bool __transient = %s;" % (transient) + linebreak + tab

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
                buff = buff + tab + "%s & Get%sValue() const;" % (t, upper(n)) + linebreak + tab
                buff = buff + tab + "void Set%s(const %s &%s);" % (upper(n), t, n) + linebreak + tab

            buff = buff + "};"
            buffer.append(buff);
        
        for name in names:
            f.write(tab + "struct " + name + ";" + linebreak)
                
        for buff in buffer:
            f.write(linebreak + tab + buff + linebreak)
        
        f.write(postfix)
        
def generateImplementation(file, structures, namespace, deps):
    includes = ""
    for d  in deps:
        includes = includes + "#include %s\n" % (d) 
    
    prefix = includes + "\n"
    prefix = prefix + """using namespace """ + namespace + """;

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
            
            for field in struct["fields"]:
                required = "true"
                if "required" in field:
                    required = field["required"]
                if required == "true":
                    requiredCount += 1
                    
            # constructor for required members
            if requiredCount > 0:
                buff = buff + "%s::%s(" % (n, n)
                first = True
                for field in struct["fields"]:
                    required = "true"
                    if "required" in field:
                        required = field["required"]
                    if required == "true":
                        if not first:
                            buff = buff + ", " 
                        buff = buff + "const %s &%s" % (field["type"], field["cppName"])
                        first = False
                buff = buff + ") : %s()" % (struct["name"]) + linebreak 
                buff = buff + "{" + linebreak 
                for field in struct["fields"]:
                    required = "true"
                    if "required" in field:
                        required = field["required"]
                    if required == "true":
                        buff = buff + tab + "this->%s = new %s(%s);" % (field["cppName"], field["type"], field["cppName"]) + linebreak
                buff = buff + "}" + linebreak + linebreak 
 
            # constructor for all members
            if len(struct["fields"]) != requiredCount:
                buff = buff + "%s::%s(" % (n, n)
                first = True
                for field in struct["fields"]:
                    if not first:
                        buff = buff + ", " 
                    buff = buff + "const %s &%s" % (field["type"], field["cppName"])
                    first = False
                buff = buff + ") : %s(" % (struct["name"])
                first = True
                for field in struct["fields"]:
                    required = "true"
                    if "required" in field:
                        required = field["required"]
                    if required == "true":
                        requiredCount += 1
                        if not first:
                            buff = buff + ", " 
                        buff = buff + "%s" % (field["cppName"])
                        first = False
                buff = buff + ")" + linebreak
                
                buff = buff + "{" + linebreak
                for field in struct["fields"]:
                    required = "true"
                    if "required" in field:
                        required = field["required"]
                    if required != "true":
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
                buff = buff + "%s & %s::Get%sValue() const" % (field["type"], n, upper(fn)) + linebreak
                buff = buff + "{" + linebreak + tab
                buff = buff + "return *%s;" % (fn) + linebreak
                buff = buff + "}" + linebreak + linebreak
            # setter
            for field in struct["fields"]:
                fn = field["cppName"]
                t = field["type"]
                buff = buff + "void %s::Set%s(const %s &%s)" % (n, upper(fn), t, fn) + linebreak
                buff = buff + "{" + linebreak + tab
                buff = buff + "if(this->%s != nullptr) {" % (fn) + linebreak + tab + tab
                buff = buff + "delete this->%s;" % (fn) + linebreak + tab
                buff = buff + "}" + linebreak + tab
                buff = buff + "this->%s = new %s(%s);" % (fn, t, fn) + linebreak 
                buff = buff + "}" + linebreak + linebreak
            f.write(buff)
            
        f.write(postfix)
        
def generateStructureToJSONConverter(file, structures, namespace, deps):
    includes = ""
    for d  in deps:
        includes = includes + "#include %s\n" % (d) 
   
    prefix = includes + "\nusing namespace " + namespace + """; 
    
namespace jsonserializer::structures
{
"""
    postfix = """}
"""
    
    tab = "    "
    linebreak = "\n" 
    with open(file, "w") as f:
        f.write(prefix)
        
        for struct in structures:
            buff = tab + "template <> Serializable Converter::ToJSON(const %s &obj)" % (struct["name"]) + linebreak
            buff = buff + tab + "{" + linebreak + tab
            buff = buff + tab + "Serializable s;" + linebreak
            
            for field in struct["fields"]:
                required = "true"
                if "required" in field:
                    required = field["required"]
                if required == "true":
                    func = "REQ"
                else:
                    func = "OPT"
                jsonName = field["cppName"]
                if "jsonName" in field:
                    jsonName = field["jsonName"]
                buff = buff + tab + tab + "%s(s, \"%s\", obj.%s);" % (func, jsonName, field["cppName"]) + linebreak
            
            buff = buff + tab + tab + "return s;" + linebreak
            buff = buff + tab + "}" + linebreak
            if struct != structures[-1]:
                buff = buff + linebreak
            f.write(buff)
        
        f.write(postfix)
        
def generateStructureFromJSONConverter(file, structures, namespace, deps):
    includes = ""
    for d  in deps:
        includes = includes + "#include %s\n" % (d) 
    
    prefix = includes + "\nusing namespace " + namespace + """; 
    
namespace jsonserializer::structures
{
"""
    postfix = """}
"""
    
    tab = "    "
    linebreak = "\n"
    with open(file, "w") as f:
        f.write(prefix)
        
        for struct in structures:
            buff = tab + "template <> %s Converter::FromJSON(const Serializable &json)" % (struct["name"]) + linebreak
            buff = buff + tab + "{" + linebreak 
            buff = buff + tab + tab + "%s obj;" % (struct["name"]) + linebreak
            
            for field in struct["fields"]:
                required = "true"
                if "required" in field:
                    required = field["required"]
                if required == "true":
                    func = "REQ"
                else:
                    func = "OPT"
                jsonName = field["cppName"]
                if "jsonName" in field:
                    jsonName = field["jsonName"]
                buff = buff + tab + tab + "%s(json, \"%s\", obj.%s);" % (func, jsonName, field["cppName"]) + linebreak
            
            buff = buff + tab + tab + "return std::move(obj);" + linebreak
            buff = buff + tab + "}" + linebreak
            if struct != structures[-1]:
                buff = buff + linebreak 
            f.write(buff)
        
        f.write(postfix)
        

def generateCommonHeader(file, namespace, deps):
    content = """#ifndef JSON_SERIALIZER_GENERATED_SOURCES_""" + namespace.upper().replace("::", "_") + """_H_
#define JSON_SERIALIZER_GENERATED_SOURCES_""" + namespace.upper().replace("::", "_").replace("::", "_") + """_H_

"""
    includes = ""
    for d  in deps:
        includes = includes + "#include %s\n" % (d) 
    content = content + includes
    content = content + """    
#endif // JSON_SERIALIZER_GENERATED_SOURCES_""" + namespace.upper().replace("::", "_") + """_H_
"""
    with open(file, "w") as f:
        f.write(content)


if __name__ == "__main__":
    # reference to StructConverter.h       
    converterHeaderFile = "\"jsonserializer/StructConverter.h\""

    # references to serialize templates
    toJSONTemplates = "\"templates/ToJSONTemplates.cpp\""
    fromJSONTemplates = "\"templates/FromJSONTemplates.cpp\""

    # generated outputs
    headerFile = "DataStructures.h"
    implFile = "DataStructures.cpp"
    toJSONFile = "DataStructureConverterToJSON.cpp"
    fromJSONFile = "DataStructureConverterFromJSON.cpp"


    with open(jsonFile, "r") as dataFile:
        data = json.load(dataFile)

    for structureSet in data:
        if "outputDirectory" in structureSet:
            outputPath = structureSet["outputDirectory"]
        else:
            outputPath = "generated"
        path = os.path.join(os.path.join(os.path.dirname(__file__), "generated"), outputPath)

        if "commonHeader" in structureSet:
            commonHeader = structureSet["commonHeader"]
        else:
            commonHeader = "generated.h"
        commonHeader = os.path.join(os.path.dirname(jsonFile), commonHeader)
        print("Commonheader: " + commonHeader)

        if "namespace" in structureSet:
            namespace = structureSet["namespace"]
        else:
            namespace = "jsonserializer::generated"
        
        dependencies = includes[:] 
        if "dependencies" in structureSet:
            dependencies = structureSet["dependencies"]

        if "definitionsFile" in structureSet:
            with open(os.path.join(os.path.dirname(jsonFile), structureSet["definitionsFile"]), "r") as file:
                definitions = json.load(file)
        else:
            definitions = structureSet["definitions"]

        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path)
        if os.path.exists(commonHeader):
            os.remove(commonHeader)

        generateHeader(os.path.join(path, headerFile), definitions, namespace, dependencies + [converterHeaderFile])
        generateImplementation(os.path.join(path, implFile), definitions, namespace, dependencies + ["\"" + headerFile + "\""])
        generateStructureToJSONConverter(os.path.join(path, toJSONFile), definitions, namespace, dependencies + ["\"" + headerFile + "\"", toJSONTemplates])
        generateStructureFromJSONConverter(os.path.join(path, fromJSONFile), definitions, namespace, dependencies + ["\"" + headerFile + "\"", fromJSONTemplates])

        generateCommonHeader(commonHeader, namespace, dependencies + ["\"" + os.path.join(path, headerFile).replace(os.path.dirname(jsonFile), "")[1:] + "\""])
