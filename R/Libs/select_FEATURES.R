#===================================================================
# FUNCTION TO SELECT IMPORTANT FEATURES AND PLOT IMPORTANT VARIABLES
#===================================================================
select.features <- function(vimp1, vimp2, predictors){
  
  # create dataframe(vimp) with ranked importance > 0
  v1names <- rownames(vimp1)[order(vimp1$Overall, decreasing=T)][vimp1$Overall>0]
  v1scores <- vimp1$Overall[order(vimp1$Overall, decreasing=T)][vimp1$Overall>0]
  vimp1df <- data.frame(name = v1names, score = v1scores)
  v2names <- rownames(vimp2)[order(vimp2$Overall, decreasing=T)][vimp2$Overall>0]
  v2scores <- vimp2$Overall[order(vimp2$Overall, decreasing=T)][vimp2$Overall>0]
  vimp2df <- data.frame(name = v2names, score = v2scores)
  
  # plot vimpdf (top 20 for large dataframe)
  suppressMessages(library(repr))
  suppressMessages(library(gridExtra))
  options(repr.plot.width=8,repr.plot.height=8)
  
  if(nrow(vimp1df) > 20) vimp1df <- vimp1df[1:20,]
  if(nrow(vimp2df) > 20) vimp2df <- vimp2df[1:20,]
  p1 <- ggplot(vimp1df, aes(x=reorder(name, score), y=score)) +
    geom_bar(stat = "identity") +
    xlab("") + ylab("") +
    coord_flip() + 
    ggtitle("Important features")
  p2 <- ggplot(vimp2df, aes(x=reorder(name, score), y=score)) +
    geom_bar(stat = "identity") +
    xlab("") + ylab("Importance") +
    coord_flip() + 
    ggtitle("Important features")
  grid.arrange(p1, p2, nrow = 2)
  
  # return important feature names
  predictors[sapply(predictors, function(x) any(grepl(x,v1names)))]
}
