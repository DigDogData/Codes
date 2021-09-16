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
