# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
#rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
library(tidyverse)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes/Misc")

# coerce dataframe into tibble (or read file using "read_csv()")
#data(iris)
#iris <- as_tibble(iris)
#flights <- read_csv("../Data/Flight Delays Data.csv", na = c(""," ","?","NA","na"))

# explore dplyr::filter()
apr1 <- filter(flights, Month == 4, DayofMonth == 1)  # all data for Apr 1
apr_may <- filter(flights, Month %in% c(4, 5))        # all data for Apr or May
flights2 <- filter(flights, !(ArrDelay > 100 | DepDelay < 100))

# explore dplyr::arrange()
apr2 <- arrange(apr1, DepDelay, ArrDelay)   # order DepDelay first, ArrDelay next
apr3 <- arrange(apr1, desc(DepDelay))       # order by descending DepDelay

# explore dplyr::select() and rename()
apr4 <- select(apr1, Year, Month, DepDelay, ArrDelay)   # select columns
apr5 <- select(apr1, -c(Carrier, OriginAirportID, DestAirportID))
apr6 <- select(apr1, DayOfWeek, DayofMonth, Year, everything()) # shuffle columns
apr1 <- rename(apr1, year = Year, dayofmonth = DayofMonth, dayofweek = DayOfWeek)

# explore dplyr:mutate() and dplyr::transmute()
apr1 <- apr1 %>% mutate(gain = ArrDelay - DepDelay, gainPercent = gain/DepDelay)
apr2 <- apr1 %>% transmute(gain = ArrDelay - DepDelay, gainPercent = gain/DepDelay)

# explore dplyr::summarise() with group_by() and n()
by_carrier <- group_by(flights, Year, Month, Carrier)
delay <- summarise(by_carrier,
                   count = n(),
                   meanDepDelay = mean(DepDelay, na.rm = T),
                   meanArrDelay = mean(ArrDelay, na.rm = T),
                   meanDelay = mean(DepDelay, na.rm = T))
delay <- filter(delay, count > 10000, Carrier != "OO")

# all 3 steps above can be done by piping with %>% to avoid intermediate naming
delay <- flights %>%
  group_by(Year, Month, Carrier) %>%
  summarise(
    count = n(),
    meanDepDelay = mean(DepDelay, na.rm = T),
    meanArrDelay = mean(ArrDelay, na.rm = T),
    meanDelay = mean(DepDelay, na.rm = T)
  ) %>%
  filter(count > 10000, Carrier != "OO")
  


# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)
