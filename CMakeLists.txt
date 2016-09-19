cmake_minimum_required(VERSION 3.6)
project (jsonserializer)
 
set (PROJECT_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/include)
set (PROJECT_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)
 
# check for generator flags
if(NOT GENERATED_DIRECTORY)
    set (GENERATED_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/generated)
endif()
if(NOT GENERATED_HEADER)
    set (GENERATED_HEADER ${CMAKE_CURRENT_SOURCE_DIR}/include/generated.h)
endif()
if(NOT JSON_FILE)
    message(FATAL_ERROR "Please specify a JSON template for your structures!")
endif()
 
# TODO: maybe another solution to get the generator script
file (GLOB GENERATOR *.py)
# execute generator at configuration time to provide actual output files to the linker (?)
execute_process(
COMMAND "python" 
"${GENERATOR}" 
"--json=${JSON_FILE}" 
"--output=${GENERATED_DIRECTORY}" 
"--header=${GENERATED_HEADER}"
)

if(${result})
    message (FATAL_ERROR "Structure generation failed!")
endif()

set(SERIALIZER_SOURCES
${PROJECT_SOURCE_DIR}/Serializable.cpp 
${PROJECT_SOURCE_DIR}/PersistingService.cpp
)
 
file(GLOB GENERATED_SOURCES ${GENERATED_DIRECTORY}/*.cpp)

# generator will be executed every time the lib is built
add_custom_target(python_generator 
COMMAND "python" 
"${GENERATOR}" 
"--json=${JSON_FILE}" 
"--output=${GENERATED_DIRECTORY}" 
"--header=${GENERATED_HEADER}"
)

include_directories(${PROJECT_INCLUDE_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

add_library(${PROJECT_NAME} STATIC ${SERIALIZER_SOURCES} ${GENERATED_SOURCES})
target_include_directories (${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
add_dependencies(${PROJECT_NAME} python_generator)

