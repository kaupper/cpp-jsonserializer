cmake_minimum_required(VERSION 3.6)

FUNCTION(PREPEND var prefix)
   SET(listVar "")
   FOREACH(f ${ARGN})
      LIST(APPEND listVar "${prefix}/${f}")
   ENDFOREACH(f)
   SET(${var} "${listVar}" PARENT_SCOPE)
ENDFUNCTION(PREPEND)

project(jsonserializer)

if(NOT JSON_CONFIGURATION_FILES)
    message(FATAL_ERROR "Please specify configuration files for your templates (JSON_CONFIGURATION_FILES)!")
endif()

if(NOT JSON_OUTPUT_DIR)
    message(FATAL_ERROR "Please specify a output directory (JSON_OUTPUT_DIR)!")
endif()

PREPEND(JSON_CONFIGURATION_FILES ${CMAKE_SOURCE_DIR} ${JSON_CONFIGURATION_FILES})

# execute generator at configuration time
execute_process(
    COMMAND "python3" 
    "${PROJECT_SOURCE_DIR}/generator.py" 
    "--cfg" ${JSON_CONFIGURATION_FILES}
    "--output" "${CMAKE_BINARY_DIR}/${JSON_OUTPUT_DIR}"
)

set(JSON_INCLUDE_DIR ${CMAKE_BINARY_DIR}/${JSON_OUTPUT_DIR} PARENT_SCOPE)
file(GLOB JSON_SOURCES ${CMAKE_BINARY_DIR}/${JSON_OUTPUT_DIR}/*.cpp)
set(JSON_SOURCES ${JSON_SOURCES} PARENT_SCOPE)

if(${result})
    message (FATAL_ERROR "Structure generation failed!")
endif()
