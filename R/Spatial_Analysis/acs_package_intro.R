rm(list=ls())

library(acs)

# install API key only once (located in Gmail "Census Data API Key Request")
#api.key.install(key="3667d7caa626883afa0b05c916a7ae363b5349ce")

# create geo.set object (empty placeholder) for geographic data of interest
nyc <- geo.make(state = "NY", county = "New York")

# get data from Census ACS API
# (table "B01003" => total population)
acs.fetch(geography = nyc, endyear = 2011, table.number = "B01003")



# detach all user-loaded packages and personal environment(s)
source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R")
detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
