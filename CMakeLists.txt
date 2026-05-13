cmake_minimum_required(VERSION 3.15)
project(pypvfs LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# All native sources live alongside the Python package they back.
set(PVFS_CORE_DIR "${CMAKE_SOURCE_DIR}/src/pvfs_tools/Core")

# ---------- libpvfs (the core C++ library) ----------------------------------

add_library(pvfs SHARED
    "${PVFS_CORE_DIR}/pvfs.cpp"
)
target_include_directories(pvfs PRIVATE "${PVFS_CORE_DIR}")
set_target_properties(pvfs PROPERTIES
    OUTPUT_NAME "pvfs"
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "\$ORIGIN"
)

if(MSVC)
    # PVFS_EXPORT = __declspec(dllexport) when building pvfs.dll itself
    # (see src/pvfs_tools/Core/pvfs_global.h).
    target_compile_definitions(pvfs PRIVATE PVFS_LIBRARY)
endif()

# ---------- libpvfs_wrapper (the C ABI surface ctypes loads) ----------------

add_library(pvfs_wrapper SHARED
    "${PVFS_CORE_DIR}/pvfs_wrapper.cpp"
)
target_include_directories(pvfs_wrapper PRIVATE "${PVFS_CORE_DIR}")
target_link_libraries(pvfs_wrapper PRIVATE pvfs)
set_target_properties(pvfs_wrapper PROPERTIES
    OUTPUT_NAME "pvfs_wrapper"
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "\$ORIGIN"
)

# ---------- Platform-specific compile/link tuning ---------------------------

if(MSVC)
    # /wd4251: STL types crossing DLL boundary (intentional in this wrapper).
    target_compile_options(pvfs         PRIVATE /wd4251 /O2)
    target_compile_options(pvfs_wrapper PRIVATE /wd4251 /O2)
    # Match upstream PVFS DLL runtime choice (MD / MDd).
    set_property(TARGET pvfs         PROPERTY MSVC_RUNTIME_LIBRARY
        "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
    set_property(TARGET pvfs_wrapper PROPERTY MSVC_RUNTIME_LIBRARY
        "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
    target_compile_definitions(pvfs         PRIVATE _CRT_SECURE_NO_WARNINGS)
    target_compile_definitions(pvfs_wrapper PRIVATE _CRT_SECURE_NO_WARNINGS)
endif()

if(UNIX AND NOT APPLE)
    # Statically embed libstdc++ / libgcc so the wheel does not require a
    # specific GLIBCXX / CXXABI version on the user's system. Without this,
    # the .so files end up depending on whichever libstdc++ the build host
    # shipped (e.g. GLIBCXX_3.4.32 from GCC 13 on Ubuntu 24.04), which is
    # what silently broke pypvfs 1.0.1 on every pre-Ubuntu-24.04 Linux.
    target_link_options(pvfs         PRIVATE -static-libstdc++ -static-libgcc)
    target_link_options(pvfs_wrapper PRIVATE -static-libstdc++ -static-libgcc)
endif()

# ---------- Install rules (scikit-build-core picks these up) ----------------

# Both shared libraries land next to pvfs_binding.py so ctypes.CDLL() finds
# them by Path(__file__).parent / "<name>".
install(TARGETS pvfs pvfs_wrapper
    LIBRARY DESTINATION pvfs_tools/Core   # .so on Linux / .dylib on macOS
    RUNTIME DESTINATION pvfs_tools/Core   # .dll on Windows
)
