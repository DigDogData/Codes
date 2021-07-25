#========================================
# FUNCTION TO DECOMPOSE TIME-SERIES DATA
#========================================
# function to plot time series decomposition (called from decomp.ts() below)
plot.decomp <- function(df){
  cols <- names(df)[2:5]
  facetname <- as.vector(sapply(cols, function(x) rep(x, nrow(df))))
  value <- as.vector(as.matrix(df[, 2:5]))
  df2 <- data.frame(time = df$time, value = value, facetname = facetname)
  print(ggplot(df2, aes(x = time, y = value)) +
          geom_line(size = 1) +
          facet_wrap(~ factor(facetname,
                              levels = c("original", "trend", "seasonal", "remainder")),
                     ncol = 1,
                     scale = "free_y") +
          xlab("") +
          ylab("") +
          theme(axis.text = element_text(size = 10),
                strip.text.x = element_text(size = 11)))
}


# span denotes fraction of data length for loess window
decomp.ts <- function(df, tseries, span = 0.5, showPlot = F){
  wspan <- span * length(tseries)
  fit <- stl(tseries, s.window = "periodic", t.window = wspan)
  if(showPlot){
    # create decomsposition dataframe for plotting
    df2 <- data.frame(time = as.matrix(time(tseries)),
                      original = as.matrix(tseries),
                      fit$time.series)
    # reorder last three columns
    df2 <- df2[c("time", "original", "trend", "seasonal", "remainder")]
    plot.decomp(df2)
  }
  
  # add decomposition series to original dataframe and return
  cbind(df, as.data.frame(fit$time.series))
}
