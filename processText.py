from nltk.corpus import stopwords

class LinkedinProcessing():
    def __init__(self):
        self.globalHash = {}
    
    def processCharValidity(self, char: str):
        try:
            int(char)
            return False
        except:
            pass
        convertedChar = char.lower()
        if ((ord(convertedChar) >= 97 and ord(convertedChar) <= 122) or convertedChar == " " or convertedChar == "\n"):
            return True
        return False
    
    def processWordValidity(self, word: str):
        wordSet = set(stopwords.words('english'))
        if (word in wordSet):
            return False
        return True

    def processSentence(self, rawText: str):
        splitText = list(rawText)
        cleanedText = []
        for char in splitText:
            if (self.processCharValidity(char)):
                cleanedText.append(char)
        splitWords =  "".join(cleanedText).split()
        cleanedWords = []
        for word in splitWords:
            if self.processWordValidity(word):
                cleanedWords.append(word)
        return cleanedWords

    def pushTextToHashMap(self, textArray: list):
        for text in textArray:
            if text not in self.globalHash:
                self.globalHash[text] = 1
            else:
                self.globalHash[text] = self.globalHash[text] + 1
    
    def returnAllResults(self):
            return sorted(self.globalHash.items(), key=lambda key: key[1])
                
    def runDescriptionProcessing(self, text):
        processedText:list = self.processSentence(text)
        self.pushTextToHashMap(processedText)
    
process1 = LinkedinProcessing()
with open('description.txt') as file:
    fileContents = file.read()
    process1.runDescriptionProcessing(fileContents)
    print(process1.returnAllResults())
        