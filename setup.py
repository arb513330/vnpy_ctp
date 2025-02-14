import platform
from setuptools import Extension, setup


def get_ext_modules() -> list:
    """
    获取三方模块

    Linux、Windows需要编译封装接口
    Mac由于缺乏二进制库支持无法使用
    """
    # Linux
    if platform.system() == "Linux":
        library_dirs = ["vnpy_ctp/api"]
        extra_compile_flags = [
            "-std=c++17",
            "-O3",
            "-Wno-delete-incomplete",
            "-Wno-sign-compare",
        ]
        extra_link_args = ["-lstdc++"]
        runtime_library_dirs = ["$ORIGIN"]
    # Windows
    elif platform.system() == "Windows":
        library_dirs = ["vnpy_ctp/api/libs", "vnpy_ctp/api"]
        extra_compile_flags = [
            "/MP", "/std:c++17",  # standard
            "/O2", "/Ob2", "/Oi", "/Ot", "/Oy", "/GL",  # Optimization
            "/D_CRT_SECURE_NO_WARNINGS",
            # suppress warning of unsafe functions like fopen, strcpy, etc
            "/D_SILENCE_CXX17_CODECVT_HEADER_DEPRECATION_WARNING"
        ]
        extra_link_args = []
        runtime_library_dirs = []
    else:
        return []

    include_dirs = ["vnpy_ctp/api/include", "vnpy_ctp/api/vnctp"]
    libraries = ["thostmduserapi_se", "thosttraderapi_se"]

    vnctpmd = Extension(
        name="vnpy_ctp.api.vnctpmd",
        sources=["vnpy_ctp/api/vnctp/vnctpmd/vnctpmd.cpp"],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_compile_args=extra_compile_flags,
        extra_link_args=extra_link_args,
        runtime_library_dirs=runtime_library_dirs,
        language="cpp",
    )

    vnctptd = Extension(
        name="vnpy_ctp.api.vnctptd",
        sources=["vnpy_ctp/api/vnctp/vnctptd/vnctptd.cpp"],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_compile_args=extra_compile_flags,
        extra_link_args=extra_link_args,
        runtime_library_dirs=runtime_library_dirs,
        language="cpp",
    )

    return [vnctptd, vnctpmd]


setup(ext_modules=get_ext_modules())
