import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tagged-union",
    version="0.0.1",
    author="Thomas Carotti",
    author_email="thomas@carotti.co.uk",
    description="Python tagged unions (sum type, algebraic data types, etc.) with match capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carotti/tagged-union",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)