#!/usr/bin/python3
'''Python Module'''
import sys
args = sys.argv

def checkFiles(args):
    if (len(args) == 1):
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    elif (len(args) == 3):
        try:
            with open(args[1], 'r') as file:
                readme = file.read()
                return(readme)
        except:
            sys.stderr.write("Missing {}\n".format(args[1]))
            exit(1)

checkFiles(args);

def parseReadme(readme):
    symbol = [] #represents the markdown symbol to convert
    for line in readme.split("\n"):
        symbol = line.split(' ')[0]
        print(symbol[0])
        # use if statements to see which symbol is
            #call function for the right symbol and return de line converted
parseReadme(checkFiles(args));