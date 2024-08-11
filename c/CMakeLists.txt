cmake_minimum_required(VERSION 3.10)
project(KnapsackSolverC)

# Set the C++ standard to C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Include the OR-Tools headers
include_directories("${CMAKE_SOURCE_DIR}/libs/or-tools/include")

# Link the OR-Tools libraries
link_directories("${CMAKE_SOURCE_DIR}/libs/or-tools/lib")

# Create the executable from the main source file
add_executable(KnapsackSolver main.cpp)

# Link against the OR-Tools library
target_link_libraries(KnapsackSolver ortools)

