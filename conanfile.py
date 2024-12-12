from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.gnu import PkgConfigDeps
from conan.tools.scm import Git
from conan.tools.files import save, patch, rmdir, mkdir, rename, copy, get, replace_in_file, collect_libs
from conan.tools.build import check_min_cppstd, stdcpp_library
from conan.tools.system.package_manager import Apt

import os
import textwrap

class ClapackConan(ConanFile):
    name = "clapack"
    version = "3.2.1"
    url = "https://github.com/ulricheck/conan-clapack.git"

    short_paths = True
    settings = "os", "compiler", "build_type", "arch"

    options = {"shared": [True, False]}

    default_options = {
        "shared": False,
    }

    # exports = "*"

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        source_url = "https://github.com/ulricheck/clapack/archive/{0}.tar.gz".format(self.version)
        archive_name = "clapack-{0}".format(self.version)
        get(self, source_url, strip_root=True)
       

    def generate(self):
        tc = CMakeToolchain(self)

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            tc.variables[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        tc.cache_variables["CLAPACK_BUILD_TESTING"] = "OFF"

        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

        deps = PkgConfigDeps(self)
        deps.generate()

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()


    def package_info(self):
        #self.cpp_info.defines.append("HAVE_LAPACK")
        clapack_modules = ["blas", "lapack", "f2c"]
        suffix = ""
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                suffix = "d"
        for lib in clapack_modules:
            self.cpp_info.libs.append("%s%s" % (lib, suffix))
