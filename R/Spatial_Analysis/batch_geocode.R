###########################################################
### CODE RUNS BATCH GEOCODES FOR LIST OF STREET ADDRESSES
###########################################################
# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes/Spatial Analysis")

# get data
crime <- read.csv("../Data/Houston Crime Data/Crime.csv", sep = "|", stringsAsFactors = F)

# get address
addresses <- crime$Location

# function to process google server responses
suppressMessages(library(ggmap))
getGeoDetails <- function(address){
  
  # extract relevant parts of geocode output
  geo_reply <- geocode(address, output = "all", messaging = T, override_limit = T)
  answer <- data.frame(lat = NA, long = NA, formatted_address = NA, address_type = NA, status = NA)
  answer$status <- geo_reply$status
  
  # wait 1 hour if over query limit
  while(geo_reply$status == "OVER_QUERY_LIMIT"){
    cat("OVER QUERY LIMIT - Pausing for 2 mins at ")
    cat(paste(as.character(Sys.time()), "\n"))
    Sys.sleep(2*60)
    geo_reply <- geocode(address, output = "all", messaging = T, override_limit = T)
    answer$status <- geo_reply$status
  }
  
  #return NA if address does not match
  if(geo_reply$status != "OK") return(answer)
  
  #else, store geocode output to dataframe
  answer$lat <- geo_reply$results[[1]]$geometry$location$lat
  answer$long <- geo_reply$results[[1]]$geometry$location$lng
  answer$address_type <- paste(geo_reply$results[[1]]$types, collapse = ',')
  answer$formatted_address <- geo_reply$results[[1]]$formatted_address
  
  return(answer)
}

# initialise a dataframe to hold results
geocoded <- data.frame()

# find starting point of address list (if the script was interrupted)
# by loading temp file (if exists) and counting rows
startindex <- 1
tempfilename <- "temp_geocoded.rds"
if(file.exists(tempfilename)){
  geocoded <- readRDS(tempfilename)
  startindex <- nrow(geocoded) + 1
  cat(paste("Found temp file - resuming from index", startindex, "\n"))
}

# start the geocoding address by address
for(ii in seq(startindex, length(addresses))){
  cat(paste("Working on index", ii, "of", length(addresses), "\n"))
  
  #query google server - will pause here if over the limit
  result <- getGeoDetails(addresses[ii])
  result$index <- ii
  
  #append answer to data file
  geocoded <- rbind(geocoded, result)
  
  #save temporary data
  saveRDS(geocoded, tempfilename)
  
  # flush print to console (if running on R console outside RStudio)
  flush.console()
}

# add latitude and longitude to the main data
crime$lat <- geocoded$lat
crime$long <- geocoded$long

# write to data files
#saveRDS(crime, "temp_geocoded.rds")
write.table(crime, "../Data/Houston Crime Data/Crime_geocoded.csv", quote = F, row.names = F, sep = "|")

# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)   # "unload=F" avoids sp/rgeos package load error
