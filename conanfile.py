from conans import ConanFile, CMake
from conans.tools import download
from conans.tools import unzip


class ClapackConan(ConanFile):
    name = "clapack"
    version = "3.2.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    # exports = "CMakeLists.txt"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    clapack_modules = ["blas", "lapack", "libf2c"]
    # exports = "*"

    def source(self):
        self.run("git clone https://github.com/openmeeg/clapack.git ")
    
    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin") # From bin to bin
        self.copy(pattern="*.dylib*", dst="bin", src="lib") 
       
    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(source_dir="clapack", build_dir="build")
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
        suffix = ""
        if self.settings.build_type == "Debug":
            suffix = "d"
        for lib in self.clapack_modules:
            self.cpp_info.libs.append("%s%s" % (lib, suffix))
