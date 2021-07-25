#=========================
# BIKE DATA VISUALIZATION
#=========================
# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes")

# attach packages and headers
library(dplyr)
source("Libs/to_NAME.R")
source("Libs/to_FACTOR.R")
source("Libs/impute_NA.R")
source("Libs/make_PLOT.R")

# get data
data <- read.csv("Data/Bike Rental UCI dataset.csv", strip.white = T,
                 na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)

# remove any duplicated rows
data <- data %>% filter(!duplicated(data, ))

# replace weekday and month number by name
data$weekday <- to.dayname(data, "weekday")
data$mnth <- to.monthname(data, "mnth")

# remove unneeded columns
dropCols <- c('instant', 'dteday')
data <- data[, !(names(data) %in% dropCols)]

# transform all character columns to factor/category (add some non-char columns)
cols <- names(data)[sapply(data, is.character)]
cols <- c(cols, "season", "yr", "hr", "holiday", "workingday", "weathersit")
data[, cols] <- to.factor(data, cols)  # add ", Rname = T" for valid R name

# reorder day & month factor levels chronoloigcally (default order alphabetical)
data$weekday <- factor(data$weekday, levels = c("Sunday", "Monday", "Tuesday",
                                                "Wednesday", "Thursday", "Friday",
                                                "Saturday"))
data$mnth <- factor(data$mnth, levels = c("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"))

# replace all categorical NAs by "Unknown"
data <- impute.NA(data, num.impute = F, cat.impute = T, val = "Unknown")

# first, histogram and boxplot of numerical response
response <- "cnt"
p1 <- hist.plot(data, response)
p2 <- box.plot(data, response)
grid.arrange(p1, p2, ncol = 2)

browser()

# next, scatterplot of response vs all numerical predictors
colNums <- names(data)[sapply(data, is.numeric)]
colNums <- colNums[(!colNums %in% response)]
for(i in 1:length(colNums))
  assign(paste("p", i, sep=""), scatter.plots(data, colNums[i], response))
grid.arrange(p1, p2, p3, p4, p5, p6, ncol = 2)

browser()

# next, boxplot of response grouped by all categorical predictors
cols <- names(data)[sapply(data, is.factor)]
for(i in 1:length(cols))
  assign(paste("p", i, sep=""), box.group.plots(data, cols[i], response))
grid.arrange(p1, p2, p3, p4, p5, p6, p7, p8, ncol = 2)

browser()

# next, time series plot of response by hour of the day (8th, 12th, 16th, 20th)
i <- 1
for(t in seq(8, 20, by = 4)){
  times <- subset(data$cnt, data$hr == t)
  assign(paste("p", i, sep=""), time.plots(times, response, t))
  i <- i + 1
}
grid.arrange(p1, p2, p3, p4, ncol = 1)

browser()

# pair plots (with correlation values) of numerical predictors
colNums <- c(colNums, response)
pair.plots(data, colNums)
