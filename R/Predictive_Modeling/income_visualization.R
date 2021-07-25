#===========================
# INCOME DATA VISUALIZATION
#===========================
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
data <- read.csv("Data/Adult Census Income Binary Classification dataset.csv",
                 strip.white=T, na.strings=c(""," ","?","NA","na"),
                 stringsAsFactors = F)

# remove any duplicated rows
data <- data %>% filter(!duplicated(data, ))

# replace all categorical NAs by "Unknown"
data <- impute.NA(data, num.impute = F, cat.impute = T, val = "Unknown")

# transform all character columns to factor/category
cols <- names(data)[sapply(data, is.character)]
data[, cols] <- to.factor(data, cols)  # add ", Rname = T" for valid R name

# use intuitive response class names
#levels(incomeData$income) <- c("lo", "hi")

# first, barplot categorical response
response <- "income"
print(bar.plot(data, response))

browser()

# next, histogram and boxplots of all numerical predictors facetted by "income"
facet.formula <- as.formula(paste(". ~", response))
colNums <- names(data)[sapply(data, is.numeric)]
for(i in 1:length(colNums)){
  assign(paste("p", i, sep=""), hist.facet.plots(data, colNums[i], facet.formula))
  assign(paste("q", i, sep=""), box.facet.plots(data, colNums[i], facet.formula))
}
grid.arrange(p1, q1, p2, q2, p3, q3, ncol = 2)
grid.arrange(p4, q4, p5, q5, p6, q6, ncol = 2)

browser()

# next, barplots of all categorical predictors facetted by response
cols <- cols[(!cols %in% response)]
for(i in 1:length(cols))
  assign(paste("p", i, sep=""), bar.facet.plots(data, cols[i], facet.formula))
grid.arrange(p1, p2, p3, p4, ncol = 1)
grid.arrange(p5, p6, p7, p8, ncol = 1)
