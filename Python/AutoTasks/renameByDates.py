#!/usr/bin/env python3

# renameByDates.py - Add today's date to filenames

import shutil  # import file manipulation module
from pathlib import Path
from datetime import date


def main():

    # get today's date
    today = date.today()
    dt = today.strftime("%m-%d-%Y")  # MM-DD-YYYY format

    addDateToFilename(dt)


def addDateToFilename(dtt):

    # loop over files
    p = Path.cwd()
    p2 = p / "QuizFiles"
    for filename in p2.glob("*answer*"):  # filter by name

        # get parts of file name
        oldName = filename.name  # full filename (with extension)
        shortName = filename.stem  # filename wo extension
        extension = filename.suffix

        # add date to filename
        newName = shortName + "_" + dtt + extension

        # copy to a different folder
        shutil.copy(p2 / oldName, p / "test" / newName)  # copy file
        shutil.move(p2 / oldName, p2 / newName)  # rename file


if __name__ == "__main__":
    main()
