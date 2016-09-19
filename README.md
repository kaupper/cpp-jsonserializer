Welcome to cpp-jsonserializer!

The content of this repository is dedicated to the automatic creation of (de-)serialiable structs using jsoncpp and cpp.

The generation of the structs itself is done by a python script (generator.py) and has following parameters:
- `--json=<struct_description_file>`: Specifies the file which should be used as template for our structs. For the structure of such a template file see below.
- `--output=<output_directory>`: Specifies the output directory for generated files. Default is ./generated/.
- `--header=<common_header>`: Specifies the path and the file name for the header file which should be included in your application. Default is ./generated.h.

Example structure for JSON input:
```json
[{
	"fields": [{
		"cppName": "testField11",
		"jsonName": "test_field_11",
		"type": "int",
		"required": "true"
	}, {
		"cppName": "testField12",
		"jsonName": "test_field_12",
		"type": "std::string",
		"required": "true"
	}],
	"name": "TestStruct1"
}]
```

This JSON file will produce the following header:
```c++
#ifndef JSON_SERIALIZER_DATA_STRUCTURES_H_
#define JSON_SERIALIZER_DATA_STRUCTURES_H_

#include <vector>
#include <string>
#include <map>

#include "include/StructConverter.h"

namespace jsonserializer::structures
{
    struct TestStruct1;

    struct TestStruct1
    {
        TestStruct1();
        virtual ~TestStruct1();
        TestStruct1(const TestStruct1 &);
        TestStruct1 & operator=(const TestStruct1 &);
        TestStruct1(TestStruct1 &&);
        TestStruct1 & operator=(TestStruct1 &&);
        TestStruct1(int testField11, std::string testField12);
    
        int *testField11;
        std::string *testField12;
    
        std::map<std::string, void*> map;

        int * GetTestField11();
        int & GetTestField11Value();
        std::string * GetTestField12();
        std::string & GetTestField12Value();
    };
}

#endif // JSON_SERIALIZER_DATA_STRUCTURES_H_
```

Structs generated will contain:
- A simple constructor initializing the members.
- A destructur which deletes the members if neccesary.
- Copy and move constructor/assignment operators.
- Another constructor with all required fields (see JSON).

To be able to have optional fields out members must be pointers, therefore it is possible that they are `NULL`/`nullptr`. 
If you do not want to do checks for `nullptr` yourself you can use the corresponding `Get<field_name>()`.
`GetTestField11()` will check if the `testField11` is a nullptr. If so it will create a new pointer (stored with the field name in `map`) and returns that default object. Validation of these objects is up to the user.
`Get<field_name>Value()` returns the dereferenced object (may segfault!!).

To get all files to compile you will have to set the include directories to the root folder of this repository!
