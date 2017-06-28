cmake_minimum_required(VERSION 3.6)

project(jsonserializer)

if(NOT JSON_CONFIGURATION_FILES)
    message(FATAL_ERROR "Please specify configuration files for your templates (JSON_CONFIGURATION_FILES)!")
endif()

# execute generator at configuration time
execute_process(
    COMMAND "python3"
    "${PROJECT_SOURCE_DIR}/generator.py"
    "--cfg" ${JSON_CONFIGURATION_FILES}
    RESULT_VARIABLE result
)

set(JSON_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/generated PARENT_SCOPE)
file(GLOB JSON_SOURCES ${PROJECT_SOURCE_DIR}/generated/*.cpp)
set(JSON_SOURCES ${JSON_SOURCES} PARENT_SCOPE)

if(${result})
    message (FATAL_ERROR "Structure generation failed!")
endif()
