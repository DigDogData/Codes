#=========================================================
# FUNCTIONS TO RETURN WEEKDAY AND MONTH NAMES FOR NUMBERS
#=========================================================
# returns list of weekday names
to.dayname <- function(df, x){
  namelist <- recode(df[, x],
                     "0" = "Sunday",
                     "1" = "Monday",
                     "2" = "Tuesday",
                     "3" = "Wednesday",
                     "4" = "Thursday",
                     "5" = "Friday",
                     "6" = "Saturday")
  namelist
}

# returns list of month names
to.monthname <- function(df, x){
  namelist <- recode(df[, x],
                     "1" = "Jan",
                     "2" = "Feb",
                     "3" = "Mar",
                     "4" = "Apr",
                     "5" = "May",
                     "6" = "Jun",
                     "7" = "Jul",
                     "8" = "Aug",
                     "9" = "Sep",
                     "10" = "Oct",
                     "11" = "Nov",
                     "12" = "Dec")
  namelist
}

