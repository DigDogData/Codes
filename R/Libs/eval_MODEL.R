#==========================================================
# FUNCTIONs TO EVALUATE CLASSIFIER MODEL AND PLOT ROC CURVE
#==========================================================
# function to plot ROC curve
plot.ROC <- function(df){
  
  # compute ROC object for plotting
  roc <- data.frame(fprate = 1 - df$specificities,
                    tprate = df$sensitivities,
                    totrate = df$sensitivities + df$specificities,
                    threshold = df$thresholds)
  
  # find optimal cutoff probability
  xpt <- round(subset(roc, totrate==max(totrate))$fprate, digits=2)
  ypt <- round(subset(roc, totrate==max(totrate))$tprate, digits=2)
  thresh <- round(subset(roc, totrate==max(totrate))$threshold, digits=2)
  annoText <- noquote(paste("p = ", thresh, " (", xpt, ", ", ypt, ")", sep=""))
  
  # plot ROC
  print(ggplot(roc, aes(x=fprate, y=tprate)) +
          geom_line(size=1.2, color="dodgerblue3") +
          geom_point(aes(x=xpt, y=ypt), size=4, color="red4") +
          geom_text(aes(x=xpt, y=ypt), label=annoText, hjust=0, nudge_x=0.03, size=4.5) +
          geom_abline(intercept=0, slope=1, linetype=2) +
          xlab("FP Rate") +
          ylab("TP Rate") +
          ggtitle("ROC Curve") +
          theme(text = element_text(size=14)))
}

#============================
# function to evaluate model
#============================
eval.MODEL <- function(score, obs, prob, plot = T){
  
  # get confusion matrix
  suppressMessages(library(caret))
  cfMatrix <- confusionMatrix(score, obs)
  
  # compute metrics
  accu <- as.numeric(cfMatrix$overall[1])
  prec <- as.numeric(cfMatrix$byClass[5])
  sens <- as.numeric(cfMatrix$byClass[1])
  spec <- as.numeric(cfMatrix$byClass[2])
  fprate <- 1 - spec
  f1score <- as.numeric(cfMatrix$byClass[7])

  # compute ROC object
  suppressMessages(library(pROC))
  pos <- cfMatrix$positive
  rocObj <- roc(response = obs,
                predictor = prob[, pos],
                levels = rev(levels(obs)))
  rocauc <- rocObj$auc
  
  # print metrics and plot ROC curve
  if(plot){
    cat(noquote("=======================================\n"))
    cat(noquote("Confusion Matrix =>\n"))
    print(cfMatrix$table)
    cat(noquote("---------------------------------------\n"))
    cat(noquote(paste("Accuracy =", round(accu, digits=3))), "\n")
    cat(noquote(paste("Precision =", round(prec, digits=3))), "\n")
    cat(noquote(paste("Sensitivity/TPRate/Recall =", round(sens, digits=3))), "\n")
    cat(noquote(paste("Specificity =", round(spec, digits=3))), "\n")
    cat(noquote(paste("FPRate/(1 - Specificity) =", round(fprate, digits=3))), "\n")
    cat(noquote(paste("F1 Score =", round(f1score, digits=3))), "\n")
    cat(noquote(paste("ROC AUC =", round(rocauc, digits=3))), "\n")
    cat(noquote(paste("Positive Label = \"", cfMatrix$positive, "\"", sep="")), "\n")
    cat(noquote("=======================================\n"))
  
    plot.ROC(rocObj)
    plot(rocObj)      # plotter from pROC package
  }
  
  # return metrics
  metrics <- c(ROC = rocauc,
               Accuracy = accu,
               Precision = prec,
               Sensitivity = sens,
               Specificity = spec,
               FPrate = fprate,
               F1Score = f1score)
  return(metrics)
}
