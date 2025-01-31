from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


class Clipper2Conan(ConanFile):
    name = "clipper2"
    version = "1.5.2"

    license = "BSL License"
    author = "Angus Johnson"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "usingz": ["ON", "OFF", "ONLY"]}
    default_options = {"shared": False, "fPIC": True, "usingz": "ON"}

    exports_sources = "CMakeLists.txt","clipper.version.in","Clipper2.pc.cmakein","Clipper2Config.cmake.in","Clipper2Lib/*"

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
        tc.variables["CLIPPER2_USINGZ"] = self.options.usingz
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        if self.options.usingz != "ONLY":
            self.cpp_info.components["clipper2"].set_property("cmake_target_name", "Clipper2::clipper2")
            self.cpp_info.components["clipper2"].set_property("pkg_config_name", "Clipper2")
            self.cpp_info.components["clipper2"].libs = ["Clipper2"]
            if self.settings.os in ["Linux", "FreeBSD"]:
                self.cpp_info.components["clipper2"].system_libs.append("m")

        if self.options.usingz != "OFF":
            self.cpp_info.components["clipper2z"].set_property("cmake_target_name", "Clipper2::clipper2z")
            self.cpp_info.components["clipper2z"].set_property("pkg_config_name", "Clipper2Z")
            self.cpp_info.components["clipper2z"].libs = ["Clipper2Z"]
            self.cpp_info.components["clipper2z"].defines.append("USINGZ")
            if self.settings.os in ["Linux", "FreeBSD"]:
                self.cpp_info.components["clipper2z"].system_libs.append("m")
