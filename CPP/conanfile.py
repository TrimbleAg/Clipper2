from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


class Clipper2Conan(ConanFile):
    name = "Clipper2"
    version = "1.2.2"

    license = "BSL License"
    author = "Angus Johnson"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    exports_sources = "CMakeLists.txt","Clipper2Lib/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CLIPPER2_TESTS"] = "OFF"
        tc.variables["CLIPPER2_UTILS"] = "OFF"
        tc.variables["CLIPPER2_EXAMPLES"] = "OFF"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["Clipper2", "Clipper2Z"]
