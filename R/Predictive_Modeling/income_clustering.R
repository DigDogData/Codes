#=============================
# CLUSTERING WITH INCOME DATA
#=============================
# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes")

# attach packages and headers
library(caret)
library(dplyr)
library(factoextra)
library(NbClust)
library(cluster)
library(gridExtra)
source("Libs/impute_NA.R")
source("Libs/to_FACTOR.R")
source("Libs/to_INDICATOR.R")
source("Libs/make_PLOT.R")

#===========================
# get data
#===========================
incomeData <- read.csv("Data/Adult Census Income Binary Classification dataset.csv",
                       check.names = F, strip.white=T, na.strings=c(""," ","?","NA","na"),
                       stringsAsFactors = F)

# truncate data for manageability (to keep dist matrix from being too large)
set.seed(42)
incomeData <- incomeData[sample(1:nrow(incomeData), 2000), ]

#===========================
# prep data
#===========================
# remove unneeded features (including label column 'income')
dropCols <- c('workclass', 'education', 'occupation', 'capital-gain',
              'capital-loss', 'native-country', 'income')
incomeData2 <- incomeData[, !(names(incomeData) %in% dropCols)]

# remove any duplicated rows
incomeData2 <- incomeData2 %>% filter(!duplicated(incomeData2, ))

# impute NA if any (numeric default "knnImpute", categorical default "Unknown")
namesNA <- names(incomeData2)[apply(is.na(incomeData2), 2, any)]
summary(incomeData2[, namesNA])
incomeData2 <- impute.NA(incomeData2)

# transform all character columns to factor/category
cols <- names(incomeData2)[sapply(incomeData2, is.character)]
if(length(cols)>0) incomeData2[, cols] <- to.factor(incomeData2, cols)

# transform all factors to indicator variables (returns a matrix)
incomeDummy <- to.indicator(incomeData2)

# center and scale data
incomeDummy <- scale(incomeDummy)

# convert income label to binary numbers (0, 1) (for later clustering studies)
income <- as.numeric(incomeData$income == ">50K")

#===================================
# dimensionality reduction with PCA
#===================================
income.pr <- prcomp(incomeDummy, scale = F, center = F)
#summary(income.pr)

# scatterplot observations by components 1 & 2
print(plot(income.pr$x[, c(1,2)], col = (income + 1), xlab = "PC1", ylab = "PC2"))

# plot variance explained by each PC (scree plot)
pr.var <- income.pr$sdev^2
pve <- pr.var / sum(pr.var)
print(plot(pve, xlab = "Principal COmponent", ylab = "Proportion of Variance Explained",
     ylim = c(0, 1), type = "b"))
# plot cumulative proportion of variance explained
print(plot(cumsum(pve), xlab = "Principal COmponent",
     ylab = "Cumulative Proportion of Variance Explained", ylim = c(0, 1), type = "b"))

# fviz_cluster() below plots PC1 vs PC2 in k-means/PAM clustering

#=======================================
# determine clustering tendency in data
#=======================================
# Hopkin's statistic close to 0 (<< 0.5) suggests data significantly clusterable
set.seed(42)
gradient.color <- list(low = "steelblue", high = "white")
clust.tend <- get_clust_tendency(incomeDummy, n = 50,
                                 gradient = gradient.color, graph = T)
cat(noquote("----------------------------------\n"))
cat(noquote(paste("Hopkin's Statistic =",
                  round(clust.tend$hopkins_stat, digits = 2), "\n")))
#print(clust.tend$plot)

#===========================
# cluster data
#===========================
# determine optimal number of clusters (wss=3, silhouette=2, gap_stat=2)
#print(fviz_nbclust(incomeDummy, FUNcluster = kmeans, method = "wss", verbose = F))
#print(fviz_nbclust(incomeDummy, FUNcluster = kmeans, method = "silhouette", verbose = F))
#print(fviz_nbclust(incomeDummy, FUNcluster = kmeans, method = "gap_stat", verbose = F))
# another method (picks majority of several recommendations)
#res.nbclust <- NbClust(incomeDummy, distance = "euclidean", method = "complete")
#print(fviz_nbclust(res.nbclust))

# do k-means clustering (use 2 clusters) (visualize with first 2 PCs)
set.seed(42)
km.res <- kmeans(incomeDummy, centers = 2, nstart = 25, iter.max = 20)
print(fviz_cluster(km.res, data = incomeDummy,
                   ellipse.type = "convex", geom = "point"))

# do pam clustering
set.seed(42)
pam.res <- pam(incomeDummy, k = 2, metric = "euclidean")
print(fviz_cluster(pam.res, ellipse.type = "convex", geom = "point"))

# do hierarchical clustering
# get distance measure (center and scale as well: stand = TRUE)
#dataDist <- get_dist(incomeDummy, method = "euclidean")
dataDist <- get_dist(incomeDummy, method = "pearson")

# compute clustering (dendogram cut to 2) (plot takes too long for >100 points)
res.hc <- hclust(dataDist, method = "ward.D2")
#print(fviz_dend(res.hc, k = 2, cex = 0.5, rect = T,
#                show_labels = F, color_labels_by_k = F, ylab = ""))

#======================================
# examine clustering of label "income"
#======================================
cat(noquote("----------------------------------\n"))
cat(noquote("Data grouping =>\n"))
print(table(income))
cat(noquote("----------------------------------\n"))
cat(noquote("K-means cluster grouping =>\n"))
print(table(km.res$cluster, income))
cat(noquote("----------------------------------\n"))
cat(noquote("PAM cluster grouping =>\n"))
print(table(pam.res$clustering, income))
cat(noquote("----------------------------------\n"))
res.hc.cuts <- cutree(res.hc, k = 2)
cat(noquote("hierarchical cluster grouping =>\n"))
print(table(res.hc.cuts, income))
cat(noquote("----------------------------------\n"))

#==========================
# examine PCA & clustering
#==========================
# get minimum number of PCs required to describe at least 90% of data variability
num <- as.numeric(which(summary(income.pr)$importance[3,] > 0.9)[1])

# create hclust model using this minimal set of PCs
income.pr.hc <- hclust(dist(income.pr$x[, 1:num]), method = "complete")

# cut tree at 2 clusters
income.pr.hc.clust <- cutree(income.pr.hc, k = 2)

# examine PCA clustering of income
cat(noquote("PCA cluster grouping =>\n"))
print(table(income.pr.hc.clust, income))
cat(noquote("----------------------------------\n"))

#========================================
# plot clustering of predictors/response
#========================================
# first add income column and all cluster assignments to incomeData2
incomeData2$income <- as.factor(incomeData$income)
incomeData2$kmeans <- as.factor(km.res$cluster)
incomeData2$pam <- as.factor(pam.res$clustering)
incomeData2$hclust <- as.factor(res.hc.cuts)
incomeData2$pc <- as.factor(income.pr.hc.clust)

# boxplot of age (numeric variable) grouped by clustering assignment
p1 <- box.group.plots(incomeData2, "kmeans", "age")
p2 <- box.group.plots(incomeData2, "pam", "age")
p3 <- box.group.plots(incomeData2, "hclust", "age")
p4 <- box.group.plots(incomeData2, "pc", "age")
grid.arrange(p1, p2, p3, p4, ncol = 2)

# barplot of income (categorical variable) grouped by clustering assignment
formula <- as.formula(". ~ income")
p1 <- bar.facet.plots(incomeData2, "kmeans", formula)
p2 <- bar.facet.plots(incomeData2, "pam", formula)
p3 <- bar.facet.plots(incomeData2, "hclust", formula)
p4 <- bar.facet.plots(incomeData2, "pc", formula)
grid.arrange(p1, p2, p3, p4, ncol = 2)

formula1 <- as.formula(". ~ kmeans")
formula2 <- as.formula(". ~ pam")
formula3 <- as.formula(". ~ hclust")
formula4 <- as.formula(". ~ pc")
p1 <- bar.facet.plots(incomeData2, "income", formula1)
p2 <- bar.facet.plots(incomeData2, "income", formula2)
p3 <- bar.facet.plots(incomeData2, "income", formula3)
p4 <- bar.facet.plots(incomeData2, "income", formula4)
grid.arrange(p1, p2, p3, p4, ncol = 2)


detach(package:gridExtra)
detach(package:cluster)
detach(package:NbClust)
detach(package:factoextra)
detach(package:caret)
detach(package:dplyr)
