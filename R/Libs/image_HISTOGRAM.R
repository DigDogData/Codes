#=========================================
# FUNCTION TO CREATE HISTOGRAM OF IMAGE
#=========================================
library(ggplot2)
hist.plot <- function(image){
  data <- imageData(image)
  br = 40     # number of histogram bins 
  mids <- hist(data[ , , 1], breaks = br, plot = F)$mids

  # if RGB image
  if(colorMode(image) > 0){
    countR <- hist(data[ , , 1], breaks = br, plot = F)$counts   # for red channel
    countG <- hist(data[ , , 2], breaks = br, plot = F)$counts   # for green channel
    countB <- hist(data[ , , 3], breaks = br, plot = F)$counts   # for blue channel
    red <- data.frame(mids = mids, counts = countR, color = "red")
    green <- data.frame(mids = mids, counts = countG, color = "green")
    blue <- data.frame(mids = mids, counts = countB, color = "blue")
    hist.df <- rbind(red, green, blue)
    ggplot(hist.df, aes(x = mids, y = counts, fill = color)) +
      geom_bar(stat = "identity", position = "dodge", show.legend = F) +
      xlab("") +
      ylab("") +
      ggtitle("RGB Histogram")
  }

  # else if Grayscale image
  else{
    count <- hist(data[ , , 1], breaks = br, plot = F)$counts
    hist.df <- data.frame(mids = mids, counts = count)
    ggplot(hist.df, aes(x = mids, y = counts)) +
      geom_bar(stat = "identity", fill = "white", color = "black") +
      xlab("") +
      ylab("") +
      ggtitle("Grayscale Histogram")
  }
}
