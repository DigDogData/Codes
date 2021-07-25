#=====================================================================
# choose the character in Oscar Wilde's play to act
# based on the number of lines each character gets to play
#=====================================================================
# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
library(stringr)
library(stringi)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

# set working directory
setwd("C:/Users/Roy/Documents/Data Analysis/Codes/String Manipulation")

# read book into R
earnest <- readLines("importance-of-being-earnest.txt")

# get rid of first and last lines
start <- which(str_detect(earnest, fixed("START OF THE PROJECT")))
end <- which(str_detect(earnest, fixed("END OF THE PROJECT")))
earnest <- earnest[(start + 1):(end - 1)]

# split play into intro and play/acts
# first get indices from first line up to line of first act
lines_start <- which(str_detect(earnest, fixed("FIRST ACT")))
indx <- 1:(lines_start - 1)
# next split
intro_text <- earnest[indx]     # intro text before first act begins
play_text <- earnest[-indx]     # play text
# explore first 20 lines of play
#writeLines(play_text[1:20])

# remove all empty lines
play_lines <- play_text[!stri_isempty(play_text)]
#writeLines(play_lines[1:20])

# look for start of line ("^") followed by
# first capital letter ("[A-Z]") followed by
# one or more word characters ("[\\w]+") followed by
# full stop ("\\.")
pattern_1 <- "^[A-Z][\\w]+\\."
#print(str_view(play_lines, pattern_1, match = T))
#print(str_view(play_lines, pattern_1, match = F))

# get subset of lines that match pattern
lines <- str_subset(play_lines, pattern_1)

# get characters from lines
who <- str_extract(lines, pattern_1)
print(unique(who))

# list of characters
characters <- c("Algernon", "Jack", "Lane", "Cecily", "Gwendolen", "Chasuble", 
                "Merriman", "Lady Bracknell", "Miss Prism")

# match start, then character name, then .
pattern_2 <- "^(?:Algernon|Jack|Lane|Cecily|Gwendolen|Chasuble|Merriman|Lady Bracknell|Miss Prism)\\."
#print(str_view(play_lines, pattern_3, match = T))

# pull out characters from matches
lines <- str_subset(play_lines, pattern_2)
who <- str_extract(lines, pattern_2)
#print(unique(who))

# count lines per character (helps you choose the character you'd like to play !)
print(table(who))

# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)

