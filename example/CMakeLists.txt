cmake_minimum_required(VERSION 3.6)

project(example)
set(JSON_OUTPUT_DIR generated/)
set(JSON_CONFIGURATION_FILES sample.json sample2.json)

add_subdirectory(cpp-jsonserializer)

include_directories(${JSON_INCLUDE_DIR})

add_executable(examples main.cpp ${JSON_SOURCES})