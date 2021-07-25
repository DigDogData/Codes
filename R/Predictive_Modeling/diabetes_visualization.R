#=============================
# DIABETES DATA VISUALIZATION
#=============================
# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# get working directory (must be same as that of this code)
setwd("C:/Users/Admin/Documents/Data Analysis/Codes/Predictive Modeling")

# attach packages and headers
library(dplyr)
source("../../RLibs/to_FACTOR.R")
source("../../RLibs/impute_NA.R")
source("../../RLibs/make_PLOT.R")

# get data
data <- read.csv("../../Data/Diabetes Data.csv", strip.white = T,
                 na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)
admitInfo <- read.csv("../../Data/Admissions mapping.csv", strip.white = T,
                  na.strings=c(""," ","?","NA","na"), stringsAsFactors = F)

# add admission type info from admissions data
data <- data %>% left_join(admitInfo, by="admission_type_id")

# remove unneeded columns
dropCols <- c("admission_type_id", "encounter_id", "patient_nbr")
data <- data[, !(names(data) %in% dropCols)]

# remove any duplicated rows
data <- data %>% filter(!duplicated(data, ))

# replace all categorical NAs by "Unknown"
data <- impute.NA(data, num.impute = F, char.impute = T, val = "Unknown")

# transform all character columns to factor/category
cols <- names(data)[sapply(data, is.character)]
data[, cols] <- to.factor(data, cols)  # add ", Rname = T" for valid R name

# first, barplot categorical response
print(p1 <- bar.plot(data, "readmitted"))

browser()

# plot tells us "readmitted" has >2 classes, so create a new column
# "readmitted2" with 2 classes (YES/NO) 
data$readmitted2 <- ifelse(data$readmitted!="NO", "YES", as.character(data$readmitted))
data$readmitted2 <- factor(data$readmitted2)

# make YES positive class, add readmitted barplot to previous one
data$readmitted2 <- factor(data$readmitted2, levels = c("YES","NO"))
response <- "readmitted2"
grid.arrange(p1, bar.plot(data, response), ncol = 2, newpage = F)

browser()

# next, histogram and boxplots of all numerical predictors facetted by "readmitted2"
facet.formula <- as.formula(paste(". ~", response))
colNums <- names(data)[sapply(data, is.numeric)]
for(i in 1:length(colNums)){
  assign(paste("p", i, sep=""), hist.facet.plots(data, colNums[i], facet.formula))
  assign(paste("q", i, sep=""), box.facet.plots(data, colNums[i], facet.formula))
}
grid.arrange(p1, q1, p2, q2, p3, q3, ncol = 2)
browser()
grid.arrange(p4, q4, p5, q5, p6, q6, ncol = 2)
browser()
grid.arrange(p7, q7, p8, q8, p9, q9, ncol = 2)
browser()
grid.arrange(p10, q10, ncol = 2)
browser()

# next, barplots of all categorical predictors facetted by "readmitted2"
cols <- cols[(!cols %in% "readmitted")]
for(i in 1:length(cols))
  assign(paste("p", i, sep=""), bar.facet.plots(data, cols[i], facet.formula))
grid.arrange(p1, p2, p3, p4, ncol = 1)
browser()
grid.arrange(p5, p6, p7, p8, ncol = 1)
browser()
grid.arrange(p9, p10, p11, p12, ncol = 1)
browser()
grid.arrange(p13, p14, p15, p16, ncol = 1)
browser()
grid.arrange(p17, p18, p19, p20, ncol = 1)
browser()
grid.arrange(p21, p22, p23, p24, ncol = 1)
browser()
grid.arrange(p25, p26, p27, p28, ncol = 1)
browser()
grid.arrange(p29, p30, p31, p32, ncol = 1)
browser()
grid.arrange(p33, p34, p35, p36, ncol = 1)
print(p37)
