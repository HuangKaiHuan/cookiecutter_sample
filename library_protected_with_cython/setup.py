#!/usr/bin/env python

"""The setup script."""

import io
import os
import sys

# Python supported version checks. Keep right after stdlib imports to ensure we
# get a sensible error for older Python versions
if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version >= 3.6 required.")
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools import setup
from setuptools.extension import Extension

import versioneer

sources = ["src"]
exclude = ["__init__.py", "_version.py"]

extensions = []
py_modules = []
for source in sources:
    for dir_path, folder_names, file_names in os.walk(source):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            rel_path = os.path.relpath(file_path, "src")
            file_name_no_ext = os.path.splitext(rel_path.replace(os.sep, "."))[0]
            if file_name.endswith((".pyx", ".py")):
                if file_name not in exclude:
                    extension = Extension(
                        file_name_no_ext,
                        sources=[file_path],
                        extra_compile_args=["-Os", "-g0"],
                        extra_link_args=["-Wl,--strip-all"],
                    )
                    extensions.append(extension)
                else:
                    py_modules.append(file_name_no_ext)


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as fh:
        return fh.read()


readme = read("README.rst")
changelog = read("CHANGELOG.rst")

install_requires = [
    # eg: "numpy==1.11.1", "six>=1.7",
]

extras_require = {
    "dev": [
        "black==20.8b1",
        "isort==5.7.0",
        "flake8==3.8.4",
        "mypy==0.800",
        "pre-commit~=2.10.0",
        "pytest==6.2.2",
        "pytest-cov==2.11.1",
        "tox~=3.21.0",
        "gitchangelog==3.0.4",
        "gitlint==0.15.0",
        "invoke==1.5.0",
    ]
}

setup(
    author="Huang Kai Huan",
    author_email="huang_kh@robotics.robotics.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="An example package. Generated with cookiecutter-rrpylibrary.",
    install_requires=install_requires,
    extras_require=extras_require,
    long_description=readme + "\n\n" + changelog,
    include_package_data=True,
    keywords="library_protected_with_cython",
    name="library_protected_with_cython",
    url="http://192.168.16.33/huang_kh/library_protected_with_cython",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass({"build_ext": build_ext}),
    package_dir={"": "src"},
    ext_modules=cythonize(
        extensions,
        build_dir="build",
        language_level=3,
        compiler_directives=dict(always_allow_keywords=True),
    ),
    py_modules=py_modules,
    packages=[],
    zip_safe=False,
)
