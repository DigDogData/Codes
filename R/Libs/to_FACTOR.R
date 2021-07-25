#=============================================================================
# FUNCTION TO TRANSFORM CHARACTER COLUMNS TO FACTORS WITH VALID R NAME LEVELS
#=============================================================================
to.factor <- function(df, cols, Rname = FALSE){
  func <- function(x){
    if(Rname) df[, x] <- gsub("([[:alpha:]]+)-([[:alpha:]]+)", "\\1.\\2", df[, x])
#    if(Rname) df[, x] <- gsub("([[:alpha:]]+)[-/]([[:alpha:]]+)", "\\1.\\2", df[, x])
    factor(df[, x])
  }
  lapply(cols, func)
}
