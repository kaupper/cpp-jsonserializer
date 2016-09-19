Welcome to cpp-jsonserializer!

The content of this repository is dedicated to the automatic creation of (de-)serialiable structs using jsoncpp and cpp.

The generation of the structs itself is done by a python script (generator.py) and has following parameters:
- --json=\<struct_description_file\>: Specifies the file which should be used as template for our structs. For the structure of such a template file please see EXAMPLE.json
- --output=\<output_directory\>: Specifies the output directory for generated files. Default is ./generated/
- --header=\<common_header\>: Specifies the path and the file name for the header file which should be included in your application. Default is ./generated.h

Usage of structures:
