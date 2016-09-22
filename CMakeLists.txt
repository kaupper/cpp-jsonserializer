cmake_minimum_required(VERSION 3.6)

if(NOT JSON_SERIALIZER_NAME)
    set(JSON_SERIALIZER_NAME jsonserializer)
endif()

project (${JSON_SERIALIZER_NAME})

# -- setup structure generator 
# check for generator flags
if(NOT WITHOUT_STRUCTS)
    if(NOT GENERATED_NAMESPACE)
        message(FATAL_ERROR "Please specify a namespace for your structures (GENERATED_NAMESPACE)!")
    endif()
    if(NOT GENERATED_DIRECTORY)
        message(FATAL_ERROR "Please specify a output directory for your structures (GENERATED_DIRECTORY)!")
    endif()
    if(NOT GENERATED_HEADER)
        message(FATAL_ERROR "Please specify a filename for your generated headerfile for your structures (GENERATED_HEADER)!")
    endif()
    if(NOT JSON_FILE)
        message(FATAL_ERROR "Please specify a JSON template for your structures (JSON_FILE)!")
    endif()

    # execute generator at configuration time to provide actual output files to the linker (?)
    execute_process(
        COMMAND "python" 
        "${PROJECT_SOURCE_DIR}/DataStructureGenerator.py" 
        "--json=${JSON_FILE}" 
        "--output=${GENERATED_DIRECTORY}" 
        "--header=${GENERATED_HEADER}"
        "--namespace=${GENERATED_NAMESPACE}"
    )

    if(${result})
        message (FATAL_ERROR "Structure generation failed!")
    endif()
    
    # set sources
    file(GLOB GENERATED_SOURCES ${GENERATED_DIRECTORY}/*.cpp)
    set(SOURCES ${SOURCES} ${GENERATED_SOURCES})
endif()
# -------------


# set include directories
include_directories(${PROJECT_SOURCE_DIR}/jsonserializer ${PROJECT_SOURCE_DIR})
set(SOURCES 
    ${SOURCES}
    ${PROJECT_SOURCE_DIR}/src/Serializable.cpp 
    ${PROJECT_SOURCE_DIR}/src/PersistingService.cpp
)


# include jsoncpp
include("Jsoncpp.cmake")

# build library
add_library(${PROJECT_NAME} STATIC ${SOURCES})
target_include_directories (${PROJECT_NAME} PUBLIC ${PROJECT_SOURCE_DIR})
target_link_libraries(${PROJECT_NAME} "jsoncpp")

if(NOT WITHOUT_STRUCTS)
    add_custom_target(generated
        COMMAND ${CMAKE_COMMAND} 
        "-DGENERATOR=${PROJECT_SOURCE_DIR}/DataStructureGenerator.py" 
        "-DJSON_FILE=${JSON_FILE}"
        "-DGENERATED_DIRECTORY=${GENERATED_DIRECTORY}"
        "-DGENERATED_HEADER=${GENERATED_HEADER}"
        "-DGENERATED_NAMESPACE=${GENERATED_NAMESPACE}"
        "-P" 
        "${PROJECT_SOURCE_DIR}/generateIfChanged.cmake"
    )
    add_dependencies(${PROJECT_NAME} generated)
endif()
