from setuptools import setup, find_packages

setup(
    name="GPLC",
    version="1.0.0",
    description="Graphical Propositional Logic Calculator",
    author="Silviu Ciobanica-Mkrtchyan",
    author_email="silviu.cimk@outlook.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add any third-party dependencies here
    ],
    entry_points={
        "console_scripts": [
            "gplc=main:main",
        ],
    },
    python_requires=">=3.13",
)