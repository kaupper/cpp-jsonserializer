execute_process(
COMMAND "stat"
"-c"
"%Y"
"${GENERATOR}"
OUTPUT_VARIABLE GENERATOR_DATE)

execute_process(
COMMAND "stat"
"-c"
"%Y"
"${GENERATED_DIRECTORY}"
OUTPUT_VARIABLE DIRECTORY_DATE)

execute_process(
COMMAND "stat"
"-c"
"%Y"
"${JSON_FILE}"
OUTPUT_VARIABLE JSON_DATE)

if(${GENERATOR_DATE} GREATER ${DIRECTORY_DATE} OR ${JSON_FILE} GREATER ${DIRECTORY_DATE})
    execute_process(
    COMMAND "python" 
    "${GENERATOR}" 
    "--json=${JSON_FILE}" 
    "--output=${GENERATED_DIRECTORY}" 
    "--header=${GENERATED_HEADER}"
    )
else()
    message(STATUS "Generated files are up to date")
endif()