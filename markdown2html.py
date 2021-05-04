#!/usr/bin/python3
'''Python Module'''
import sys
import hashlib
import re
args = sys.argv
readme_lines = []
html_file = []
symbols = ['#','-','*']
boldOrEm = ['**', '__', ['<b>','</b>'],['<em>','</em>']]

def checkFiles(args):
    '''Function to check and read the readme file from cli'''
    if (len(args) < 3):
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    elif (len(args) == 3):
        try:
            with open(args[1], 'r') as file:
                readme = file.read()
                for line in readme.split("\n"):
                    readme_lines.append(line)
                return(readme_lines)
        except:
            sys.stderr.write("Missing {}\n".format(args[1]))
            exit(1)

def parseHeadings(text, symbol):
    '''Function to parse all heading levels'''
    heading_line = "<h{}>{}</h{}>".format(len(symbol),(' ').join(text), len(symbol))
    return (heading_line)

def parseListItem(text, symbol):
    '''Function to convert list text into li tag items'''
    list_item = "<li>{}</li>".format(('').join(text))
    return(list_item)

def parseParagraph(text):
    '''Function to change any text line into a p tag'''
    paragraph = "<p>{}</p>".format(text)
    return(paragraph)

def changeBoldOrEmphasis(line, replace, tags):
    '''Function to change any text into bold or emphasis tags'''
    changeNeeded = line.count(replace)
    newLine = line
    while (changeNeeded >= 2):
        newLine = newLine.replace(replace, tags[0],1)
        newLine = newLine.replace(replace, tags[1],1)
        changeNeeded -= 2
    return(newLine)

def changeMD5(line):
    '''Function to changes any text between [[]] into MD5 hash'''
    right = line[:line.find('[[')]
    left = line[line.find(']]')+2:]
    text = hashlib.md5(line[line.find('[[')+2:line.find(']]')].encode())
    return ("{}{}{}".format(right,text.hexdigest(),left))

def changeCc(line):
    '''Function to remove any 'C' or 'c' in the text between (( ))'''
    right = line[:line.find('((')]
    left = line[line.find('))')+2:]
    text = line[line.find('((')+2:line.find('))')]
    for char in text:
        if (char == 'C' or char == 'c'):
            text = text.replace(char,'')
    return ("{}{}{}".format(right,text,left))

def parseReadme(readme):
    '''Function that read lines from the README file'''
    for line in range(len(readme)):
        newLine = readme[line]
        if (newLine.count(boldOrEm[0]) >= 2):
            newLine = changeBoldOrEmphasis(newLine, boldOrEm[0], boldOrEm[2])
        if (newLine.count(boldOrEm[1]) >= 2):
            newLine = changeBoldOrEmphasis(newLine, boldOrEm[1], boldOrEm[3])
        if (newLine.find('[[') < newLine.find(']]')):
            newLine = changeMD5(newLine)
        if (newLine.find('((') < newLine.find('))')):
            newLine = changeCc(newLine)
        data = newLine.split(' ')
        if (len(data[0]) > 0):
            symbol = data[0]
            if (symbol[0] in symbols):
                text = data[1:]
            else:
                text = newLine
            if (symbol[0] == '#'):
                html_file.append(parseHeadings(text, symbol))
            elif (symbol[0] == '-'):
                list_item = parseListItem(text, symbol)
                if (('').join(html_file[-1:])[1:3] == 'ul'):
                    prev_items = ('').join(html_file[-1:])[4:-5]
                    list_item = ("{}{}").format(prev_items, list_item)
                    html_file.pop()
                html_file.append("<ul>{}</ul>".format(list_item))
            elif (symbol[0] == '*'):
                list_item = parseListItem(text, symbol)
                if (('').join(html_file[-1:])[1:3] == 'ol'):
                    prev_items = ('').join(html_file[-1:])[4:-5]
                    list_item = ("{}{}").format(prev_items, list_item)
                    html_file.pop()
                html_file.append("<ol>{}</ol>".format(list_item))
            elif (symbol[0] not in symbols):
                html_line = parseParagraph(text)
                if (readme[line-1] != ''):
                    html_line = "<p>{}<br />{}</p>".format(html_file[-1][3:-4], html_line[3:-4])
                    html_file.pop()
                html_file.append(html_line)

def createHTML(data):
    '''Function that takes a list of lines as input and write into the final html file'''
    file = open(args[2], "w")
    for line in data:
        file.write("{}\n".format(line))

#print(*html_file, sep='\n')

if __name__ == "__main__":
    checkFiles(args)
    parseReadme(readme_lines)
    createHTML(html_file)
