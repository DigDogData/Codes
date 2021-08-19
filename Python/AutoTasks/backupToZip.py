#!/usr/bin/env python3

# backupToZip.py - Backs up an working folder into a zipped archive

import os
import zipfile  # module to zip/unzip files
from pathlib import Path
from datetime import datetime


def main():
    folder = Path.home() / "Documents/Scripts"  # folder to be archived
    backupToZip(folder)


def backupToZip(folder):

    # attach current datetime to archive name
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d_%H:%M:%S")
    root = folder.name  # root path of folder
    zipFilename = root + "_" + dt + ".zip"

    # create zipped file
    print(f"Creating '{zipFilename}'...")
    backupZip = zipfile.ZipFile(zipFilename, "w")

    # walk folder tree and add to zipped file
    # ('arcname' argument avoids archiving absolute path)
    for foldername, subfolders, filenames in os.walk(folder):
        # print(f"Adding files in {foldername}...")
        parentPath = os.path.relpath(foldername, folder)
        arcname = os.path.join(root, parentPath)  # archive name
        backupZip.write(foldername, arcname)
        for filename in filenames:
            filePath = os.path.join(foldername, filename)
            parentPath = os.path.relpath(filePath, folder)
            arcname = os.path.join(root, parentPath)
            backupZip.write(filePath, arcname)

    backupZip.close()

    print("Done.")


if __name__ == "__main__":
    main()
