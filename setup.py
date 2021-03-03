import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jimutmap",
    version="1.3.7",
    author="Jimutmap Contributors",
    author_email="jimutbahanpal@yahoo.com",
    description="To get enormous amount of Apple Maps tile with ease",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jimut123/jimutmap",
    install_requires=['wget','bs4','numpy','tqdm'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

