import os
from conans import ConanFile, CMake, tools


class ClapackConan(ConanFile):
    name = "clapack"
    version = "3.2.1"
    url = "https://github.com/ulricheck/conan-clapack.git"

    short_paths = True
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports = "FindCLAPACK.txt"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    # exports = "*"

    def source(self):
        source_url = "https://github.com/ulricheck/clapack/archive/{0}.tar.gz".format(self.version)
        archive_name = "clapack-{0}".format(self.version)
        tools.get(source_url)
        os.rename(archive_name, "source")
    
    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin") # From bin to bin
        self.copy(pattern="*.dylib*", dst="bin", src="lib") 
       
    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        if self.settings.os == "Linux":
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = True
        cmake.configure(source_dir="source")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern='*.h' , dst="include", src="package/include", keep_path=False)
        self.copy(pattern='*.cmake' , dst="cmake", src="package/cmake", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="package/lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="package/lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="package/lib", keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src="package/lib", keep_path=False)  


    def package_info(self):
        self.cpp_info.defines.append("HAVE_LAPACK")
        clapack_modules = ["blas", "lapack", "f2c"]
        suffix = ""
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                suffix = "d"
        for lib in clapack_modules:
            self.cpp_info.libs.append("%s%s" % (lib, suffix))
