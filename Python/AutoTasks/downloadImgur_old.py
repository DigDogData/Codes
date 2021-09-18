#!/usr/bin/env python3

# downloadImgur.py - Downloads Imgur images based on category
# USAGE: py downloadImgur.py <category> <limit>

import sys
import os
import bs4
import requests
import logging


def main():
    url = "https://imgur.com"
    downloadImgur(url)


def downloadImgur(url):

    # set logging config
    logging.basicConfig(
        # level=logging.DEBUG,  # lowest logging level (includes DEBUG messages)
        level=logging.INFO,  # next lowest level (excludes DEBUG messages)
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # logging.disable(logging.CRITICAL)  # uncomment to disable logging

    # get category and limit from CLI
    if len(sys.argv) == 3:
        category = sys.argv[1]
        limit = sys.argv[2]
    else:
        sys.exit("USAGE: python downloadImgur.py <category> <limit>")

    # make request to Imgur
    category_src = url + "/search?q=" + category
    logging.info("Category URL: " + category_src)
    try:
        res = requests.get(category_src)
        res.raise_for_status()  # util's raiseStatus() module does not work here
    except Exception as err:
        logging.error(str(err))
        sys.exit(1)

    # find all images for this category
    soup = bs4.BeautifulSoup(res.text, "lxml")
    image_coun_elem = soup.select(".sorting-text-align > i")  # inspect to find filter
    image_count = image_coun_elem[0].getText()
    print("------------------------------------------")
    print("There are %s images about '%s'." % (image_count, category))
    print("Downloading first %s images..." % limit)
    print("------------------------------------------")
    image_list = soup.select(".image-list-link > img")

    os.makedirs("imgur", exist_ok=True)  # create ./imgur directory

    # loop through images and download each image
    for i in range(int(limit)):
        image = image_list[i]
        image_url = "https:" + image.get("src")
        logging.info("Image URL: " + image_url)

        # make request to image source
        try:
            image_res = requests.get(image_url)
            image_res.raise_for_status()
            image_name = os.path.basename(image_url)
            imageFile = open(os.path.join("imgur", image_name), "wb")
            for chunk in image_res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            logging.info("Image " + image_name + " saved.")
        except Exception as err:
            logging.error("Image Download Error: " + str(err))
            pass


if __name__ == "__main__":
    main()
