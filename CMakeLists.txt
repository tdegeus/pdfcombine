
cmake_minimum_required(VERSION 3.0)

project(pdfcombine)

set(PROJECT_BINARIES "pdfcombine")

INSTALL(PROGRAMS ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_BINARIES} DESTINATION bin)
