#=========================================
# FUNCTIONs TO CREATE VISUALIZATION PLOTS
#=========================================
library(ggplot2)
library(gridExtra)
library(GGally)

#===================================
# PLOTS FOR DESCRIPTIVE STATISTICS
#===================================
# this function creates a barplot of categorical response variable by class
bar.plot <- function(df, x){
  title <- paste("Bar plot of \"", x, "\"", sep="")
  print(ggplot(df, aes_string(x = x)) +
          geom_bar(width = 0.5) +
          geom_text(stat="count",
                    aes(label = paste(..count.., " (",
                                      round(prop.table(..count..)*100, digits=1),"%",
                                      ")", sep="")), vjust=-0.5) +
          ggtitle(title) +
          theme(axis.text = element_text(size = 11),
                axis.title = element_text(size = 12,face = "bold"),
                axis.title.y = element_blank(),
                axis.text.y = element_blank(),
                axis.ticks.y = element_blank()))
}

# this function creates a histogram of numerical response
hist.plot <- function(df, x){
  title <- paste("Histogram of \"", x, "\"", sep="")
  bw <- (max(df[, x], na.rm=T) - min(df[, x], na.rm=T))/20
  print(ggplot(na.omit(df), aes_string(x = x)) +
          geom_histogram(binwidth = bw) +
          ggtitle(title) +
          theme(axis.text = element_text(size = 11),
                axis.title = element_text(size = 12,face = "bold"),
                axis.title.y = element_blank(),
                axis.text.y = element_blank(),
                axis.ticks.y = element_blank()))
}

# this function creates a boxplot of numerical response
box.plot <- function(df, x){
  title <- paste("Boxplot of \"", x, "\"", sep="")
  print(ggplot(df, aes_string(0, x)) +
          geom_boxplot() +
          xlab("") +
          ggtitle(title) +
          theme(axis.text = element_text(size = 11),
                axis.title = element_text(size = 12,face = "bold"),
                axis.text.x = element_blank(),
                axis.ticks.x = element_blank()))
}

# this function creates a scatterplot of numerical response vs numerical predictor x
scatter.plots <- function(df, x, response){
  plt <- ggplot(df, aes_string(x, response)) +
    geom_point()
}

# this function creates a boxplot of numerical response grouped by categorical predictor x
box.group.plots <- function(df, x, response){
  plt <- ggplot(df, aes_string(x, response)) +
      geom_boxplot() +
    xlab(x)
}

# this function creates time-series plot of response vs times
time.plots <- function(series, response, hr){
  title <- paste("TS plot of \"", response, "\" at the ", hr, "th hr of the day", sep="")
  df <- data.frame(x = 1:length(series), y = series)
  plt <- ggplot(df, aes(x, y)) +
    geom_line() +
    xlab("day") +
    ylab(response) +
    ggtitle(title)
}

#========================================================================
# plots above are for response variable, those below are for predictors
#========================================================================
# this function creates a histogram of numerical predictor
hist.plots <- function(df, x){
  bw <- (max(df[, x], na.rm=T) - min(df[, x], na.rm=T))/20
  if(bw > 0){
    plt <- ggplot(na.omit(df), aes_string(x = x)) +
      geom_histogram(binwidth = bw) +
      theme(axis.title.y = element_blank(),
            axis.text.y = element_blank(),
            axis.ticks.y = element_blank())
  } else{
    cat(noquote(paste("*** Histogram of \"", x, "\" has 0 binwidth ***\n", sep="")))
    plt <- ggplot(na.omit(df), aes_string(x = x)) +
      geom_histogram() +
      theme(axis.title.y = element_blank(),
            axis.text.y = element_blank(),
            axis.ticks.y = element_blank())
  }
}

# this function creates a *facetted* histogram of numerical predictor
hist.facet.plots <- function(df, x, formula){
  bw <- (max(df[, x], na.rm=T) - min(df[, x], na.rm=T))/20
  if(bw > 0){
    plt <- ggplot(na.omit(df), aes_string(x = x)) +
      geom_histogram(binwidth = bw) +
      facet_grid(formula) +
      theme(axis.title.y = element_blank(),
            axis.text.y = element_blank(),
            axis.ticks.y = element_blank())
  } else{
    cat(noquote(paste("*** Histogram of \"", x, "\" has 0 binwidth ***\n", sep="")))
    plt <- ggplot(na.omit(df), aes_string(x = x)) +
      geom_histogram() +
      facet_grid(formula) +
      theme(axis.title.y = element_blank(),
            axis.text.y = element_blank(),
            axis.ticks.y = element_blank())
  }
}

# this function creates a boxplot of numerical predictor
box.plots <- function(df, x){
  plt <- ggplot(df, aes_string(0, x)) +
    geom_boxplot() +
    xlab("") +
    theme(axis.text.x = element_blank(),
          axis.title.x = element_blank(),
          axis.ticks.x = element_blank())
}

# this function creates a *facetted* boxplot of numerical predictor
box.facet.plots <- function(df, x, formula){
  plt <- ggplot(df, aes_string(0, x)) +
    geom_boxplot() +
    xlab("") +
    facet_grid(formula) +
    theme(axis.text.x = element_blank(),
          axis.title.x = element_blank(),
          axis.ticks.x = element_blank())
}

# this function creates a *conditional* scatterplot of numerical response vs predictor x
# conditioned (colored) by categorical predictor x2
scatter.cond.plots <- function(df, x, response, x2){
  plt <- ggplot(df, aes_string(x, response)) +
    geom_point(aes_string(color = x2))
}

# this function creates a barplot of categorical predictor
bar.plots <- function(df, x){
  plot <- ggplot(df, aes_string(x = x)) +
    geom_bar() +
    theme(axis.title.y = element_blank())
}

# this function creates a *facetted* barplot of categorical predictor
bar.facet.plots <- function(df, x, formula){
  plot <- ggplot(df, aes_string(x = x)) +
    geom_bar() +
    facet_grid(formula) +
    theme(axis.title.y = element_blank())
}

# this function creates correlation pairs plots
pair.plots <- function(df, cols){
  print(ggpairs(na.omit(df), columns = cols))
}

#================================
# PLOTS FOR TIME SERIES ANALYSIS
#================================
# function to plot time series
timeseries.plot <- function(df, x, y){
  title <- paste("Time Series plot of \"", y, "\"", sep="")
  print(ggplot(df, aes_string(x = x, y = y)) +
          geom_line(color = "red", size = 1) +
          ggtitle(title) +
          xlab("") +
          theme(axis.text = element_text(size=11),
                axis.title=element_text(size = 12, face = "bold")))
}

# function to plot ACF & PACF
acf.plots <- function(series, colName){
  conf.level <- 0.95
  ciline <- qnorm((1 - conf.level)/2)/sqrt(length(series))
  a <- acf(series, plot = F)
  dfa <- data.frame(lag = a$lag, acf = a$acf)
  p <- pacf(series, plot = F)
  dfp <- data.frame(lag = p$lag, acf = p$acf)
  
  p1 <- ggplot(dfa, aes(x = lag, y = acf)) +
    geom_hline(aes(yintercept = 0), size = 1) +
    geom_hline(aes(yintercept = ciline), linetype = 2, color = "blue") +
    geom_hline(aes(yintercept = -ciline), linetype = 2, color = "blue") +
    geom_segment(aes(xend = lag, yend = 0), size = 1) +
    xlab("") +
    ylab("ACF") +
    ggtitle(paste("ACF of \"", colName, "\"", sep="")) +
    theme(axis.text=element_text(size = 11),
          axis.title=element_text(size = 12,face = "bold"))
  p2 <- ggplot(dfp, aes(x = lag, y = acf)) +
    geom_hline(aes(yintercept = 0), size = 1) +
    geom_hline(aes(yintercept = ciline), linetype = 2, color = "blue") +
    geom_hline(aes(yintercept = -ciline), linetype = 2, color = "blue") +
    geom_segment(aes(xend = lag, yend = 0), size = 1) +
    xlab("Lag") +
    ylab("PACF") +
    ggtitle(paste("PACF of \"", colName, "\"", sep="")) +
    theme(axis.text=element_text(size = 11),
          axis.title=element_text(size = 12,face = "bold"))
  
  grid.arrange(p1, p2, ncol = 1)
}


