#=====================================
# RECOMMENDER PROBLEM WITH MOVIE DATA
#=====================================
# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes")

# attach packages and headers
library(recommenderlab)
library(dplyr)

#===========================
# get data
#===========================
movieData <- read.csv("Data/Movie Ratings.csv", strip.white = T,
                     na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)
titles <- read.csv("Data/IMDB Movie Titles.csv", strip.white = T,
                  na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)

# reduce data size for manageability
#set.seed(42)
#movieData <- movieData[sample(1:nrow(movieData), 1000), ]

#===========================
# prep data
#===========================
# add title info from titles data
movieData <- movieData %>% left_join(titles, by=c("MovieId" = "Movie.ID"))

# keep only needed columns
cols <- c("UserId", "Rating", "Movie.Name")
movieData <- movieData[, cols]

# remove any duplicated rows
movieData <- movieData %>% filter(!duplicated(movieData, ))

# reorder columns rating and movie name (needed for next step)
movieData <- movieData[c("UserId", "Movie.Name", "Rating")]

# transform to ratingMatrix object
movieMatrix <- as(movieData, "realRatingMatrix")

# reduce movie numbers (column size) for manageability
set.seed(42)
colIndx <- sample(1:ncol(movieMatrix), 5000)
movieMatrix <- movieMatrix[, colIndx]

# movieMatrix is very sparse => keep only relevant data
movieMatrix <- movieMatrix[rowCounts(movieMatrix) >= 20, ]  # users who rated >=20 movies
movieMatrix <- movieMatrix[, colCounts(movieMatrix) > 0]    # movies rated at least once

# normalize rating data (applied to each row)
#movieMatrix3 <- normalize(movieMatrix2)      # sets all rowMeans = 0
#movieMatrix3 <- normalize(movieMatrix2, method = "Z-score")

# binarize (unnormalized) data (loses info) (needed by some recommenders)
#movieMatrix4 <- binarize(movieMatrix2, minRating = 1)  # movie rated or not
#movieMatrix4 <- binarize(movieMatrix2, minRating = 5)  # movie rated above/below cutoff

#===========================
# split data
#===========================
# create a train+test object using k-fold cross validation
n_fold <- 5                                   # number of folds
keep_items <- 15                              # item numbers per user for training
rating_threshold <- 5                         # threshold for "good" rating
set.seed(42)
scheme <- evaluationScheme(data = movieMatrix,
                           method = "cross-validation",
                           k = n_fold,
                           given = keep_items,
                           goodRating = rating_threshold)

# get train & test dataset from object
trainData <- getData(scheme, "train")       # training set
testKnown <- getData(scheme, "known")       # test set with item used to build recommendation
testUnknown <- getData(scheme, "unknown")   # test set with item used to test recommendation

#======================
# train and score model
#======================
cat(noquote("---------------------------------\n"))
cat(noquote("model training begins...\n"))
start_time <- Sys.time()

# run a number of models
set.seed(42)
algorithms <- list(
  random = list(name = "RANDOM", param = list(normalize = "Z-score")),
  popular = list(name = "POPULAR", param = list(normalize = "Z-score")),
  ubcf = list(name = "UBCF", param = list(normalize = "Z-score", nn = 50)),
  ibcf = list(name = "IBCF", param = list(normalize = "Z-score", k = 50))
)

# first run for next top n movie recommendation list
evTopN <- evaluate(scheme,
                   algorithms,
                   n = c(1, 3, 5, 10, 15, 20),
                   type = "topNList",
                   progress = T)

# next run for ratings
evRating <- evaluate(scheme,
                     algorithms,
                     type = "ratings",
                     progress = T)

end_time <- Sys.time()
cat(noquote("model training ends...\n"))
print(end_time - start_time)
cat(noquote("---------------------------------\n"))

#================
# evaluate model
#================
# plot TPR-FPR & Precision-Recall for topNList results
par(mfrow=c(1, 2))
plot(evTopN, annotate = 2:4, legend = "topleft")
plot(evTopN, "prec/rec", annotate = 2:3, legend = "topright")

# plot RMSE/MSE/MAE for ratings results
par(mfrow=c(1, 1))
plot(evRating, ylim = c(0, 10))


detach(package:dplyr)
detach(package:recommenderlab)
