# ========================================================
# This program fetches tiles from satellites.pro for free.
# OPEN SOURCED UNDER GPL-V3.0.
# Author : Jimut Bahan Pal | jimutbahanpal@yahoo.com
# Project Website: https://github.com/Jimut123/jimutmap
# pylint: disable = global-statement
# cSpell: words imghdr, tqdm, asinh, jimut, bahan
# ========================================================

# https://packaging.python.org/en/latest/tutorials/packaging-projects/

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jimutmap",
    version="1.4.1",
    author="Jimut Bahan Pal and the Jimutmap Contributors",
    author_email="jimutbahanpal@yahoo.com",
    description="To get enormous amount of map tiles with ease",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jimut123/jimutmap",
    install_requires=['certifi==2020.12.5','chardet==4.0.0','chromedriver-autoinstaller==0.2.2','idna==2.10',
                      'numpy==1.19.5','requests==2.25.1','selenium==3.141.0','tqdm==4.53.0','urllib3==1.26.5', 
                      'opencv-python==4.5.5'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

