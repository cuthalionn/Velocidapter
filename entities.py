import random
class DialogueTemplate:
    def __init__(self,turns,queries=None):
        self.turns =turns
        self.selectedCount = 1
        self.queryDict = queries
        self.probWeight = None

    def __eq__(self,dialogueTemplate):
        isEqual = True

        if self.queryDict != dialogueTemplate.queryDict:
            isEqual = False
        
        if len(self.turns) != len(dialogueTemplate.turns):
            isEqual = False
        else:
            for i in range(len(self.turns)):
                if self.turns[i] != dialogueTemplate.turns[i]:
                    isEqual = False
        return isEqual


class Dialogue():
    count = 1
    def __init__(self,turns=None,queryDict=None):
        if turns is None:
            turns = []
        if queryDict is None:
            queryDict = {}
        self.turns = turns
        self.queryDict = queryDict
        self.id = Dialogue.count
        Dialogue.count += 1
        
    def terminateDialogue(self):
        Dialogue.count -=1

    def add_turn(self,turn):
        self.turns.append(turn)

    def print(self):
        for turn in self.turns:
            print("+ ",turn)    
        print("Query Values:\n", self.queryDict)
    
    def addQueryItem(self,key,phrase,value):
        assert (key not in self.queryDict.keys())
        self.queryDict[key] = (phrase,value)

    def form(self,dialTemplate,valueDict):
        finalDict = {}
        for key in list(dialTemplate.queryDict.keys()):
            finalDict[key] = valueDict[dialTemplate.queryDict[key]]
        
        for turn in dialTemplate.turns:
            for slotTag in list(dialTemplate.queryDict.keys()):
                turn = turn.replace("["+slotTag+"]",finalDict[slotTag])
            self.add_turn(turn)
            
    def __eq__(self,dialogue):
        isEqual = True
        if self.queryDict != dialogue.queryDict:
            isEqual = False
        
        if len(self.turns) != len(dialogue.turns):
            isEqual = False
        else:
            for i in range(len(self.turns)):
                if self.turns[i] != dialogue.turns[i]:
                    isEqual = False
        return isEqual
    def __hash__(self):
        return hash((tuple(self.turns),tuple(self.queryDict)))
class DataPoint:
    def __init__(self,utterance,valueDict):
        self.utterance = utterance
        self.valueDict = valueDict

class Slot():

    def __init__(self,prefix,suffix,id=None,index=None):
        self.id = id
        self.prefix = prefix
        self.suffix = suffix
        self.index = index
    @classmethod
    def fromSlotString(cls,slotString):
        if ("." in slotString):
            prefix = slotString.split(".")[0].rstrip()
            suffix = slotString.split(".")[1].rstrip()
        else:
            prefix = ""
            suffix = slotString

        return cls(prefix,suffix)

    def __eq__(self,slot):
        if slot.prefix == self.prefix and slot.suffix == self.suffix and slot.id == slot.id:
            return True
        else:
            return False
    
    def __hash__(self):
        return hash((self.prefix,self.suffix))

class Questions:

    def __init__(self, slotPhraseList):
        self.slotPhraseList = slotPhraseList

    def returnRandomPhrase(self,slot):
        phrase = ''
        try:
            phrase = random.choice(self.slotPhraseList[slot])
        except:
            phrase = 'Phrase not found'

        return phrase

class TemplateTurn():

    def __init__(self,utts,slots):
        self.utts  = utts
        self.slots = slots
    