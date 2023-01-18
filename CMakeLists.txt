cmake_minimum_required(VERSION 3.16)
project(mpl)


list(PREPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(JPEG REQUIRED)

file(GLOB Hh_SRC_FILES libHh/*.cpp)
add_library(Hh ${Hh_SRC_FILES})
target_include_directories(Hh PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_include_directories(Hh PUBLIC ${JPEG_INCLUDE_DIR})
target_link_libraries(Hh ${JPEG_LIBRARIES})

add_executable(subdivfit Subdivfit/Subdivfit.cpp)
target_include_directories(subdivfit PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(subdivfit Hh)
