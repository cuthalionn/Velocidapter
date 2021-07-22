import os 
from datetime import datetime
now = datetime.now()
todate = now.strftime("%d.%m.%Y.%H.%M.%S")
FiguresPath = os.path.join(os.path.expanduser('~'), 'Documents', 'MyProjects', 'dialoguecomprehensiondataset', 'Model', 'Figures')

templatesFilePath = "Data/templates.xml"
slotsFilePath = "Data/Multiwoz_restaurant_Slots.json"
questionsFilePath = "Data/taxi_questions.xml"
modularTemplatesFilePath = "Data/ModularTemplates/RestaurantBookingTemplates.xml"
greetingsFilePath = "Data/greeting.txt"
storageFilePath = "Results/MultiWOZ/restaurant/out" + todate
slotRulesFilePath = "Data/SlotRules_MultiWOZ_restaurant.json"
useSlotRules = True
