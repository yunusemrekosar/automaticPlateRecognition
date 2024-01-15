import cv2

def RemoveNonAlnumsFromEdges(texts):
    newList = []
    for s in texts:
        while len(s) > 0 and not s[0].isdigit():
            s = s[1:]
        while len(s) > 0 and not s[-1].isdigit():
            s = s[:-1]
        newList.append(s)
    return newList

def ControlTheLicensePlate(texts , auth, img):
    cleanTexts = []
    
    if isinstance(texts, str) and len(texts) > 8 :
        lst = [texts]
        cleanTexts = RemoveNonAlnumsFromEdges(lst)
    elif isinstance(texts, list):   
        shortTexts = []
        longTexts  = []
        for text in texts:
            print(len(text))
            if len(text) <= 8:
                shortTexts.append(text)
            else:
                longTexts.append(text)
            cleanTexts = RemoveNonAlnumsFromEdges(longTexts)
            cleanTexts += shortTexts
            
    for text in cleanTexts:
        cleanLicensePlateText = text.replace("\n", "")  
        cleanLicensePlateText = ''.join(e for e in cleanLicensePlateText if (e.isalnum()))
        cleanLicensePlateText = cleanLicensePlateText.replace(" ", "")
        result = FormatLicensePlate(cleanLicensePlateText)
        imgName = result+'.jpg'

        if len(result) >= 7 and len(result) < 9:
           if result in [A[0] for A in auth]:
                log(result, True,cleanLicensePlateText)
                cv2.imwrite('./outputs/'+cleanLicensePlateText+'yetkili' + imgName, img)
                return result
           
        if len(result) >= 1:
            log(result, False,cleanLicensePlateText)
            cv2.imwrite('./outputs/'+cleanLicensePlateText+'yetkisiz' + imgName  , img)
    return None

def FormatLicensePlate(text : str):
    dictCharToInt = {'A': '4',
                     'B': '3',
                     'C': '0',
                     'D': '0',
                     'D': '0',
                     'O': '0',
                     'I': '1',
                     'J': '3',
                     'G': '6',
                     'S': '5',
                     'L': '4',
                     'Z': '2'}

    dictIntToChar = {'0': 'O',
                     '1': 'I',
                     '2': 'Z',
                     '3': 'B',
                     '4': 'A',
                     '5': 'S',
                     '6': 'G',
                     '7': 'I',
                     '8': 'B',
                     '9': 'P'}    
                        
    if len(text) > 6:
        indicesToReplace_f = [0, 1,(len(text)-1), (len(text)-2)]     
        text = replaceCharsAtIndices(text, dictCharToInt, indicesToReplace_f)
        indicesToReplace_l = [2]
        text = replaceCharsAtIndices(text, dictIntToChar, indicesToReplace_l)
   
    return text          

def replaceCharsAtIndices(inputStr, charDict, indices):
    result = list(inputStr)
    for index in indices:
        if 0 < index < len(charDict):
            char = inputStr[index]
            if char in charDict:
               result[index] = charDict[char]

    return "".join(result)

def log(plateText: str, isRecognized : bool , cleanText : str):
     with open('log.txt', 'a') as log:
        if (isRecognized):
            log.write(plateText + 'palakalı araç geçiş yaptı' +cleanText+'\n\n')
        else:
            log.write(plateText + 'palakalı araç yetkisiz' +cleanText+'\n\n')