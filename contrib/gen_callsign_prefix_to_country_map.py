import plistlib


FILE = "../cty.plist"

with open(FILE, "rb") as cty_plist:
    cty = plistlib.load(cty_plist)
    for key, value in cty.items():
        print(key, value)
