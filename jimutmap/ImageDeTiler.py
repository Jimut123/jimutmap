#!python3

"""
A simple script which converts all the images in
the folder it is run from into a single image.
Images should be in a directory <searchDir>, with
the tiles binned into folders based on their
Y-axis identity, named as their X-axis identity.
In other words, they should be folders of rows
containing column-items for that row of images.

Example:

| tmp/
    |
    | 15/
        | 132.jpg
        | 133.jpg
        | 134.jpg
    | 16/
        | 132.jpg
        | 133.jpg
        | 134.jpg
    | 17/
        | 132.jpg
        | 133.jpg
        | 134.jpg

If run as a script, it will just execute in the
current directory.

License: MIT
Original URL: https://gist.github.com/will-hart/133814e92cf45745e9d1

@author Philip Kahn
@email pkahn@costar.com
"""

import os
from glob import glob
from typing import Tuple, Iterable, Optional
from typing_extensions import Literal
from PIL import Image


class ImageDeTiler():
    """
    Create a composite image from WMTS tiles

    Parameters
    ------------------

    searchDir:str (default= ".")
        Directory to search in

    fileType:str (default= "jpg")
        File type to expect, and to output
    """

    def __init__(self, searchDir:str= ".", fileType:str= "jpg"):
        self._dir = None
        self._tileDimensions = None
        self._yRange = None
        self._xRange = None
        self._folders = None
        fileType = fileType.replace(".","")
        if fileType.lower() not in ImageDeTiler._getAllowedImageTypes():
            raise ValueError(f"Invalid image type `{fileType.lower()}`, must be one of {ImageDeTiler._getAllowedImageTypes()}")
        self.fileType = fileType.lower()
        self.workingDir = searchDir
        self.finalWidth, self.finalHeight = self.getOutputResolution()


    @property
    def workingDir(self) -> str:
        """
        Get the working directory of the instance
        """
        return self._dir

    @workingDir.setter
    def workingDir(self, newDir:str):
        if not os.path.isdir(newDir):
            raise FileNotFoundError(f"`{newDir}` is not a directory")
        self._dir = os.path.normpath(newDir)
        self.folders = frozenset([int(x) for x in os.listdir(self._dir) if not x.startswith(".")])
        xCols = None
        for yDir in self.folders:
            xCheckDir = os.path.join(self._dir, str(yDir))
            if xCols is None:
                xCols = frozenset([int(os.path.basename(x).replace(f".{self.fileType}", "")) for x in glob(os.path.join(xCheckDir, f"*.{self.fileType}"))])
                self._xRange = (min(xCols), max(xCols))
                if frozenset([x for x in range(self._xRange[0], self._xRange[1] + 1)]) != xCols:
                    raise FileNotFoundError(f"The smallest X tile is {self._xRange[0]} and the largest {self._xRange[1]}; every value in-between must be supplied.")
                continue
            matchCols = frozenset([int(os.path.basename(x).replace(f".{self.fileType}", "")) for x in glob(os.path.join(xCheckDir, f"*.{self.fileType}"))])
            if not matchCols == xCols:
                raise FileNotFoundError(f"Invalid directory structure: all child directories should have identical filenames in the format <xColumnNumber>.{self.fileType}")
        with Image.open(os.path.join(self._dir, str(self.getYTileRange()[0]), f"{self.getXTileRange()[0]}.{self.fileType}")) as image:
            self._tileDimensions = image.size

    @property
    def folders(self) -> tuple:
        """
        Get the collection of child folders being used by this
        instance. If you want the full path, use getFoldersPaths().
        """
        return tuple(self._folders)

    @folders.setter
    def folders(self, yColumns:Iterable):
        yCols = frozenset([int(x) for x in yColumns])
        self._yRange = (min(yCols), max(yCols))
        if frozenset([x for x in range(self._yRange[0], self._yRange[1] + 1)]) != yCols:
            raise FileNotFoundError(f"The smallest Y tile is {self._yRange[0]} and the largest {self._yRange[1]}; every value in-between must be supplied.")
        self._folders = [str(x) for x in sorted(yCols)]

    def getFoldersPaths(self) -> tuple:
        """
        Get the path to each folder to be read by the instance
        """
        return tuple([os.path.join(self.workingDir, x) for x in self.folders])

    def getFileSet(self) -> frozenset:
        """
        Get a set of all the files to be processed by this tiler.
        Helpful if you want to clean up the files once the composite
        has been created.
        """
        builder = list()
        for yDir in self.getFoldersPaths():
            builder += list(glob(os.path.join(yDir, f"*.{self.fileType}")))
        return frozenset(builder)

    def getYTileRange(self) -> Tuple[int, int]:
        """
        Get the min and max value for the tiles in the Y direction
        """
        return self._yRange

    def getXTileRange(self) -> Tuple[int, int]:
        """
        Get the min and max value for the tiles in the X direction
        """
        return self._xRange

    def getXResolution(self) -> int:
        """
        Get the native X resolution of a tile
        """
        return self._tileDimensions[0]

    def getYResolution(self) -> int:
        """
        Get the native Y resolution of a tile
        """
        return self._tileDimensions[1]

    def getOutputResolution(self) -> Tuple[int, int]:
        """
        Get the final output resolution of the stitched image
        """
        xTiles = self.getXTileRange()
        xTiles = max(xTiles) - min(xTiles) + 1
        yTiles = self.getYTileRange()
        yTiles = max(yTiles) - min(yTiles) + 1
        return (xTiles * self.getXResolution(), yTiles * self.getYResolution())


    @staticmethod
    def _getAllowedImageTypes():
        """
        Get the allowed input image types of a tile
        """
        return frozenset([
            "jpg",
            "jpeg",
            "png",
            "bmp"
            ])

    @staticmethod
    def _getImageTypesWithAlphaChannel():
        """
        Get available image types with alpha channel
        """
        return frozenset([
            "png",
            "tiff",
            "apng",
        ]).intersection(ImageDeTiler._getAllowedImageTypes())

    def _getOutputFileColorspace(self) -> Literal["RGBA", "RGB"]:
        """
        Get the output file colorspace for the instanced file type
        """
        # cSpell:words RGBA
        return "RGBA" if self.fileType in ImageDeTiler._getImageTypesWithAlphaChannel() else "RGB"

    def process(self, outputName:str= "output", overrideOutputDir:Optional[str]= None, debug:bool= False) -> str:
        """
        Automatically traverses the directory the script is run from
        and tiles all the images together into a massive super image

        Parameters
        ------------------

        outputName:str (default= "output)
            The file name of the stitched output

        overrideOutputDir:str (default= None)
            When specified, place the output file in this directory.
            If it is not specified or does not exist, the working
            directory when instanced `workingDir` is the output directory.

        Returns: output path of the stitched image
        """
        if outputName.endswith(self.fileType):
            outputName = outputName[:-(len(self.fileType) + 1)]
        if overrideOutputDir is not None and os.path.isdir(overrideOutputDir):
            outputDir = overrideOutputDir
        else:
            outputDir = self.workingDir
        outputPath = os.path.join(outputDir, f"{outputName}.{self.fileType}")
        if debug:
            print("----------------------------------------------")
            print(f"Preparing output image `{outputPath}` at resolution {self.finalWidth}x{self.finalHeight}")
            print("----------------------------------------------")
        builder = Image.new(self._getOutputFileColorspace(), (self.finalWidth, self.finalHeight))
        # Iterate over each row folder and create a row tile
        for i, rowPath in enumerate(self.getFoldersPaths()):
            if debug:
                print("----------------------------------------------")
                print(f"Processing row #{i + 1}")
                print("----------------------------------------------")
            row = self.getCompositedXTiles(rowPath)
            # Paste this row into the building image
            builder.paste(row, (0, i * self.getYResolution()))
        builder.save(outputPath)
        if debug:
            print("==============================================\n")
        return outputPath

    def getCompositedXTiles(self, path:str, debug:bool= False) -> Image.Image:
        """
        Takes a path and returns an image which contains
        all the tiled images, tiled along the X direction

        Parameters
        ------------------

        path:str
            A path to a folder containing all the tiled images.
            Each image should be named for its integer X-tile,
            eg, "127.jpg", and there should be an image for each
            integer in the closed range provided by `getXTileRange()`.
            (Note this is unlike the `range()` method, which is half-open
            at the end)

        Returns: PIL.Image.Image object
        """
        result = Image.new(self._getOutputFileColorspace(), (self.finalWidth, self.getYResolution()))

        for i, colNumber in enumerate(range(self.getXTileRange()[0], self.getXTileRange()[1] + 1)):
            readFile = os.path.join(path, f"{colNumber}.{self.fileType}")
            with Image.open(readFile) as img:
                x, y= img.size
                if debug:
                    print(f"\t{readFile}: {img.mode}, {x}x{y}")
                result.paste(img, (i * self.getXResolution(), 0))
        return result

if __name__ == "__main__":
    ImageDeTiler().process()
