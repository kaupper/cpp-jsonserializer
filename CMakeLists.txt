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

if(${result})
    message (FATAL_ERROR "Structure generation failed!")
endif()

file(GLOB SOURCES ${PROJECT_SOURCE_DIR}/generated-src/*.cpp)

add_library(${PROJECT_NAME} STATIC ${SOURCES})
target_include_directories(${PROJECT_NAME} PUBLIC ${PROJECT_SOURCE_DIR}/generated-inc)
target_include_directories(${PROJECT_NAME} PRIVATE ${PROJECT_SOURCE_DIR}/generated-inc/jsonserializer)
