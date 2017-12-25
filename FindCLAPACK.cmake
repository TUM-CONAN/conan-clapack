#=============================================================================
# Copyright 2001-2011 Kitware, Inc.
#
# Distributed under the OSI-approved BSD License (the "License");
# see accompanying file Copyright.txt for details.
#
# This software is distributed WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the License for more information.
#=============================================================================
# (To distribute this file outside of CMake, substitute the full
#  License text for the above reference.)

find_path(CLAPACK_INCLUDE_DIR NAMES CLAPACK.h PATHS ${CONAN_INCLUDE_DIRS_CLAPACK})
find_library(CLAPACK_LIBRARY NAMES ${CONAN_LIBS_CLAPACK} PATHS ${CONAN_LIB_DIRS_CLAPACK})

MESSAGE("** CLAPACK ALREADY FOUND BY CONAN!")
SET(CLAPACK_FOUND TRUE)
MESSAGE("** FOUND CLAPACK:  ${CLAPACK_LIBRARY}")
MESSAGE("** FOUND CLAPACK INCLUDE:  ${CLAPACK_INCLUDE_DIR}")

set(CLAPACK_INCLUDE_DIRS ${CLAPACK_INCLUDE_DIR})
set(CLAPACK_LIBRARIES ${CLAPACK_LIBRARY})

mark_as_advanced(CLAPACK_LIBRARY CLAPACK_INCLUDE_DIR)

if(CLAPACK_INCLUDE_DIR AND EXISTS "${CLAPACK_INCLUDE_DIR}/CLAPACK.h")
    file(STRINGS "${CLAPACK_INCLUDE_DIR}/CLAPACK.h" CLAPACK_H REGEX "^#define CLAPACK_VERSION \"[^\"]*\"$")

    string(REGEX REPLACE "^.*CLAPACK_VERSION \"([0-9]+).*$" "\\1" CLAPACK_VERSION_MAJOR "${CLAPACK_H}")
    string(REGEX REPLACE "^.*CLAPACK_VERSION \"[0-9]+\\.([0-9]+).*$" "\\1" CLAPACK_VERSION_MINOR  "${CLAPACK_H}")
    string(REGEX REPLACE "^.*CLAPACK_VERSION \"[0-9]+\\.[0-9]+\\.([0-9]+).*$" "\\1" CLAPACK_VERSION_PATCH "${CLAPACK_H}")
    set(CLAPACK_VERSION_STRING "${CLAPACK_VERSION_MAJOR}.${CLAPACK_VERSION_MINOR}.${CLAPACK_VERSION_PATCH}")

    # only append a TWEAK version if it exists:
    set(CLAPACK_VERSION_TWEAK "")
    if( "${CLAPACK_H}" MATCHES "CLAPACK_VERSION \"[0-9]+\\.[0-9]+\\.[0-9]+\\.([0-9]+)")
        set(CLAPACK_VERSION_TWEAK "${CMAKE_MATCH_1}")
        set(CLAPACK_VERSION_STRING "${CLAPACK_VERSION_STRING}.${CLAPACK_VERSION_TWEAK}")
    endif()

    set(CLAPACK_MAJOR_VERSION "${CLAPACK_VERSION_MAJOR}")
    set(CLAPACK_MINOR_VERSION "${CLAPACK_VERSION_MINOR}")
    set(CLAPACK_PATCH_VERSION "${CLAPACK_VERSION_PATCH}")
endif()