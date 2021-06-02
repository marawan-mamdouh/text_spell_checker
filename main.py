import PyPDF2
import difflib
import docx
import re


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


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
    words = []
    extension = fileName.split(".")
    if extension[-1] == "pdf":
        file = open(fileName, "rb")
        object = PyPDF2.PdfFileReader(file)
        for i in range(object.getNumPages()):
            page = object.getPage(i)
            page_content = page.extractText()
            for line in page_content.split():
                line = re.sub('[^A-Za-z]+', ' ', line)
                lineWords = line.strip().split()
                for word in lineWords:
                    word = word.lower()
                    if word != "" and not hasNumbers(word):
                        words.append(word)
        file.close()
    elif extension[-1] == "docx":
        doc = docx.Document(fileName)
        fullText = ""
        for para in doc.paragraphs:
            fullText += " " + para.text
        for line in fullText.split():
            line = re.sub('[^A-Za-z]+', ' ', line)
            lineWords = line.strip().split()
            for word in lineWords:
                word = word.lower()
                if word != "" and not hasNumbers(word):
                    words.append(word)
    else:
        file = open(fileName, "r")
        for line in file:
            line = re.sub('[^A-Za-z]+', ' ', line)
            lineWords = line.strip().split()
            for word in lineWords:
                word = word.lower()
                if word != "" and not hasNumbers(word):
                    words.append(word)
        file.close()
    return list(set(words))


def findErrors(dictionaryList, textlist):
    misspellings = []
    for word in textlist:
        if word not in dictionaryList:
            misspellings.append(word)
    return list(set(misspellings))


def suggest(errorList, dictionary):
    for word in errorList:
        suggestion = difflib.get_close_matches(word, dictionary)
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
inputType = input("Enter (1) to check file or Enter (2) to write some words to check : ")
if inputType == "1":
    dictionaryFile = input("Please enter the dictionary file : ")
    textFile = input("Please enter the text file : ")
    dictionaryList = readDictionaryFile(dictionaryFile.strip())
    textlist = readTextFile(textFile.strip())
    errorList = findErrors(dictionaryList, textlist)
    print("errorList -> ", errorList)
    suggest(errorList, dictionaryList)
elif inputType == "2":
    words = []
    dictionaryList = readDictionaryFile("dictionary.txt".strip())
    text = input("write text to check : \n")
    for line in text.split():
        line = re.sub('[^A-Za-z-]+', ' ', line)
        lineWords = line.strip().split()
        for word in lineWords:
            word = word.lower()
            if word != "" and not hasNumbers(word):
                words.append(word)
    errorList = findErrors(dictionaryList, list(set(words)))
    if not errorList:
        print("There is No Errors (^‿^)\n")
    else:
        print("errorList -> ", errorList)
        suggest(errorList, dictionaryList)

    print('''┏━━━━┓┏┓━━━━━━━━━━━┏┓━━━━━━━━━━━┏━┓━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┏┓━┏┓━━━━━━━━━━━━━━━━━━━━━━┏┓━┏┓━━━━━━━━━┏┓━━━━━━━━━━┏┓━━━━━━━━━
┃┏┓┏┓┃┃┃━━━━━━━━━━━┃┃━━━━━━━━━━━┃┏┛━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┏┛┗┓┃┃━━━━━━━━━━━━━━━━━━━━━━┃┃━┃┃━━━━━━━━━┃┃━━━━━━━━━━┃┃━━━━━━━━━
┗┛┃┃┗┛┃┗━┓┏━━┓━┏━┓━┃┃┏┓┏━━┓━━━━┏┛┗┓┏━━┓┏━┓━━━━┏┓┏┓┏━━┓┏┓┏━┓━┏━━┓━━━━┗┓┏┛┃┗━┓┏━━┓━━━━┏━━┓┏━━┓┏━━┓┃┃━┃┃━━━━━┏━━┓┃┗━┓┏━━┓┏━━┓┃┃┏┓┏━━┓┏━┓
━━┃┃━━┃┏┓┃┗━┓┃━┃┏┓┓┃┗┛┛┃━━┫━━━━┗┓┏┛┃┏┓┃┃┏┛━━━━┃┃┃┃┃━━┫┣┫┃┏┓┓┃┏┓┃━━━━━┃┃━┃┏┓┃┃┏┓┃━━━━┃━━┫┃┏┓┃┃┏┓┃┃┃━┃┃━━━━━┃┏━┛┃┏┓┃┃┏┓┃┃┏━┛┃┗┛┛┃┏┓┃┃┏┛
━┏┛┗┓━┃┃┃┃┃┗┛┗┓┃┃┃┃┃┏┓┓┣━━┃━━━━━┃┃━┃┗┛┃┃┃━━━━━┃┗┛┃┣━━┃┃┃┃┃┃┃┃┗┛┃━━━━━┃┗┓┃┃┃┃┃┃━┫━━━━┣━━┃┃┗┛┃┃┃━┫┃┗┓┃┗┓━━━━┃┗━┓┃┃┃┃┃┃━┫┃┗━┓┃┏┓┓┃┃━┫┃┃━
━┗━━┛━┗┛┗┛┗━━━┛┗┛┗┛┗┛┗┛┗━━┛━━━━━┗┛━┗━━┛┗┛━━━━━┗━━┛┗━━┛┗┛┗┛┗┛┗━┓┃━━━━━┗━┛┗┛┗┛┗━━┛━━━━┗━━┛┃┏━┛┗━━┛┗━┛┗━┛━━━━┗━━┛┗┛┗┛┗━━┛┗━━┛┗┛┗┛┗━━┛┗┛━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┏━┛┃━━━━━━━━━━━━━━━━━━━━━━━━┃┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┗━━┛━━━━━━━━━━━━━━━━━━━━━━━━┗┛━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')
