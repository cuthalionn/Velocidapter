from dataModule import DataStorage,DataLoader
from entities import Dialogue
from templateConstructor import TemplateConstructor
import config as cfg
import random 
from math import gcd
import numpy as np
import copy
# random.seed(1250)
# np.random.seed(1250)

class DataGenerator():
    def __init__(self,args):
        self.args = args
        self.dataLoader = DataLoader(args)
        self.dataStorer = DataStorage(args)
        self.prepareData()
        

    def prepareData(self):

        self.templateList = self.dataLoader.loadTemplates()
        self.slotDict = self.dataLoader.loadSlotValues()
        self.questions =  self.dataLoader.loadQuestions()
    
    def generate(self):
        dialogues = {}

        fail = 0
        count = 0
        while fail< self.args["max_number_tries_dial"] and  count < self.args["max_dialogue_count"]:
            
            if(count%1000 ==0):
                print(count)
            dialogue = Dialogue()
            
            #Choose a template to fill and extract queries
            queryDict, template = self.chooseTemplate()
            
            #Assign values to the queries from the data
            self.fillQueryDict(queryDict, dialogue) 
            
            #Create dialogue from template and assigned values
            dialogue.form(template,queryDict)
            if dialogue not in dialogues:
                dialogues[dialogue] = 1
                count +=1
            else:
                fail =+1
                dialogue.terminateDialogue()
        for dialogue in list(dialogues.keys()):
            self.dataStorer.addToTree(dialogue) 

        self.dataStorer.store()
        return dialogues

    def fillQueryDict(self, queryDict, dialouge):
        #Pop values used so that they are used once in each dialogue.
        slotDict = copy.deepcopy(self.slotDict)
        for key in list(queryDict.keys()):
            phrase = self.questions.returnRandomPhrase(key)
            randomValue = random.choice(slotDict[key.suffix])
            slotDict[key.suffix].remove(randomValue)
            queryDict[key] = randomValue
            # Saved for later use, where we need to return a query dictionary with the dialogue
            dialouge.addQueryItem(key,phrase,randomValue) 

    def chooseTemplate(self):
        template = self.chooseFairly(self.templateList)
        template.selectedCount += 1
        tempLateQueries = template.queryDict
        queryDict = {}
        for value in list(tempLateQueries.values()):
            queryDict[value] = ""
        return queryDict, template
            
    def chooseFairly(self,templateList):
        choosenTemplate = None

        lcm = templateList[0].selectedCount
        for temp in templateList:
            lcm = lcm * temp.selectedCount // (gcd(lcm,temp.selectedCount))

        sumWeights = 0
        for temp in templateList:
            temp.probWeight =lcm / temp.selectedCount
            sumWeights += temp.probWeight

        for temp in templateList:
            temp.probWeight /= sumWeights

        rand_num = random.random()
        for temp in templateList:
            if rand_num < temp.probWeight:
                choosenTemplate = temp
                break
            rand_num = rand_num - temp.probWeight
        return choosenTemplate

def main():
    args = cfg.get_args()
    if args["new_templates"]:
        tc = TemplateConstructor(args)
        tc.initFill()
        tc.construct()
        tc.makeTree()
        tc.store()
    dg = DataGenerator(args)
    dg.generate()

if __name__ == "__main__":
    main()