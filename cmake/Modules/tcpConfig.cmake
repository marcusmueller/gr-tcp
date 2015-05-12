INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_TCP tcp)

FIND_PATH(
    TCP_INCLUDE_DIRS
    NAMES tcp/api.h
    HINTS $ENV{TCP_DIR}/include
        ${PC_TCP_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    TCP_LIBRARIES
    NAMES gnuradio-tcp
    HINTS $ENV{TCP_DIR}/lib
        ${PC_TCP_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(TCP DEFAULT_MSG TCP_LIBRARIES TCP_INCLUDE_DIRS)
MARK_AS_ADVANCED(TCP_LIBRARIES TCP_INCLUDE_DIRS)

