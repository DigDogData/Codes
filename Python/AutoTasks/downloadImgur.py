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
    image_list = soup.select(".post > .image-list-link")

    os.makedirs("imgur", exist_ok=True)  # create ./imgur directory

    # loop through image thumbnails and make request to image source
    for i in range(int(limit)):
        thumbnail = image_list[i]
        image_url = url + thumbnail.get("href")
        logging.info("Image URL: " + image_url)

        try:
            # make request to image source
            image_res = requests.get(image_url)
            image_res.raise_for_status()
            image_soup = bs4.BeautifulSoup(image_res.text, "lxml")
            image = image_soup.select("img")  # get image
            print(str(image))
            # image_location = image[0].get("src")
            # logging.info("Image Location: " + image_location)
            continue

            # make request to image location and download image
            try:
                image_res2 = requests.get(image_location)
                image_res2.raise_for_status()
                image_name = os.path.basename(image_location)
                imageFile = open(os.path.join("imgur", image_name), "wb")
                for chunk in image_res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                logging.info("Image " + image_name + " saved.")
            except Exception as err:
                logging.error("Image Download Error: " + str(err))
                pass

        except Exception as err:
            logging.error("Image URL Access Error: " + str(err))


if __name__ == "__main__":
    main()
