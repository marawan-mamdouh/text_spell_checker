import difflib
import re

import PyPDF2
import docx

words = []


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def listWords(inputString):
    inputString = re.sub('[^A-Za-z\']+', ' ', inputString)
    for word in inputString.strip().split():
        word = word.lower()
        if word != "" and not hasNumbers(word):
            words.append(word)


def readDictionaryFile(fileName):
    dictionary = []
    file = open(fileName, "r")
    for line in file:
        lineWords = line.strip().split()
        for word in lineWords:
            dictionary.append(word.lower())
    file.close()
    return dictionary


def readTextFile(fileName):
    extension = fileName.split(".")
    if extension[-1] == "pdf":
        file = open(fileName, "rb")
        pdfObject = PyPDF2.PdfFileReader(file)
        for i in range(pdfObject.getNumPages()):
            page = pdfObject.getPage(i)
            fullText = str(page.extractText())
            listWords(fullText)
        file.close()
    elif extension[-1] == "docx":
        docObject = docx.Document(fileName)
        fullText = ""
        for para in docObject.paragraphs:
            fullText += " " + para.text
            listWords(fullText)
    elif extension[-1] == "txt":
        file = open(fileName, "r")
        for line in file:
            listWords(line)
        file.close()
    return list(set(words))


def findErrors(dictionaryWordsList, inputTextList):
    misspellings = []
    for word in inputTextList:
        if word not in dictionaryWordsList:
            misspellings.append(word)
    return list(set(misspellings))


def suggest(misspellings, dictionaryWordsList):
    for word in misspellings:
        suggestion = difflib.get_close_matches(word, dictionaryWordsList)
        print(f"- Did you mean {', '.join(str(x) for x in suggestion)} instead of {word}?")


print('''
╔╗╔╗╔╗──╔╗──────────────╔╗─────╔╗╔╗──────────────╔╗╔╗────╔╗───────╔╗
║║║║║║──║║─────────────╔╝╚╗───╔╝╚╣║──────────────║║║║────║║───────║║
║║║║║╠══╣║╔══╦══╦╗╔╦══╗╚╗╔╬══╗╚╗╔╣╚═╦══╗╔══╦══╦══╣║║║─╔══╣╚═╦══╦══╣║╔╦══╦═╗
║╚╝╚╝║║═╣║║╔═╣╔╗║╚╝║║═╣─║║║╔╗║─║║║╔╗║║═╣║══╣╔╗║║═╣║║║─║╔═╣╔╗║║═╣╔═╣╚╝╣║═╣╔╝
╚╗╔╗╔╣║═╣╚╣╚═╣╚╝║║║║║═╣─║╚╣╚╝║─║╚╣║║║║═╣╠══║╚╝║║═╣╚╣╚╗║╚═╣║║║║═╣╚═╣╔╗╣║═╣║
─╚╝╚╝╚══╩═╩══╩══╩╩╩╩══╝─╚═╩══╝─╚═╩╝╚╩══╝╚══╣╔═╩══╩═╩═╝╚══╩╝╚╩══╩══╩╝╚╩══╩╝
───────────────────────────────────────────║║
───────────────────────────────────────────╚╝
''')
misspellings = []
while 1:
    inputType = input("Enter (1) to check file or Enter (2) to write some words to check : ")
    if inputType == "1":
        while 1:
            dictionaryFileName = input("Please enter the dictionary file (.txt) : ").strip()
            if dictionaryFileName.split(".")[-1] == "txt":
                break
            else:
                print("\nError Enter .txt file")
        while 1:
            textFileName = input("Please enter the text file (.txt, .pdf or .docx) : ").strip()
            if textFileName.split(".")[-1] == "txt" or textFileName.split(".")[-1] == "pdf" or \
                    textFileName.split(".")[-1] == "docx":
                break
            else:
                print("\nError Enter (.txt, .pdf or .docx) file")
        dictionaryWordsList = readDictionaryFile(dictionaryFileName.strip())
        inputTextList = readTextFile(textFileName.strip())
        misspellings = findErrors(dictionaryWordsList, inputTextList)
    elif inputType == "2":
        dictionaryWordsList = readDictionaryFile("dictionary.txt".strip())
        text = input("write text to check : \n")
        listWords(text)
        misspellings = findErrors(dictionaryWordsList, list(set(words)))

    if inputType == "1" or inputType == "2":
        if not misspellings:
            print("\nThere is No misspellings (^‿^)\n")
        else:
            print("\nmisspellings -> ", misspellings, "\n")
            suggest(misspellings, dictionaryWordsList)
        break
    else:
        print("\nPlease Enter Correct Choice", "(1) to check file or (2) to write some words to check")

print('''\n\n┏━━━━┓┏┓━━━━━━━━━━━┏┓━━━━━━━━━━━┏━┓━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┏┓━┏┓━━━━━━━━━━━━━━━━━━━━━━┏┓━┏┓━━━━━━━━━┏┓━━━━━━━━━━┏┓━━━━━━━━━
┃┏┓┏┓┃┃┃━━━━━━━━━━━┃┃━━━━━━━━━━━┃┏┛━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┏┛┗┓┃┃━━━━━━━━━━━━━━━━━━━━━━┃┃━┃┃━━━━━━━━━┃┃━━━━━━━━━━┃┃━━━━━━━━━
┗┛┃┃┗┛┃┗━┓┏━━┓━┏━┓━┃┃┏┓┏━━┓━━━━┏┛┗┓┏━━┓┏━┓━━━━┏┓┏┓┏━━┓┏┓┏━┓━┏━━┓━━━━┗┓┏┛┃┗━┓┏━━┓━━━━┏━━┓┏━━┓┏━━┓┃┃━┃┃━━━━━┏━━┓┃┗━┓┏━━┓┏━━┓┃┃┏┓┏━━┓┏━┓
━━┃┃━━┃┏┓┃┗━┓┃━┃┏┓┓┃┗┛┛┃━━┫━━━━┗┓┏┛┃┏┓┃┃┏┛━━━━┃┃┃┃┃━━┫┣┫┃┏┓┓┃┏┓┃━━━━━┃┃━┃┏┓┃┃┏┓┃━━━━┃━━┫┃┏┓┃┃┏┓┃┃┃━┃┃━━━━━┃┏━┛┃┏┓┃┃┏┓┃┃┏━┛┃┗┛┛┃┏┓┃┃┏┛
━┏┛┗┓━┃┃┃┃┃┗┛┗┓┃┃┃┃┃┏┓┓┣━━┃━━━━━┃┃━┃┗┛┃┃┃━━━━━┃┗┛┃┣━━┃┃┃┃┃┃┃┃┗┛┃━━━━━┃┗┓┃┃┃┃┃┃━┫━━━━┣━━┃┃┗┛┃┃┃━┫┃┗┓┃┗┓━━━━┃┗━┓┃┃┃┃┃┃━┫┃┗━┓┃┏┓┓┃┃━┫┃┃━
━┗━━┛━┗┛┗┛┗━━━┛┗┛┗┛┗┛┗┛┗━━┛━━━━━┗┛━┗━━┛┗┛━━━━━┗━━┛┗━━┛┗┛┗┛┗┛┗━┓┃━━━━━┗━┛┗┛┗┛┗━━┛━━━━┗━━┛┃┏━┛┗━━┛┗━┛┗━┛━━━━┗━━┛┗┛┗┛┗━━┛┗━━┛┗┛┗┛┗━━┛┗┛━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┏━┛┃━━━━━━━━━━━━━━━━━━━━━━━━┃┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┗━━┛━━━━━━━━━━━━━━━━━━━━━━━━┗┛━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')
