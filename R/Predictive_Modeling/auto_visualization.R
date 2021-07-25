#=========================
# AUTO DATA VISUALIZATION
#=========================
# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes")

# attach packages and headers
library(dplyr)
source("Libs/to_FACTOR.R")
source("Libs/impute_NA.R")
source("Libs/make_PLOT.R")

# get data
data <- read.csv("Data/Autos.csv", strip.white = T,
                     na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)
makes <- read.csv("Data/Makes.csv", strip.white = T,
                  na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)

# add make info from makes data
data <- data %>% left_join(makes, by='make.id')

# remove unneeded columns
dropCols <- c('make.id')
data <- data[, !(names(data) %in% dropCols)]

# remove any duplicated rows
data <- data %>% filter(!duplicated(data, ))

# replace all categorical NAs by "Unknown"
data <- impute.NA(data, num.impute = F, cat.impute = T, val = "Unknown")

# transform all character columns to factor/category
cols <- names(data)[sapply(data, is.character)]
data[, cols] <- to.factor(data, cols)  # add ", Rname = T" for valid R name

# first, histogram and boxplot of numerical response
response <- "price"
p1 <- hist.plot(data, response)
p2 <- box.plot(data, response)
grid.arrange(p1, p2, ncol = 2)

browser()

# next, scatterplot of response vs all numerical predictors
colNums <- names(data)[sapply(data, is.numeric)]
colNums <- colNums[(!colNums %in% response)]
for(i in 1:length(colNums))
  assign(paste("p", i, sep=""), scatter.plots(data, colNums[i], response))
grid.arrange(p1, p2, p3, p4, p5, p6, p7, p8, ncol = 4)
grid.arrange(p9, p10, p11, p12, p13, p14, p15, ncol = 4)

browser()

# next, boxplot of response grouped by all categorical predictors
cols <- names(data)[sapply(data, is.factor)]
for(i in 1:length(cols))
  assign(paste("p", i, sep=""), box.group.plots(data, cols[i], response))
grid.arrange(p1, p2, p3, p4, p5, p6, ncol = 2)
grid.arrange(p7, p8, p9, p10, ncol = 2)

browser()

# time to prune some unneeded columns
colNums <- colNums[!(colNums %in% c("symboling", "normalized.losses"))]

# pair plots (with correlation values) of numerical predictors
pair.plots(data, colNums)
