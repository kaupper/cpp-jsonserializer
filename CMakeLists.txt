cmake_minimum_required(VERSION 3.6)
project (jsonserializer)

# -- setup structure generator 
# check for generator flags
if(NOT GENERATED_DIRECTORY)
    message(FATAL_ERROR "Please specify a output directory for your structures!")
endif()
if(NOT GENERATED_HEADER)
    message(FATAL_ERROR "Please specify a filename for your generated headerfile for your structures!")
endif()
if(NOT JSON_FILE)
    message(FATAL_ERROR "Please specify a JSON template for your structures!")
endif()

# execute generator at configuration time to provide actual output files to the linker (?)
execute_process(
COMMAND "python" 
"${PROJECT_SOURCE_DIR}/DataStructureGenerator.py" 
"--json=${JSON_FILE}" 
"--output=${GENERATED_DIRECTORY}" 
"--header=${GENERATED_HEADER}"
)

if(${result})
    message (FATAL_ERROR "Structure generation failed!")
endif()
# -------------


# set include directories
include_directories(${PROJECT_SOURCE_DIR}/include ${PROJECT_SOURCE_DIR})
# set sources
file(GLOB GENERATED_SOURCES ${GENERATED_DIRECTORY}/*.cpp)
set(SOURCES 
${GENERATED_SOURCES}
${PROJECT_SOURCE_DIR}/src/Serializable.cpp 
${PROJECT_SOURCE_DIR}/src/PersistingService.cpp
)


# include jsoncpp
include("Jsoncpp.cmake")

# build library
add_library(${PROJECT_NAME} STATIC ${SOURCES})
target_include_directories (${PROJECT_NAME} PUBLIC ${PROJECT_SOURCE_DIR})
target_link_libraries(${PROJECT_NAME} "jsoncpp")
SET_TARGET_PROPERTIES(${PROJECT_NAME} PROPERTIES OUTPUT_NAME jsonserializer)

# generator will be executed every time the lib is built
add_custom_target(python_generator 
COMMAND "python" 
"${PROJECT_SOURCE_DIR}/DataStructureGenerator.py"
"--json=${JSON_FILE}" 
"--output=${GENERATED_DIRECTORY}" 
"--header=${GENERATED_HEADER}"
)
add_dependencies(${PROJECT_NAME} python_generator)
