#================================================================
# FUNCTION TO TRANSFORM ALL CATEGORICAL DATA TO INDICATOR VALUES
#================================================================
to.indicator <- function(df){
  dummy.vars <- dummyVars(~ ., data=df)
  predict(dummy.vars, df)
}
