import xml.etree.ElementTree as ET
from entities import DialogueTemplate,Slot,Questions
from common import MyEncoder
from datetime import datetime
import numpy as np
import string
import os 
import re
import json
#Data related class and functionss
class DataStorage:
    def __init__(self,args):
        self.args = args
        self.filename = args["output_folder"]
        self.data = ET.Element("data")
        self.dialogues = ET.SubElement(self.data, "dialogues")
        
    def addToTree(self,dialogue):
        cumulativeErr = 0
        dialogueEl = ET.SubElement(self.dialogues,"dialogue")
        turns = ET.SubElement(dialogueEl,"turns")
        index = 0 
        dialogueText = ""
        for turn in dialogue.turns:
            dialogueText += turn + " "
            turnEl = ET.SubElement(turns,"turn")
            turnEl.text = turn
            if index % 2 == 0:
                turnEl.set("speaker","user")
            else:
                turnEl.set("speaker","system")
            index += 1
        
        queries = ET.SubElement(dialogueEl,"queries")

        for querySlot in list(dialogue.queryDict.keys()):
            if (querySlot.prefix == "arbitrary"):
                answerLength = len(dialogue.queryDict[querySlot][1].split(" "))
                cumulativeErr += answerLength - 1
                continue

            queryEl = ET.SubElement(queries,"query")
            prefixEl = ET.SubElement(queryEl,"prefix")
            suffixEl = ET.SubElement(queryEl,"suffix")
            qPhraseEl = ET.SubElement(queryEl,"phrase")
            startIndexEl = ET.SubElement(queryEl,"startIndex")
            endIndexEl = ET.SubElement(queryEl,"endIndex")
            valueEl = ET.SubElement(queryEl,"value")
            prefixEl.text = querySlot.prefix
            suffixEl.text = querySlot.suffix
            qPhraseEl.text =  dialogue.queryDict[querySlot][0]
            valueEl.text = dialogue.queryDict[querySlot][1]
            startIndexEl.text = str(querySlot.index + cumulativeErr)
            answerLength = len(dialogue.queryDict[querySlot][1].split(" "))
            endIndexEl.text = str(querySlot.index + answerLength + cumulativeErr)
            cumulativeErr += answerLength - 1

            assert (" ".join(dialogueText.split(" ")[int(startIndexEl.text):int(endIndexEl.text)]).replace(",","").replace(".","").replace("?","").replace("!","") == valueEl.text.replace(",","").replace(".","").replace("?","").replace("!",""))

        id = ET.SubElement(dialogueEl,"id")
        id.text = str(dialogue.id)

        timeStamp = ET.SubElement(dialogueEl,"timeStamp")
        timeStamp.text = str(datetime.now())
        


    def store(self):
        tree = ET.ElementTree(self.data)
        tree.write(self.filename + ".xml")
        trainVal = True
        if trainVal:
            trainTree, valTree = self.trainVal(tree, 1 - self.args["val_split"])
            with open(self.filename+"train.json", "w") as write_file:
                json.dump(trainTree,write_file,cls=MyEncoder)
            with open(self.filename+"val.json", "w") as write_file:
                json.dump(valTree,write_file,cls=MyEncoder)
        else:
            with open(self.filename+"train.json", "w") as write_file:
                json.dump(tree,write_file,cls=MyEncoder)
            
        

    def trainVal(self,tree,ratio):
        elementTree = tree.getroot()
        trainTree = ET.Element("data")
        testTree = ET.Element("data")

        trainDialogues = ET.SubElement(trainTree, "dialogues")
        testDialogues = ET.SubElement(testTree, "dialogues")

        dialogues =  elementTree[0]
        numDialogues = len(dialogues)
        numTrain = int(numDialogues*ratio)
        for dialogueIndex in range(numTrain):
            trainDialogues.append(dialogues[dialogueIndex])
        for dialogueIndex in range(numTrain,numDialogues):
            testDialogues.append(dialogues[dialogueIndex])
        return ET.ElementTree(trainTree),ET.ElementTree(testTree)


class DataLoader:
    def __init__(self,args):
        self.args = args
        self.templateTree = ET.parse(os.path.join(args["input_folder"],"templates.xml"))
        self.questionTree = ET.parse(os.path.join(args["input_folder"],"questions.xml"))
        self.slotsPath = os.path.join(args["input_folder"],"slots.json")


    def loadSlotValues(self):
        with open(self.slotsPath) as json_file:
            data = json.load(json_file)

        return data

    def loadQuestions(self):
        slotPhraseList = {}
        root = self.questionTree.getroot()

        for question in root:
            slot = question[0]
            qPhrases = question[1]

            phrases = []
            tempSlot = Slot(slot[0].text,slot[1].text)
            for qPhrase in qPhrases:
                phrases.append(qPhrase.text)
            slotPhraseList[tempSlot] = phrases
        
        return Questions(slotPhraseList)

    def loadTemplates(self):
        dialTemplates = []
        root = self.templateTree.getroot()

        for dialogue in root:
            turns = dialogue[0]
            slots = dialogue[1]
            dialTurns = []
            queries = {}
            for turn in turns:
                dialTurns.append(turn.text)
            for slot in slots:
                tempSlot = Slot(slot[0].text,slot[1].text,slot.get("id"),int(slot[2].text))
                queries[slot.get("id")] = tempSlot


            dialTemp = DialogueTemplate(dialTurns,queries)
            dialTemplates.append(dialTemp)
        
        return dialTemplates

    def extractSlotDict(self,DataPointlist):
        slotDict = {}

        for dataPoint in DataPointlist:
            for key,values in dataPoint.valueDict.items():
                key = key.suffix
                values = [' '.join(value.translate(str.maketrans('', '', string.punctuation)).split()) for value in values]
                values = list(filter(lambda a: (a != '' and self.special_match(a) == True), values)) # and self.special_match(a) == True
                if len(values) != 0:
                    if key in slotDict.keys():
                        for value in values:
                            if value not in slotDict[key]:
                                slotDict[key].append(value)
                    elif key not in slotDict.keys():
                        slotDict[key] = values
        return slotDict

    def special_match(self, strg, search=re.compile(r'[^a-z0-9. ]').search):
        return not bool(search(strg))


