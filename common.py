# from keras.preprocessing.sequence import pad_sequences
import numpy as np
import re
import string
import random
from json import JSONEncoder
import configuration as cfg
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

                    # dialogueText += turn.text.translate(str.maketrans('', '', string.punctuation)) + " "
                    dialogueText += turn.text + " "
                splitDialogue = dialogueText.split(" ")
                dic = {}
                indexSoFar = 0
                for i in range(len(splitDialogue)):
                    dic[i] = (indexSoFar,splitDialogue[i])
                    indexSoFar += len(splitDialogue[i]) + 1


                # dic = { i :(m.start(0), m.group(0)) for i, m in enumerate(r.finditer(dialogueText))}
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
                        print("false")
                        print("dialogtext****************")
                        print(dialogueText)
                        print("dialogtext**********************************")
                        print(dic)
                        print("dic******************************************")
                        print(str(startWordIndex), " ", str(startIndex)," ", str(len(answerText)))
                        print("*******************************")
                        print(dialogueText[startIndex:startIndex+len(answerText)])
                        print("********************************")
                        print(answerText)
                        print("**********************************")
                    else:
                        # print("true")
                        trueCount +=1
                    
                    answers.append(answer)
                    newQasEl = {"answers" :answers,"id":str(count), "is_impossible": False, "question": question}
                    count += 1
                    qas.append(newQasEl)
                newEl = {"context": dialogueText,"qas":qas}
                jsonDialogues.append(newEl)
            innerDictList = {"paragraphs": jsonDialogues, "title": "flightBooking"}
        print("True: ", trueCount)
        print("False: ",falseCount)
        print("Total word count: %s, Total turn count: %s, Average words per turn: %s "%(wordCount,turnCount,wordCount/turnCount))
        finalDict = {"data": [innerDictList]}
        return finalDict

# def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
#     """

#     Call in a loop to create terminal progress ba   r
#     @params:
#         iteration   - Required  : current iteration (Int)
#         total       - Required  : total iterations (Int)
#         prefix      - Optional  : prefix string (Str)
#         suffix      - Optional  : suffix string (Str)
#         decimals    - Optional  : positive number of decimals in percent complete (Int)
#         length      - Optional  : character length of bar (Int)
#         fill        - Optional  : bar fill character (Str)
#         printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
#     """
#     percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
#     filledLength = int(length * iteration // total)
#     bar = fill * filledLength + '-' * (length - filledLength)
#     print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
#     # Print New Line on Complete
#     if iteration == total: 
#         print()

# def mixedPadding(data,startLabels,endLabels, max_length):
#     newdata = np.zeros((len(data),max_length))
#     newStartLabels = np.zeros((len(data),max_length))
#     newEndLabels = np.zeros((len(data),max_length))
#     prevData= None
#     preLength = 0
#     printProgressBar(0, len(data), prefix = 'Progress:', suffix = 'Complete', length = 50)
#     for j in range(len(data)):
#         maxLength = len(data[j])
#         prevData = data[j]
#         if (np.array_equal(prevData,data[j])):
#             NotImplemented
#         else:
#             preLength = random.randint(0, max_length- maxLength)

#         data[j] = pad_sequences(data[j:j+1], maxlen=preLength+maxLength, padding='pre')[0]
#         newdata[j] = pad_sequences(data[j:j+1], maxlen=max_length, padding='post')[0]

#         startLabels[j] = pad_sequences(startLabels[j:j+1], maxlen=preLength+maxLength, padding='pre')[0]
#         newStartLabels[j] = pad_sequences(startLabels[j:j+1], maxlen=max_length, padding='post')[0]

#         endLabels[j] = pad_sequences(endLabels[j:j+1], maxlen=preLength+maxLength, padding='pre')[0]
#         newEndLabels[j] = pad_sequences(endLabels[j:j+1], maxlen=max_length, padding='post')[0]

#         # time.sleep(0.1)
#         # Update Progress Bar
#         printProgressBar(j + 1, len(data), prefix = 'Progress:', suffix = 'Complete', length = 50)
#     return newdata,newStartLabels,newEndLabels