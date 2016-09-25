cmake_minimum_required(VERSION 3.6)

if(NOT JSON_SERIALIZER_NAME)
    set(JSON_SERIALIZER_NAME jsonserializer)
endif()

project (${JSON_SERIALIZER_NAME})

# -- setup structure generator 
# check for generator flags
if(NOT WITHOUT_STRUCTS)
    if(NOT JSON_FILE)
        message(FATAL_ERROR "Please specify a JSON template for your structures (JSON_FILE)!")
    endif()

    # execute generator at configuration time to provide actual output files to the linker (?)
    execute_process(
        COMMAND "python" 
        "${PROJECT_SOURCE_DIR}/DataStructureGenerator.py" 
        "--json=${JSON_FILE}" 
    )

    if(${result})
        message (FATAL_ERROR "Structure generation failed!")
    endif()
endif()
# -------------


# set include directories
include_directories(${PROJECT_SOURCE_DIR}/jsonserializer ${PROJECT_SOURCE_DIR})
file(GLOB_RECURSE GLOB_SOURCES DataStructures.cpp)
file(GLOB_RECURSE SOURCES *.cpp)
set(SOURCES ${GLOB_SOURCES} ${SOURCES})
list(REMOVE_DUPLICATES SOURCES)

# include jsoncpp
include("Jsoncpp.cmake")

# build library
add_library(${PROJECT_NAME} STATIC ${SOURCES})
target_include_directories (${PROJECT_NAME} PUBLIC ${PROJECT_SOURCE_DIR} ${PROJECT_SOURCE_DIR}/generated)
target_link_libraries(${PROJECT_NAME} "jsoncpp")
