cmake_minimum_required(VERSION 3.6)

project(example)

set(JSON_CONFIGURATION_FILES ${PROJECT_SOURCE_DIR}/sample.json ${PROJECT_SOURCE_DIR}/sample2.json)
add_subdirectory(cpp-jsonserializer)

add_executable(examples main.cpp)
target_link_libraries(examples jsonserializer)