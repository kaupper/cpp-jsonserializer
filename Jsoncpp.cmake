include(ExternalProject)

ExternalProject_Add(json-cpp
    URL https://github.com/open-source-parsers/jsoncpp/archive/1.7.5.zip
    CMAKE_ARGS
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
        -DJSONCPP_WITH_TESTS:BOOL=OFF
    # Disable the install step.
    INSTALL_COMMAND ""
    # Wrap the download, configure and build steps in a script to log the
    # output.
    LOG_DOWNLOAD ON
    LOG_CONFIGURE ON
    LOG_BUILD ON
)
ExternalProject_Get_Property(json-cpp source_dir)
ExternalProject_Get_Property(json-cpp binary_dir)
include_directories("${source_dir}/include")
link_directories("${binary_dir}/src/json_lib")