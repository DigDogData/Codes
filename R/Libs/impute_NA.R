#========================================================
# FUNCTION TO IMPUTE NA FOR NUMERIC AND CATEGORICAL DATA
#========================================================
impute.NA <- function(df, num.impute = TRUE, char.impute = TRUE,
                      method = "knnImpute", val = "Unknown"){
  
  # get NA column names
  cols <- names(df)
  colChar <- cols[sapply(df, is.character)]     # all character columns
  colNum <- cols[!(cols %in% colChar)]          # all numeric columns
  colNA <- cols[apply(is.na(df), 2, any)]       # columns with NA values
  
  # if there is no NA
  if(length(colNA) == 0){
    cat(noquote("----------------------------------------------\n"))
    cat(noquote("There are no missing/NA values in the data\n"))
    cat(noquote("----------------------------------------------\n"))
  }

  # else if there is NA
  else{
    colCharNA <- intersect(colChar, colNA)
    colNumNA <- intersect(colNum, colNA)
    if(length(colCharNA) > 0){
      cat(noquote("-----------------------------------------------\n"))
      cat(noquote("These categorical Variables have NA values =>\n"))
      print(colCharNA)
      cat(noquote("-----------------------------------------------\n"))
    }
    if(length(colNumNA) > 0){
      cat(noquote("-----------------------------------------------\n"))
      cat(noquote("These numerical Variables have NA values =>\n"))
      print(colNumNA)
      cat(noquote("-----------------------------------------------\n"))
    }
    
    # do medianImpute/knnImpute/bagImpute for numrical NA
    if(num.impute & length(colNumNA)>0){
      suppressMessages(library(caret))
    
      # if medianImpute is needed
      if(method == "medianImpute"){
        pre <- preProcess(df, method=method)
        df <- predict(pre, df)
      }

      # or if knnImpute is needed
      else if(method == "knnImpute"){
      
        # do imputation (also does z-score transform of ALL numeric columns)
        pre <- preProcess(df, method = method)
        dfImpute <- predict(pre, df)
      
        # transform ALL numeric columns back to original scale
        fun <- function(x) dfImpute[,x] * sd(df[,x], na.rm=T) + mean(df[,x], na.rm=T)
        df[, colNum] <- sapply(colNum, fun)
      }
    
      # or if bagImpute is needed
      else{
      
        # generate dummy (indicator) variables
        dummy.vars <- dummyVars(~ ., data=df)
        dfDummy <- predict(dummy.vars, df)
      
        # do imputation
        pre <- preProcess(dfDummy, method=method)
        dfImpute <- predict(pre, dfDummy)
        df[, colNumNA] <- dfImpute[, colNumNA]
      }
    }
  
    # impute categorical NA by val
    if(char.impute & length(colCharNA)>0){
    
      func <- function(x){
        df[, x][is.na(df[, x])] <- val
        df[, x]
      }
      df[, colCharNA] <- lapply(colCharNA, func)
    }
  }
  
  df
}
