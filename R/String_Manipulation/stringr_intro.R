# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
library(stringr)
library(babynames)
myEnv <- new.env()
sys.source("C:/Users/Roy/Documents/Data Analysis/RLibs/detach_ALL.R", envir = myEnv)
attach(myEnv)

#===========================
# get data
#===========================
data("babynames")

# get boy and girl names for year 2014
babynames_2014 <- subset(babynames, year == 2014)
babynames_boy <- subset(babynames_2014, sex == "M")
babynames_girl <- subset(babynames_2014, sex == "F")
boy_names <- babynames_boy$name
girl_names <- babynames_girl$name

#===========================
# use str_length()
#===========================
# get character length of each name
boy_length <- str_length(boy_names)
girl_length <- str_length(girl_names)

# confirm str_length() works with factors
#print(head(str_length(factor(boy_names))))

#===========================
# use str_sub()
#===========================
# get first 3 letters of each boy name
boy_first3_letters <- str_sub(boy_names, 1, 3)

# get last 3 letters of each girl name
girl_last3_letters <- str_sub(girl_names, -3, -1)

#===========================
# use str_detect()
#===========================
# look for pattern "zz" in boy names
contains_zz <- str_detect(boy_names, pattern = fixed("zz"))

#===========================
# use str_subset()
#===========================
# find girl names that contain "U" and "z"
contains_U <- str_subset(girl_names, pattern = fixed("U"))
contains_Uz <- str_subset(contains_U, pattern = fixed("z"))
#print(head(contains_Uz))

#===========================
# use str_count()
#===========================
# count occurrences of "a" in each girl_names
count_a <- str_count(girl_names, pattern = fixed("a"))

# count occurrences of "z" in each girl_names
count_z <- str_count(girl_names, pattern = fixed("z"))

# subset girl_names with at least 4 total a+z
total_count <- count_a + count_z
#print(head(girl_names[total_count >= 4]))

#===========================
# use str_split()
#===========================
date_ranges <- c("23.01.2017 - 29.01.2017", "30.01.2017 - 06.02.2017")

# split dates by "-"
split_dates <- str_split(date_ranges, pattern = fixed(" - "))
#print(split_dates)
split_dates <- str_split(date_ranges, pattern = fixed(" - "), simplify = T, n = 2)
#print(split_dates)

start_dates <- split_dates[, 1]
end_dates <- split_dates[, 2]

# split start_dates into day, month and year
dmy <- str_split(start_dates, pattern = fixed("."), simplify = T)
#print(dmy)

# split start_dates into day, and month.year
dmy <- str_split(start_dates, pattern = fixed("."), simplify = T, n = 2)
#print(dmy)

#=========================
# do some text statistics
#=========================
line1 <- "The table was a large one, but the three were all crowded together at one corner of it:"
line2 <- "\"No room! No room!\" they cried out when they saw Alice coming."
line3 <- "\"There's plenty of room!\" said Alice indignantly, and she sat down in a large arm-chair at one end of the table."
lines <- c(line1, line2 , line3)

# split lines into words
words <- str_split(lines, pattern = fixed(" "))

# count number of words in each line
#print(lapply(words, length))

# average word length per line
words_lengths <- lapply(words, str_length)
#print(lapply(words_lengths, mean))

#=============================
# do some string replacements
#=============================
ids <- c("ID#: 192", "ID#: 118", "ID#: 001")
phone_numbers <- c("510-555-0123", "541-555-0167")

# extract ID numbers
id_nums <- str_replace(ids, "ID#: ", "")
id_nums <- as.numeric(id_nums)
#print(id_nums)

# turn phone numbers into formalt xxx.xxx.xxxx
#print(str_replace_all(phone_numbers, fixed("-"), "."))

#=============================
# do some gene manipulation
#=============================
# code 3 gene sequences from the genome of Yersinia pestis
gene1 <- "TTAGAGTAAATTAATCCAATCTTTGACCCAAATCTCTGCTGGATCCTCTGGTATTTCATGTTGGATGACGTCAATTTCTAATATTTCACCCAACCGTTGAGCACCTTGTGCGATCAATTGTTGATCCAGTTTTATGATTGCACCGCAGAAAGTGTCATATTCTGAGCTGCCTAAACCAACCGCCCCAAAGCGTACTTGGGATAAATCAGGCTTTTGTTGTTCGATCTGTTCTAATAATGGCTGCAAGTTATCAGGTAGATCCCCGGCACCATGAGTGGATGTCACGATTAACCACAGGCCATTCAGCGTAAGTTCGTCCAACTCTGGGCCATGAAGTATTTCTGTAGAAAACCCAGCTTCTTCTAATTTATCCGCTAAATGTTCAGCAACATATTCAGCACTACCAAGCGTACTGCCACTTATCAACGTTATGTCAGCCAT"
gene2 <- "TTAAGGAACGATCGTACGCATGATAGGGTTTTGCAGTGATATTAGTGTCTCGGTTGACTGGATCTCATCAATAGTCTGGATTTTGTTGATAAGTACCTGCTGCAATGCATCAATGGATTTACACATCACTTTAATAAATATGCTGTAGTGGCCAGTGGTGTAATAGGCCTCAACCACTTCTTCTAAGCTTTCCAATTTTTTCAAGGCGGAAGGGTAATCTTTGGCACTTTTCAAGATTATGCCAATAAAGCAGCAAACGTCGTAACCCAGTTGTTTTGGGTTAACGTGTACACAAGCTGCGGTAATGATCCCTGCTTGCCGCATCTTTTCTACTCTTACATGAATAGTTCCGGGGCTAACAGCGAGGTTTTTGGCTAATTCAGCATAGGGTGTGCGTGCATTTTCCATTAATGCTTTCAGGATGCTGCGATCGAGATTATCGATCTGATAAATTTCACTCAT"
gene3 <- "ATGAAAAAACAATTTATCCAAAAACAACAACAAATCAGCTTCGTAAAATCATTCTTTTCCCGCCAATTAGAGCAACAACTTGGCTTGATCGAAGTCCAGGCTCCTATTTTGAGCCGTGTGGGTGATGGAACCCAAGATAACCTTTCTGGTTCTGAGAAAGCGGTACAGGTAAAAGTTAAGTCATTGCCGGATTCAACTTTTGAAGTTGTACATTCATTAGCGAAGTGGAAACGTAAAACCTTAGGGCGTTTTGATTTTGGTGCTGACCAAGGGGTGTATACCCATATGAAAGCATTGCGCCCAGATGAAGATCGCCTGAGTGCTATTCATTCTGTATATGTAGATCAGTGGGATTGGGAACGGGTTATGGGGGACGGTGAACGTAACCTGGCTTACCTGAAATCGACTGTTAACAAGATTTATGCAGCGATTAAAGAAACTGAAGCGGCGATCAGTGCTGAGTTTGGTGTGAAGCCTTTCCTGCCGGATCATATTCAGTTTATCCACAGTGAAAGCCTGCGGGCCAGATTCCCTGATTTAGATGCTAAAGGCCGTGAACGTGCAATTGCCAAAGAGTTAGGTGCTGTCTTCCTTATAGGGATTGGTGGCAAATTGGCAGATGGTCAATCCCATGATGTTCGTGCGCCAGATTATGATGATTGGACCTCTCCGAGTGCGGAAGGTTTCTCTGGATTAAACGGCGACATTATTGTCTGGAACCCAATATTGGAAGATGCCTTTGAGATATCTTCTATGGGAATTCGTGTTGATGCCGAAGCTCTTAAGCGTCAGTTAGCCCTGACTGGCGATGAAGACCGCTTGGAACTGGAATGGCATCAATCACTGTTGCGCGGTGAAATGCCACAAACTATCGGGGGAGGTATTGGTCAGTCCCGCTTAGTGATGTTATTGCTGCAGAAACAACATATTGGTCAGGTGCAATGTGGTGTTTGGGGCCCTGAAATCAGCGAGAAAGTTGATGGCCTGCTGTAA"
genes <- c(YPO0001 = gene1, asnC = gene2, asnA = gene3)

# find number of nucleotides in each sequence
print(str_length(genes))

# find number of "A" in each sequence
print(str_count(genes, fixed("A")))

# return sequences that contain "TTTTTT"
print(str_subset(genes, fixed("TTTTTT")))

# replace all "A" in sequences with "_"
print(str_replace_all(genes, fixed("A"), "_"))


# detach all user-loaded packages and personal environment(s)
detachAll(unload = T)

