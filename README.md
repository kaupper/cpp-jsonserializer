Welcome to cpp-jsonserializer!

The content of this repository is dedicated to the automatic creation of (de-) serializable structs using [json](https://github.com/nlohmann/json/), C++, [Jinja2](https://github.com/pallets/jinja) and CMake. 
The core of the CMake file is the execution of the python script. If you want to get rid of CMake, take the python script and the folders jsonserializer and templates and move them (generator.py depends on these).
While you can get rid of CMake, be sure you have installed python 3 and Jinja2!

The generation of the structs itself is done by a python script (generator.py) and has the following parameters:
- `--cfg <configuration_files>`: Specifies the files which describes the structures. For the structure of such a description file see below. The paths are relative to the cmake source directory.

Example structure for JSON input:
```javascript
{
    // gets prepended to the template file names
    // optional, empty by default
    "name": "Data", 
    // #include <global_include>
    // optional, empty by default
    "global_includes": ["string", "vector"], 
    // #include "local_include"
    // optional, empty by default
    "local_includes": [], 
    // used as namespace for the generated structures 
    // optional, 'structures' by default
    "namespace": "test::namespace",
    // array of structures
    // optional, [] by default
    "structures": [
        {
            // name of the structure
            // required!
            "name": "TestStruct",
            // a transient struct gets flattened when serialized
            // optional, false by default
            "transient": true,
            // array with description of all fields
            // optional, [] by default
            "fields": [
                {
                    // name used in the struct
                    // required!
                    "name": "stringField",
                    // used for method naming (cc stands for CamelCase)
                    // optional, <name> with first capital letter by default
                    "ccName": "StringField",
                    // the name used in an serialized JSON string
                    // optional, snake case of <ccname> by default
                    "jsonName": "string_field",
                    // the C++ type to be used for this field
                    // optional, int by default
                    "type": "std::string",
                    // is this field optional or required?
                    // optional, false by default
                    "required": true
                },
                {
                    "name": "intfield",
                    "ccname": "IntField",
                    "jsonname": "int_field",
                    "type": "int",
                    "required": false
                }
            ]
        }
    ]
}
```


Structs generated will contain:
- A simple constructor initializing the members.
- A destructur which deletes the members if neccesary.
- Copy constructor/assignment operator.
- Another constructor with all required fields (if neccesary).
- Getter and setters for all fields as described below

To be able to have optional fields the members must be pointers, therefore it is possible that they are `NULL`/`nullptr`. 
If you do not want to do checks for `nullptr` yourself you can use the corresponding `Get<field_name>()` method.
`GetStringField()` will check if the `stringfield` is `nullptr`. If so it will create a new pointer and returns that default object. Validation of these objects is up to the user.
`Get<field_name>Value()` returns the dereferenced object (may crash of course).
`Set<field_name>(const <field_type> &)` creates a new pointer and sets it to the given value. It also takes care of an already existing pointer.

Transient structs will be flattened when serialized to JSON.

See the example folder for an usage example!
