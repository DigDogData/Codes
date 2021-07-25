# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
library(stringi)
library(stringr)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

# get names of rulers from 18th century Vietnamese Tay Son dynasty
tay_son <- c(
  "Nguy\u1ec5n Nh\u1ea1c",
  "Nguy\u1ec5n Hu\u1ec7",
  "Nguy\u1ec5n Quang To\u1ea3n"
)

# convert to separate accents
print(tay_son_separate <- stri_trans_nfd(tay_son))

# view all characters separately
#print(str_extract_all(tay_son_separate, "."))

# view all graphemes
print(str_extract_all(tay_son_separate, "\\X"))


# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)

