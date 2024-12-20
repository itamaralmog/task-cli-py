# Set the minimum required version for CMake
cmake_minimum_required(VERSION 3.10)

# Project Name
project(TaskCLI)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include FetchContent module to fetch external dependencies
include(FetchContent)

# Fetch doctest from GitHub (use the version that fits your needs)
FetchContent_Declare(
    doctest
    GIT_REPOSITORY https://github.com/doctest/doctest.git
    GIT_TAG master  # Or use a specific version/tag
)

# Fetch and make doctest available
FetchContent_MakeAvailable(doctest)

# Find the nlohmann JSON library (ensure it's installed or available in your environment)
find_package(nlohmann_json REQUIRED)

# Add the main executable
add_executable(task_cli task_cli.cpp)

# Link nlohmann_json to the task_cli executable
target_link_libraries(task_cli PRIVATE nlohmann_json::nlohmann_json)

# Add the test executable
add_executable(tests test_task_cli.cpp)

# Link doctest and nlohmann_json to the test executable
target_link_libraries(tests PRIVATE doctest::doctest nlohmann_json::nlohmann_json)

# Optional: Enable testing in CMake
enable_testing()

# Add a test to the CMake testing framework
add_test(NAME TestTasks COMMAND tests)
