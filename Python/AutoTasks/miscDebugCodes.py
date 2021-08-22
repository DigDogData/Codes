#!/usr/bin/env python3

# miscDebugCodes.py - Example Codes to debug codes

# raise exception (can use inside try-except block)
# tmp1 = 5
# tmp2 = 1
# if tmp1 != 1:
#    raise Exception("tmp1 must equal 1.")  # rest of the code does not execute
# if tmp2 == 1:
#    raise Exception("tmp2 must not equal 1.")

# assertion (sanity check) (do not use inside try-except block);
# asssertion is programmer error (not user error) check, to be used only when
# program is under development, and  must be allowed to fail if incorrect;
# user should never see it - using inside try-except block allows user to
# turn it off;
# running <python -0 miscDebugCodes.py> skips assert statements
# ages = [26, 57, 92, 54, 22, 15, 17, 80, 47, 73]
# ages.sort()
# assert ages[0] <= ages[-1]  # assert 1st age <= last age (correct, does nothing)
# ages.reverse()
# assert ages[0] <= ages[-1]  # assert 1st age <= last age (incorrect, crashes)

# logging (to display log messages as program runs):
# log messages are intended for programmer, not user (use print for user messages)
import logging

logging.disable(logging.CRITICAL)  # comment/uncomment to enable/disable all logs
logging.basicConfig(
    # filename="myLog.txt",  # stores logs in a file
    level=logging.DEBUG,  # DEBUG is lowest log level, logs everything
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.debug("Start of program")


# function to compute factorial
def factorial(n):
    logging.debug("Start of factorial(%s%%)" % (n))
    total = 1
    # for i in range(n + 1):    # uncomment to introduce error
    for i in range(1, n + 1):
        total *= i
        logging.debug("i is " + str(i) + ", total is " + str(total))
    logging.debug("End of factorial(%s%%)" % (n))
    return total


# print(factorial(5))
logging.debug("End of program")

# various logging levels (DEBUG/INFO/WARNING/ERROR/CRITICAL)
logging.debug("Some debugging details.")
logging.info("The logging module is working.")
logging.warning("An error message is about to be logged.")
logging.error("An error has occurred.")
logging.critical("The program is unable to recover!")
