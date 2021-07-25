# from keras.preprocessing.sequence import pad_sequences
import numpy as np
import re
import string
import random
from json import JSONEncoder
class MyEncoder(JSONEncoder):
    def default(self, b):# pylint: disable=E0202
        elementTree = b.getroot()
        # r = re.compile('\w+')
        count = 0
        jsonDialogues = []
        trueCount = 0 
        falseCount = 0
        wordCount = 0
        turnCount = 0
        for dialogues in elementTree:
            for dialogue in dialogues:
                qas = []
                dialogueText = ""
                turns = dialogue[0]
                for turn in turns:
                    turnCount +=1 

                    dialogueText += turn.text + " "
                splitDialogue = dialogueText.split(" ")
                dic = {}
                indexSoFar = 0
                for i in range(len(splitDialogue)):
                    dic[i] = (indexSoFar,splitDialogue[i])
                    indexSoFar += len(splitDialogue[i]) + 1


                wordCount += len(dic)
                queries = dialogue[1]

                for query in queries:
                    question = query[2].text.translate(str.maketrans('', '', string.punctuation))
                    startWordIndex = int(query[3].text)

                   
                    startIndex= dic[startWordIndex][0]
                    answerText = query[5].text
                    answers = []
                    answer = {"answer_start":startIndex, "text": answerText}

                    if(answerText != dialogueText[startIndex:startIndex+len(answerText)]):
                        falseCount += 1
                    else:
                        trueCount +=1
                    
                    answers.append(answer)
                    newQasEl = {"answers" :answers,"id":str(count), "is_impossible": False, "question": question}
                    count += 1
                    qas.append(newQasEl)
                newEl = {"context": dialogueText,"qas":qas}
                jsonDialogues.append(newEl)
            innerDictList = {"paragraphs": jsonDialogues, "title": "flightBooking"}
        print("Total word count: %s, Total turn count: %s, Average words per turn: %s "%(wordCount,turnCount,wordCount/turnCount))
        finalDict = {"data": [innerDictList]}
        return finalDict