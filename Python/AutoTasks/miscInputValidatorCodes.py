#!/usr/bin/env python3

# miscInputValidator.py - Example Codes to validate formatted inputs

try:
    import pyinputplus as pyip
except ImportError:
    print("Install pyinputplus module")
    pass  # do nothing

# rsp = pyip.inputNum("Enter a number: ")  # integer/float
# rsp = pyip.inputInt("Enter a number: ")  # integer only
# rsp = pyip.inputFloat("Enter a number: ")  # float only
# rsp = pyip.inputNum("Enter a number: ", min=5)  # number >= 5
# rsp = pyip.inputNum("Enter a number: ", greaterThan=5)  # number > 5
# rsp = pyip.inputNum("Enter a number: ", lessThan=10)  # number < 10
# rsp = pyip.inputNum("Enter a number: ", blank=True)  # input optional
# rsp = pyip.inputNum("Enter a number: ", limit=3)  # at most 3 tries
# rsp = pyip.inputNum("Enter a number: ", timeout=10)  # within 10 seconds
# rsp = pyip.inputNum("Enter a number: ", limit=3, defaut="N/A")  # no error
# rsp = pyip.inputNum(allowRegexes=[r"(I|V|X|L|C|D|M])+", r"zero"])  # 42 & XLII work
# rsp = pyip.inputNum(allowRegexes=[r"(i|v|x|l|c|d|m])+", r"zero"])  # 42 & xlii work
# rsp = pyip.inputNum(blockRegexes=[r"[02468]$"])  # xlii works, 42 does not work

# code for how-to-keep-an-idiot-busy-for-hours
while True:
    prompt = "Want to know how to keep and idiot busy for hours?\n"

    # inputYesNo() method returns 'yes' for prompt='yes'/'YES'/'y' and 'no' likewise
    response = pyip.inputYesNo(prompt)

    if response == "no":
        break

print("Thank you. Have a nice day.")
