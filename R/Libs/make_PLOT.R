#=========================================
# FUNCTIONs TO CREATE VISUALIZATION PLOTS
#=========================================
library(ggplot2)
library(gridExtra)
library(GGally)

#===================================
# Histogram plots
#===================================
# vanilla histogram of numerical variable y and binCount = nbin
hist.plot <- function(df, y, nbin = 20){
  title <- paste("Histogram of \"", y, "\"", sep="")
  bw <- (max(df[, y], na.rm=T) - min(df[, y], na.rm=T))/nbin
  ggplot(data = na.omit(df)) +
    geom_histogram(aes_string(x = y), binwidth = bw) +
#    ggtitle(title) +
    ylab("")
}

# this function creates a *facetted* histogram of numerical variable
hist.facet.plots <- function(df, x, formula){
  bw <- (max(df[, x], na.rm=T) - min(df[, x], na.rm=T))/20
  if(bw > 0){
    ggplot(na.omit(df), aes_string(x = x)) +
      geom_histogram(binwidth = bw) +
      facet_grid(formula) +
      theme(axis.title.y = element_blank(),
            axis.text.y = element_blank(),
            axis.ticks.y = element_blank())
  } else{
    cat(noquote(paste("*** Histogram of \"", x, "\" has 0 binwidth ***\n", sep="")))
    ggplot(na.omit(df), aes_string(x = x)) +
      geom_histogram() +
      facet_grid(formula) +
      theme(axis.title.y = element_blank(),
            axis.text.y = element_blank(),
            axis.ticks.y = element_blank())
  }
}

#===================================
# Boxplots
#===================================
# vanilla boxplot of numerical variable y
box.plot <- function(df, y){
  title <- paste("Boxplot of \"", y, "\"", sep="")
  ggplot(data = df) +
    geom_boxplot(aes_string(x = 0, y = y)) +
    xlab("") +
#    ggtitle(title) +
    theme(axis.text.x = element_blank(),
          axis.ticks.x = element_blank())
}

# boxplot of numerical variable y grouped by categorical variable z
box.group.plots <- function(df, z, y, angle = 0){
  ggplot(data = df) +
    geom_boxplot(aes_string(x = z, y = y)) +
    xlab(z) +
    theme(axis.text.x = element_text(angle = angle, hjust = 1))
}

# this function creates a *facetted* boxplot of numerical predictor
box.facet.plots <- function(df, x, formula){
  ggplot(df, aes_string(0, x)) +
    geom_boxplot() +
    xlab("") +
    facet_grid(formula) +
    theme(axis.text.x = element_blank(),
          axis.title.x = element_blank(),
          axis.ticks.x = element_blank())
}

#===================================
# Barplots
#===================================
# vanilla barplot of categorical variable y (with customized data label)
bar.custom.plot <- function(df, y){
  title <- paste("Bar plot of \"", y, "\"", sep="")
  ggplot(data = df) +
    geom_bar(aes_string(x = y), width = 0.5) +
    geom_text(stat="count",
              aes(label = paste(..count.., " (",
                                      round(prop.table(..count..)*100, digits=1),"%",
                                      ")", sep="")), vjust=-0.5) +
    ggtitle(title) +
    theme(axis.text = element_text(size = 11),
          axis.title = element_text(size = 12,face = "bold"),
          axis.title.y = element_blank(),
          axis.text.y = element_blank(),
          axis.ticks.y = element_blank())
}

# vanilla barplot of categorical variable y
# (hjust=0/0.5/1 -> ticklabel left-aligned/centered/right-aligned)
bar.plot <- function(df, y, angle = 0, hjust = 0.5){
  ggplot(data = df) +
    geom_bar(aes_string(x = y), fill = "steelblue") +
    theme(axis.text = element_text(size=12),
          axis.text.x = element_text(angle = angle, hjust = hjust),
          axis.title.x = element_blank(),
          axis.title.y = element_blank()
    )
}

# vanilla barplot with labels
bar.plot2 <- function(df, y, angle = 0, hjust = 0.5){
  theme.size = 12
  geom.text.size = (5/14)*theme.size      # geom_text font size = (14/5)*theme font size
  # create new dataframe 'df2' for counts and rename columns
  df %>% group_by(df[y]) %>% summarise(N=n()) %>% rename(x=y,y=N) -> df2
  ggplot(data = df) +
    geom_bar(aes_string(x = y), fill = "steelblue") +
    geom_text(data = df2,                 # count dataframe df2 for labeling
              aes(x=x, y=y, label=y),     # df2 column names are assigned here
              size = geom.text.size,
              position = position_dodge(width = 0.9),
              vjust = -0.5
    ) +
    theme(axis.text = element_text(size=theme.size),
          axis.text.x = element_text(angle = angle, hjust = hjust),
          axis.title.x = element_blank(),
          axis.title.y = element_blank()
    )
}



# this function creates a *facetted* barplot of categorical predictor
bar.facet.plots <- function(df, x, formula){
  plot <- ggplot(df, aes_string(x = x)) +
    geom_bar() +
    facet_grid(formula) +
    theme(axis.title.y = element_blank())
}

#===================================
# Scatterplots
#===================================
# scatterplot of y vs x
scatter.plots <- function(df, x, y){
  plt <- ggplot(data = df) +
    geom_point(aes_string(x, y))
}

# this function creates a *conditional* scatterplot of numerical response vs predictor x
# conditioned (colored) by categorical predictor x2
scatter.cond.plots <- function(df, x, response, x2){
  plt <- ggplot(df, aes_string(x, response)) +
    geom_point(aes_string(color = x2))
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

#=========================
# correlation pair plots
#=========================
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
