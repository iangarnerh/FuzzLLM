import re
import sys

# tokDict = {"{m1}":["Ian", "Jennifer"], "{m2}": ["Harris", "Lawson"]}

# tokFileDict = {"{question}": "questions.txt", "{output_constraint}": "output_constraints.txt", "{characteristic_constraint}": "characteristic_constraints.txt", "{PE_constraint}": "pe_constraints.txt"}

#tokFileDict = {"{m1}": "m1.txt", "{m2}": "m2.txt"}
tokDict = {}

#def GetSlotList(mystr):
#    slList = []
#    for match in re.finditer("{[^}]*}", mystr):
#        slList.append((match.start(), match.end()))
#    return(slList)

# A Template is a string and a list of slots.
#class Template:
#    def __init__(self, tokStr):
#        self.tempStr = tokStr
#        self.sList = GetSlotList(tokStr)

def GetFirstSlot(mystr):
    match = re.search("{[^}]*}", mystr)
    if match:
        return(match.start(), match.end())
    else:
        return(match)


def ReplaceSlot(mystr, slot, tok):
    if slot[1] >= len(mystr):
        return(mystr[:slot[0]]+tok)
    else:
        return(mystr[:slot[0]]+tok+mystr[slot[1]:])

def ReadTokFiles():
    global tokDict
    tokFileDict = {}
    with open("slotMap.txt", "r") as sm:
        for line in sm:
            ltoks = line.split()
            tokFileDict[ltoks[0].strip()] = ltoks[1].strip()
    
    for tok, tfname in tokFileDict.items():
        tokDict[tok] = []
        
        with open(tfname, "r") as tFile:
            for line in tFile:
                if len(line.strip()) != 0:
                    if line.strip()[0] != '#':
                        tokDict[tok].append(line.strip())

def FillTString(mystr, outFile):
    global tokDict
    ReadTokFiles()
    cSlot = GetFirstSlot(mystr)
    if not(cSlot):
        outFile.write(mystr + '\n')
    else:
        tag = mystr[cSlot[0]:cSlot[1]]
        for tok in tokDict[tag]:
            FillTString(ReplaceSlot(mystr, cSlot, tok), outFile)

# s1 = "Answer the question and *strictly* follow the following constraint. Question: {question} Constraint: {output_constraint}"


def FillTemplates(tempFile, outFile):
    with open(tempFile, "r") as tf:
        with open(outFile, "w") as outFile:
            for line in tf:
                if len(line.strip()) != 0:
                    if line.strip()[0] != '#':
                        FillTString(line, outFile)
                        
# First arg is the template file name
# Second arg is the output file name

if __name__ == '__main__':
    FillTemplates(sys.argv[1], sys.argv[2])
