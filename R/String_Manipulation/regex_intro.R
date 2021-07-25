# restart R-session if needed
#.rs.restartR()

# clear workspace, console and plots
rm(list=ls())
#cat("\014")
if(!is.null(dev.list())) dev.off()

# load packages & personal library functions (hide function list from environment)
library(stringr)
library(htmltools)
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

#==================================
# explore some simple regex coding
#==================================
# Some strings to practice with
x <- c("cat", "coat", "scotland", "tic toc")

# get strings that start with "c"
#print(str_subset(x, "^c"))

# get strings that end with "c"
#print(str_subset(x, "c$"))

# match any character followed by "t"
#print(str_subset(x, ".t"))

# match "t" followed by any character
#print(str_subset(x, "t."))

# match two characters
#print(str_subset(x, ".."))

# match a string with exactly three characters
#print(str_subset(x, "^...$"))

#==================================
# regex coding with babynames data
#==================================
# get boy names that match Jeffrey or Geoffrey (two different ways)
#print(str_subset(boy_names, "(?:Jeffrey|Geoffrey)"))
#print(str_subset(boy_names, "(?:Je|Geo)ffrey"))

# get boy names that match Jeffrey or Geoffrey with all possible endings
#print(str_subset(boy_names, "(?:Je|Geo)ff(?:ry|ery|rey|erey)"))

# match girl names that start with Cath or Kath
#print(str_subset(girl_names, "(?:C|K)ath"))

# match girl names that end with yn or ynne
#print(str_subset(girl_names, "yn(?:|ne)$"))

#==================================
# explore character classes
#==================================
x <- c("grey sky", "gray elephant")

# get vowels in x
vowels <- "[aeiouAEIOU]"
#print(str_view_all(x, vowels))

# get proportion of vowels in boy_names
name_length <- str_length(boy_names)
num_vowels <- str_count(boy_names, vowels)
#print(mean(num_vowels/name_length))

# get everything but vowels (consonants) in x
not_vowels <- "[^aeiouAEIOU]"
#print(str_view_all(x, not_vowels))

# get boy_names with zero-or-more vowels, one-or-more vowels, only vowels, no vowels
zero_or_more_vowels <- "[aeiouAEIOU]*"
one_or_more_vowels <- "[aeiouAEIOU]+"
only_vowels <- "^[aeiouAEIOU]+$"
no_vowels <- "^[^aeiouAEIOU]+$"
#print(str_view(boy_names, zero_or_more_vowels, match = T))
#print(str_view(boy_names, one_or_more_vowels, match = T))
#print(str_view(boy_names, only_vowels, match = T))
#print(str_view(boy_names, no_vowels, match = T))

#=========================================
# get phone numbers from contact info
#=========================================
contact <- c("Call me at 555-555-0191",
             "123 Main St",
             "(555) 555 0191",
             "Phone: 555.555.0191 Mobile: 555.555.0192")

# create pattern segments for phone numbers
open_parenthesis_or_not <- "[\\(]?"
three_digits <- "\\d\\d\\d"
four_digits <- paste0(three_digits, "\\d")
separator <- "[-.() ]"
separator_or_not <- paste0(separator, "*")

# create phone pattern
phone_pattern <- paste0(open_parenthesis_or_not,
                        three_digits,
                        separator_or_not,
                        three_digits,
                        separator_or_not,
                        four_digits)
#print(str_view_all(contact, pattern = phone_pattern))

# extract phone numbers
#print(str_extract(contact, phone_pattern))

# different way, using pattern capture "()"
capture_3_digits <- "(\\d\\d\\d)"
capture_4_digits <- "(\\d\\d\\d\\d)"
phone_pattern <- paste0(capture_3_digits,
                        separator_or_not,
                        capture_3_digits,
                        separator_or_not,
                        capture_4_digits)
phone_numbers <- str_match(contact, phone_pattern)
#print(str_c("(", phone_numbers[, 2], ") ", phone_numbers[, 3], "-", phone_numbers[, 4]))

#phone_numbers <- str_match_all(contact, phone_pattern)
#print(sapply(phone_numbers, function(x) str_c("(", x[2], ") ", x[3], "-", x[4])))

#=========================================
# get age/gender from accident narratives
#=========================================
narratives <- c("19YOM-SHOULDER STRAIN-WAS TACKLED WHILE PLAYING FOOTBALL W/ FRIENDS ",
                "31 YOF FELL FROM TOILET HITITNG HEAD SUSTAINING A CHI ",
                "ANKLE STR. 82 YOM STRAINED ANKLE GETTING OUT OF BED ",
                "TRIPPED OVER CAT AND LANDED ON HARDWOOD FLOOR. LACERATION ELBOW, LEFT. 33 YOF*",
                "10YOM CUT THUMB ON METAL TRASH CAN DX AVULSION OF SKIN OF THUMB ",
                "53 YO F TRIPPED ON CARPET AT HOME. DX HIP CONTUSION ",
                "13 MOF TRYING TO STAND UP HOLDING ONTO BED FELL AND HIT FOREHEAD ON RADIATOR DX LACERATION",
                "14YR M PLAYING FOOTBALL; DX KNEE SPRAIN ",
                "55YOM RIDER OF A BICYCLE AND FELL OFF SUSTAINED A CONTUSION TO KNEE ",
                "5 YOM ROLLING ON FLOOR DOING A SOMERSAULT AND SUSTAINED A CERVICAL STRA IN")

# age patterns with one or two digits
one_digit <- "\\d"
one_digit_or_not <- "[\\d]?"
age <- paste0(one_digit, one_digit_or_not)

# age unit patterns with/out space
space_or_not <- "[\\s]?"
unit <- "(?:YO|YR|MO)"
age_unit <- paste0(space_or_not, unit)

# gender patterns with/out space
male_or_female <- "(?:M|F)"
gender <- paste0(space_or_not, male_or_female)

# extract age/gender from narratives
age_gender_pattern <- paste0(age, age_unit, gender)
age_gender <- str_extract(narratives, age_gender_pattern)
#print(age_gender)

# different way, using pattern capture "()"
one_digit <- "\\d"
one_digit_or_not <- "[\\d]?"
capture_1_or_2_digits <- "([\\d]?\\d)" 
age <- paste0(one_digit, one_digit_or_not)
capture_unit <- "((?:YO|YR|MO))"
capture_m_or_f <- "((?:M|F))"
pattern <- paste0(capture_1_or_2_digits,
                  space_or_not,
                  capture_unit,
                  space_or_not,
                  capture_m_or_f)
#print(str_match(narratives, pattern))

# capture only Y and M in unit column
capture_unit <- "((?:Y|M))"
match_O_or_R <- "(?:O|R)?"
pattern <- paste0(capture_1_or_2_digits,
                  space_or_not,
                  capture_unit,
                  match_O_or_R,
                  space_or_not,
                  capture_m_or_f)
#print(str_match(narratives, pattern))

#===========================================
# parse pieces of age/gender
#===========================================
# extract gender (remove age & units from age_gender and leftover extra space)
age_or_age_unit <- paste0(age, age_unit)
genders <- str_replace(age_gender, age_or_age_unit, replacement = "")
one_or_more_space <- "[\\s]+"
genders <- str_replace(genders, one_or_more_space, replacement = "")
#print(genders)

# extract first word character of age units
times <- str_extract(age_gender, age_unit)
times <- str_extract(times, "\\w")
#print(times)

# extract numeric age
age_numeric <- as.numeric(str_extract(age_gender, age))
#print(age_numeric)

# convert age in months to years
age_yrs <- ifelse(times == "Y", round(age_numeric), round(age_numeric/12, 2))
#print(age_yrs)

# recombine age/gender into neat format
age_gender_neat <- paste0(age_numeric, times, "_", genders)
#print(age_gender)
#print(age_gender_neat)

#===========================================
# clean up messy data
#===========================================
df <- data.frame(person.id = 1:3,
                 fruit = c("apple: 3 Orange : 9 banana:2",
                           "Orange:1 Apple: 3 banana: 10",
                           "banana: 3 Apple: 3 Orange : 04"))

# construct pattern to extract number of apples, oranges and banana
pat1 <- ".*"            # any character (possibly empty) matched at least 0 times
pat2 <- "(?:O|o)range"  # Orange or orange
pat3 <- "[ :]*"         # whitespace or : matched at least 0 times
pat4 <- "([0-9]*)"      # capture any digit matched at least 0 times
pat5 <- ".*"            # any character (possibly empty) matched at least 0 times
pattern <- paste0(pat1, pat2, pat3, pat4, pat5)
orange_nums <- str_replace(df$fruit, pattern, replacement = "\\1")
orange_nums <- as.numeric(orange_nums)
pat2 <- "(?:A|a)pple"   # Apple or apple
pattern <- paste0(pat1, pat2, pat3, pat4, pat5)
apple_nums <- str_replace(df$fruit, pattern, replacement = "\\1")
apple_nums <- as.numeric(apple_nums)
pat2 <- "(?:B|b)anana"   # Banana or banana
pattern <- paste0(pat1, pat2, pat3, pat4, pat5)
banana_nums <- str_replace(df$fruit, pattern, replacement = "\\1")
banana_nums <- as.numeric(banana_nums)

# create clean data
df_clean <- data.frame(person.id = df$person.id,
                       apple = apple_nums,
                       orange = orange_nums,
                       banana = banana_nums)

#===========================================
# capture email addresses
#===========================================
hero_contacts <- c("(wolverine@xmen.com)",
                   "wonderwoman@justiceleague.org",
                   "thor@avengers.com")

# capture email address and parts
word <- "[\\w]+"        # match any word character at least once
cword <- "([\\w]+)"     # capture any word character at least once
email <- paste0(cword, "@", cword, "\\.", cword)
email_parts <- str_match(hero_contacts, email)
#print(email_parts)

# get hosts
#print(paste0(email_parts[, 3], ".", email_parts[, 4]))

#===========================================
# backreferencing captured patterns
#===========================================
# any lower-case letter repeated 3 times (using backreference "\\1" twice)
three_repeats <- "([:lower:])\\1\\1"
#print(str_view(boy_names, three_repeats, match = T))

# any lower-case letter-pair repeated once
two_repeats <- "([:lower:][:lower:])\\1"
#print(str_view(boy_names, two_repeats, match = T))

# any lower-case letter-pair reversed (2nd capture referred first with "\\2")
pair_reversed <- "([:lower:])([:lower:])\\2\\1"
#print(str_view(boy_names, pair_reversed, match = T))

# 4-letter & 6-letter palindrome
name_list <- c("Noah","nosson", "Liam", "otto", "Mason", "abba", "William", "renner")
four_palindrome <- "^([:lower:])([:lower:])\\2\\1$"
six_palindrome <- "^([:lower:])([:lower:])([:lower:])\\3\\2\\1$"
#print(str_extract(name_list, four_palindrome))
#print(str_extract(name_list, six_palindrome))

# replace all digits in "contact" with "X"
print(str_replace_all(contact, "\\d", "X"))


# detach all user-loaded packages and personal environment(s)
detachAll(unload = F)

