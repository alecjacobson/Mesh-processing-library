cmake_minimum_required(VERSION 3.16)
project(mpl)

list(PREPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
# Threads appears to be required on Linux
find_package(Threads REQUIRED)
find_package(JPEG REQUIRED)
find_package(PNG REQUIRED)
# OpenMP is optional. Try to find it, if not then set empty param
find_package(OpenMP)
if(OpenMP_CXX_FOUND)
  set(OPENMP_MODULE OpenMP::OpenMP_CXX)
else()
  add_compile_definitions(HH_NO_OPENMP)
endif()

file(GLOB Hh_SRC_FILES libHh/*.cpp)
add_library(Hh ${Hh_SRC_FILES})
target_include_directories(Hh PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_include_directories(Hh PUBLIC ${JPEG_INCLUDE_DIR})
target_link_libraries(Hh PUBLIC ${JPEG_LIBRARIES} ${PNG_LIBRARIES} ${OPENMP_MODULE})

#Getting the X11/GLX gui running on Mac seems pretty hopeless.
if(NOT APPLE)
  # This has not been tested on Linux, but may be a good starting point
  find_package(X11 REQUIRED)
  if(X11_FOUND)
    find_package(OpenGL REQUIRED)
    file(GLOB HW_SRC_FILES libHWX/*.cpp)
    add_library(HW ${HW_SRC_FILES})
    target_include_directories(HW PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
    target_include_directories(HW PUBLIC ${X11_INCLUDE_DIR})
    target_link_libraries(HW PUBLIC ${X11_LIBRARIES} Hh OpenGL::GL OpenGL::GLU ${OPENMP_MODULE})
    set(HW_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/libHWX)
    set(HW_LIBRARY HW)
  endif()
endif()

# Filtervideo and VideoViewer depend on symbols in GradientDomainLoop.cpp so
# let's build that as a library they can link to
file(GLOB GradientDomainLoop_SRC_FILES VideoViewer/GradientDomainLoop.cpp)
add_library(GradientDomainLoop ${GradientDomainLoop_SRC_FILES})
target_include_directories(GradientDomainLoop PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(GradientDomainLoop PUBLIC ${OPENMP_MODULE})

# add_executable_folder(name <ADDITIONAL_LIBRARES> <SRC_FILES>)
function(add_executable_folder name )
  if(DEFINED ARGV1)
    set(${name}_ADDITIONAL_LIBRARES ${ARGV1})
  endif()
  if(DEFINED ARGV2)
    set(${name}_SRC_FILES ${ARGV2})
  else()
    file(GLOB ${name}_SRC_FILES ${name}/*.cpp)
  endif()
  add_executable(${name} ${${name}_SRC_FILES})
  target_include_directories(${name} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${HW_INCLUDE_DIR} ${${name}_ADDITIONAL_INCLUDE_DIRS})
  target_link_libraries(${name} PUBLIC Hh ${HW_LIBRARY} ${${name}_ADDITIONAL_LIBRARES} ${OPENMP_MODULE} Threads::Threads)
endfunction()

# Most of the executables are neatly organized by folder so that `name` is
# built from `name/*.cpp` with the same common dependencies.
add_executable_folder(FilterPM)
add_executable_folder(Filtera3d)
add_executable_folder(Filterframe)
add_executable_folder(Filterimage)
add_executable_folder(Filtermesh)
add_executable_folder(Filterprog)
add_executable_folder(MeshDistance)
add_executable_folder(MeshReorder)
add_executable_folder(MeshSimplify)
add_executable_folder(Meshfit)
add_executable_folder(MinCycles)
add_executable_folder(Polyfit)
add_executable_folder(Recon)
add_executable_folder(StitchPM)
add_executable_folder(Subdivfit)
add_executable_folder(Filtervideo GradientDomainLoop)

if(X11_FOUND)
  # G3dVec, G3dOGL, and VideoViewer share symbols from some files in G3dOGL/
  # build as a libG3d
  file(GLOB G3d_SRC_FILES G3dOGL/G3d.cpp G3dOGL/G3ddraw.cpp G3dOGL/G3devent.cpp G3dOGL/G3dio.cpp)
  add_library(G3d ${G3d_SRC_FILES})
  target_include_directories(G3d PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
  target_link_libraries(G3d PUBLIC ${OPENMP_MODULE})

  add_executable_folder(G3dVec G3d)
  add_executable_folder(G3dOGL G3d "G3dOGL/G3dOGL.cpp;G3dOGL/normalmapping.cpp;G3dOGL/PMesh_ogl.cpp;G3dOGL/SCGeomorph.cpp;G3dOGL/SimplicialComplex.cpp;G3dOGL/SplitRecord.cpp;G3dOGL/SRMesh_ogl.cpp")
  add_executable_folder(VideoViewer GradientDomainLoop VideoViewer/VideoViewer.cpp)
endif()
