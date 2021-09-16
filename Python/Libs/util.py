# This function computes entropy of a decision tree node:
# takes np.array() as parameter
def entropy(n):
    from math import log2

    val = 0.0
    for k in n:
        if k > 0:  # to avoid log(0) error
            p = k / sum(n)
            val += -p * log2(p)
    return round(val, 4)


# This function computes weighted entropy of a decision tree split level:
# takes array of np.array() as parameter
def wentropy(nn):
    val = 0.0
    for n in nn:
        ent = entropy(n)  # entropy of each node in the split
        w = sum(n) / sum(sum(nn))  # weight of that node
        val += w * ent
    return round(val, 4)


# This function pretends not to be a Python script: uses a spoofing algorithm
# to avoid bounceback from Open Street Map (OSM) servers
def image_spoof(self, tile):
    import io
    from urllib.request import urlopen, Request
    from PIL import Image

    url = self._image_url(tile)  # get the url of the street map API
    req = Request(url)  # start request
    req.add_header("User-agent", "Anaconda 3")  # add user agent to request
    fh = urlopen(req)
    im_data = io.BytesIO(fh.read())  # get image
    fh.close()  # close url
    img = Image.open(im_data)  # open image with PIL
    img = img.convert(self.desired_tile_form)  # set image format
    return img, self.tileextent(tile), "lower"  # reformat for cartopy


# This function checks for download error with requests.get() method
def raiseStatus(response):
    try:
        response.raise_for_status()  # call raise_for_status() on response object
    except Exception as exc:
        print("There was a problem: %s" % (exc))
    return None


# This function initiates browser for selenium:
# To use Brave browser, download binary file 'chromedriver' from
# https://sites.google.com/chromium.org/driver/ and add its path
# (chromedriver version must match Chromium version in Brave: Menu->About Brave).
# To use Firefox browser, download binary file 'geckodriver' from
# https://github.com/mozilla/geckodriver/releases and add its path.
def startBrowser(browserType):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service

    if browserType.lower() == "brave":
        # initialize Brave browser
        driverPath = "/home/roy/Downloads/chromedriver"
        bravePath = "/usr/bin/brave-browser"
        profilePath = "/home/roy/.config/BraveSoftware/Brave-Browser"
        options = webdriver.ChromeOptions()
        options.binary_location = bravePath
        options.add_argument("user-data-dir=" + profilePath)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        return webdriver.Chrome(service=Service(driverPath), options=options)
    else:
        # initialize Firefox browser
        driverPath = "/home/roy/Downloads/geckodriver"
        profile = webdriver.FirefoxProfile(
            "/home/roy/.mozilla/firefox/9gm5swsg.default-release"
        )
        return webdriver.Firefox(profile, service=Service(driverPath))


# This function enters login ID and password to a website
def loginToSite(browser, userId, password):
    import pyinputplus as pyip
    from selenium.webdriver.common.by import By

    userElem = browser.find_element(By.ID, userId)
    userId = pyip.inputStr("User ID: ")
    userElem.send_keys(userId)
    passwordElem = browser.find_element(By.ID, password)
    passwd = pyip.inputPassword("Password: ")
    passwordElem.send_keys(passwd)
    passwordElem.submit()
