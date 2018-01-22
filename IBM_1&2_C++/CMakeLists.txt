project (IBM)


cmake_minimum_required(VERSION 2.6)

file(TO_CMAKE_PATH "$ENV{IMAGINEPP_ROOT}" d)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${d}/CMake")

find_package(Imagine)


ImagineAddExecutable(IBM main.cpp hmm.h hmm.cpp models.h models.cpp sentence.h sentence.cpp vocab.h vocab.cpp gl_defs.h array.h array.cpp)
 


ImagineUseModules(IBM Graphics)

ImagineUseModules(IBM Graphics)
