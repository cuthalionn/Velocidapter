import xml.etree.ElementTree as ET
from entities import DialogueTemplate,Slot,TemplateTurn
import random
import copy
import string
import os
import json

class TemplateConstructor():
    def __init__(self,args):
        self.args = args
        self.tree = ET.parse(os.path.join(args["input_folder"],"modularTemplates.xml"))
        self.outFile = os.path.join(args["input_folder"],"templates.xml")
        self.templateDict = {}
        self.greetingList = []
        self.templates = []
        self.dialogues = ET.Element("dialogues")


    def initFill(self):
        with open(self.args["greetings_file"]) as file:
            for line in file:
                self.greetingList.append(line)
        
        root = self.tree.getroot()
        for template in root:
            dictKey = template.get("type")
            turns = template[0]
            
            for turn in turns:
                tempUtts = []
                tempSlots = []
                utts = turn[0]
                slots = turn[1]
                dialogue = " ".join([i.text for i in utts])

                for utt in utts:
                    tempUtts.append(utt.text)
                for slot in slots:
                    #Find index automatically
                    if not slot[2]:
                        slot[2].text = dialogue.translate(str.maketrans('', '', string.punctuation)).split(" ").index(slot.get("id"))
                    tempSlot = Slot(slot[0].text,slot[1].text,slot.get("id"),int(slot[2].text))
                    tempSlots.append(tempSlot)

                self.templateDict.setdefault(dictKey,[]).append(TemplateTurn(tempUtts,tempSlots))
                    
    def construct(self):
        fail = 0
        count = 0
        while fail < self.args["max_number_tries_temp"] and count < self.args["max_template_count"]:
            count +=1
            lastIndex = 0
            utts = []
            queryDict = {}

            #Start with a greeting turn
            template = random.choice(self.templateDict["greeting"])
            utts.extend(template.utts)

            queryDict = {slot.id:copy.deepcopy(slot) for slot in template.slots}
            for utt in template.utts:
                lastIndex += len(utt.split(" "))

            done = False
            request_respondList = copy.deepcopy(self.templateDict["request_respond"]) 
            random.shuffle(request_respondList)
            
            while not done:
            #Choose a request respond turn
                while request_respondList:
                    stepPassed = True
                    template = request_respondList.pop()
                    rules = {}
                    if self.args["use_rules"]:
                        with open(os.path.join(self.args["input_folder"],"rules.json")) as ruleFile:
                            rules = json.load(ruleFile)
                    for slot in template.slots:
                        if self.args["use_rules"]:
                            if slot.id in list(rules.keys()):
                                for slotID in rules[slot.id]:
                                    if slotID in list(queryDict.keys()):
                                        stepPassed = False
                                        break

                        if(slot.id in list(queryDict.keys())):
                            stepPassed = False
                            break
                    if stepPassed:
                        newUtts = copy.deepcopy(template.utts)
                        newSlots = copy.deepcopy(template.slots)
                        #Add greeting if it's the first turn of the system
                        if len(utts) == 1: 
                            greeting = random.choice(self.greetingList).strip()
                            systemSignifier = template.utts[0].split(" ")[0]
                            secondWInd = template.utts[0].index(template.utts[0].split(" ")[1])
                            newUtt = "".join([systemSignifier," ", greeting ," ", template.utts[0][secondWInd:]])
                            newUtts[0] = newUtt

                            for i in range(len(template.slots)):
                                newSlots[i].index = template.slots[i].index + len(greeting.split(" "))
                            
                        utts.extend(newUtts)
                    
                        for slot in newSlots:
                            slot.index += lastIndex 
                            queryDict[slot.id] = slot

                        for utt in newUtts:
                            lastIndex += len(utt.split(" "))
                        break
                if not stepPassed or len(request_respondList) == 0:
                    done = True

            #Finish with an end turn
            template = random.choice(self.templateDict["end"])
            utts.extend(template.utts)


            newTemplate = DialogueTemplate(utts,queryDict)
            if newTemplate not in self.templates:
                self.check(newTemplate)
                self.templates.append(newTemplate)
            else:
                fail += 1
    def check(self,template):
        wholeText = ""

        for turn in template.turns:
            wholeText += turn + " "
        wholeText += "\b"

        for queryID in list(template.queryDict.keys()):
            slot = template.queryDict[queryID]
            assert (wholeText.translate(str.maketrans('', '', string.punctuation)).split(" ").index(queryID) == slot.index)


    def makeTree(self):
        for template in self.templates:
            templateEl = ET.SubElement(self.dialogues,"dialogue")
            turns = ET.SubElement(templateEl,"turns")
            index = 0 
            for turn in template.turns:
                turnEl = ET.SubElement(turns,"turn")
                turnEl.text = turn
                if index % 2 == 0:
                    turnEl.set("speaker","user")
                else:
                    turnEl.set("speaker","system")
                index += 1
             
            slots = ET.SubElement(templateEl,"slots")

            for queryKey in list(template.queryDict.keys()):
                slot = template.queryDict[queryKey]
                slotEl = ET.SubElement(slots,"slot")
                slotEl.set("id", slot.id)
                prefixEl = ET.SubElement(slotEl,"prefix")
                suffixEl = ET.SubElement(slotEl,"suffix")
                indexEl = ET.SubElement(slotEl,"index")
                prefixEl.text = slot.prefix
                suffixEl.text = slot.suffix
                indexEl.text = str(slot.index)

    def store(self):
        tree = ET.ElementTree(self.dialogues)
        tree.write(self.outFile)