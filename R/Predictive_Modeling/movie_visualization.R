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
library(ggplot2)
library(gridExtra)
library(dplyr)

movieData <- read.csv("Data/Movie Ratings.csv", strip.white = T,
                     na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)
titles <- read.csv("Data/IMDB Movie Titles.csv", strip.white = T,
                  na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)

# reduce data size for manageability
#set.seed(42)
#movieData <- movieData[sample(1:nrow(movieData), 10000), ]

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

# keep relevant data (users who rated >=20 movies, movies rated >=50 times) to avoid bias
movieMatrix <- movieMatrix[rowCounts(movieMatrix) >= 20,
                           colCounts(movieMatrix) >= 50]

# get ratings data (automatically removes all 0 (missing) ratings)
ratings <- getRatings(movieMatrix)

# plot ratings distribution
ratings <- factor(ratings)
p1 <- qplot(ratings) + ggtitle("Ratings Distribution")

# plot average ratings
avg_ratings <- colMeans(movieMatrix)  # automatically ignores 0 ratings
p2 <- qplot(avg_ratings) +
  stat_bin(binwidth = 0.1) +
  ggtitle("Average ratings distribution")
grid.arrange(p1, p2, ncol = 2)

# get top10 viewed movies
# first, create a dara frame
views_per_movie <- colCounts(movieMatrix)  # views count of movies
table_views <- data.frame(
  movie = names(views_per_movie),
  views = views_per_movie
)
table_views <- table_views[order(table_views$views, decreasing = T), ]
row.names(table_views) <- NULL
# next, plot
print(ggplot(table_views[1:10, ], aes(x = reorder(movie, -views), y = views)) +
        geom_bar(stat = "identity") +
        theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
        xlab("") +
        ggtitle("Top10 Viewed Movies"))


detach(package:gridExtra)
detach(package:ggplot2)
detach(package:dplyr)
detach(package:recommenderlab)
