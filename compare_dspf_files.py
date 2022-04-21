import json, os, argparse


class COMPARE_DSPF():

    def __init__(self, file_path_1, file_path_2, output_path):
        self.filePath1 = file_path_1
        self.filePath2 = file_path_2
        self.outputPath = output_path
        pass
        
        self.currentOperation = None

        self.openFiles()
        self.layerMapDict = self.createLayerMapDict(self.fileContentList1)

        jsonOb = json.dumps(self.layerMapDict, sort_keys=True)
        with open('json1.json', 'w') as wf:
            wf.writelines(jsonOb)
        # self.layerMapDict2, rcContents2 = self.createLayerMapDict(self.fileContentList2)

        
    
    def openFiles(self):
        with open(self.filePath1, 'r') as rf:
            self.fileContentList1 = rf.readlines()

        with open(self.filePath2, 'r') as rf:
            self.fileContentList2 = rf.readlines()


    def createLayerMapDict(self, fileContents = []):
        lineNumber = 1
        layerMapDict = {}
        rcContents = []
        for cont in fileContents:
            line = str(cont).strip()
            wordList = line.split() 
            wordLength = len(wordList)
            if wordLength > 0:

                if line.lower() == "* instance section":
                    self.currentOperation = None
                
                if self.currentOperation == 'net':
                    rcContents.append(line)

                if line.upper() == '*LAYER_MAP':
                    self.currentOperation = 'layer'
                    # print(lineNumber, "\t", self.currentOperation)

                elif wordList[0].upper() == '*|NET':
                    self.currentOperation = 'net'


                if self.currentOperation == 'layer' and wordLength > 2 and wordList[0].startswith('*'):
                    tempDict = {}               
                    tempDict['id'] = wordList[0].split('*')[-1]
                    tempDict['name'] =  wordList[1]
                    tempDict['itf'] =  wordList[2].split('=')[-1]
                    tempDict['type'] = {}
    
                    layerMapDict[tempDict['id']] = tempDict

                    

            lineNumber += 1
        
        # print(layerMapDict['632'])
        layerMapDict = self.createRCmapDict(fileContents=rcContents, layerMapDict=layerMapDict)
        
        return layerMapDict

    def createRCmapDict(self,  layerMapDict, fileContents = []):
        tempDict = {}
        # prevNetVal = 1
        # currentNetVal = 1 
        print("createRCmapDict\n\n")
        for cont in fileContents:
            line = str(cont).strip()
            wordList = line.split() 
            wordLength = len(wordList)

            if wordLength > 3:

                if wordList[0].upper().startswith('R'):
                    labelId = ''
                    rvalue = None
                    rName = wordList[0].split("_")[0]
                    for val in wordList:
                        if val.startswith('R=') or val.startswith('r') :
                            rvalue = val.split('=')[-1]
                    if rvalue == None:
                        rvalue = wordList[3]

                    if  wordList[-1].split("=")[0].__contains__('$lvl'):
                        # print(wordList[-1].split("=")[-1])
                        layer = wordList[-1].split("=")[-1] 
                        labelId += layer + "_"             
                    if  wordList[-2].split("=")[0].__contains__('$lvl'):
                        layer = wordList[-2].split("=")[-1] 
                        labelId +=   layer

                    if labelId not in layerMapDict.keys():
                        tempDict = {}               
                        tempDict['id'] = labelId
                        tempDict['name'] =  labelId
                        tempDict['itf'] =  ''
                        tempDict['type'] = {}
                        layerMapDict[tempDict['id']] = tempDict   
                    if rName in layerMapDict[labelId]['type'].keys():
                        layerMapDict[labelId]['type'][rName].append(rvalue)
                    else:
                        layerMapDict[labelId]['type'][rName] = []
                        layerMapDict[labelId]['type'][rName].append(rvalue)


                elif wordList[0].upper().startswith('C'):
                    cValue =  wordList[3]
                    cName = wordList[0].split("_")[0]
                    labelId = ''
                    if  wordList[-2].split("=")[0].__contains__('$lvl'):
                        layer = wordList[-2].split("=")[-1]
                        labelId += layer + "_"
                    if  wordList[-1].split("=")[0].__contains__('$lvl'):
                        layer = wordList[-1].split("=")[-1]
                        labelId +=  layer


                    if labelId not in layerMapDict.keys():
                        tempDict = {}               
                        tempDict['id'] = labelId
                        tempDict['name'] =  labelId
                        tempDict['itf'] =  ''
                        tempDict['type'] = {}
                        layerMapDict[tempDict['id']] = tempDict
                    if cName in layerMapDict[labelId]['type'].keys():
                        layerMapDict[labelId]['type'][cName].append(cValue)
                    else:
                        layerMapDict[labelId]['type'][cName] = []
                        layerMapDict[labelId]['type'][cName].append(cValue)


        return layerMapDict
                    

    def createLayerOutput():
        pass



def print_dict(tempDict):
    try:
        jsonObj = json.dumps(tempDict, indent=4)
        print(jsonObj)
    except:
        print(tempDict)


def compareDspf(file_path_1, file_path_2, output_path='.'):
    print("\n\n", file_path_1, file_path_2, output_path, "\n\n")

    compare_dspf_class = COMPARE_DSPF(file_path_1, file_path_2, output_path)


if __name__ == "__main__":
    
    curWorkingDir = str(os.getcwd()).replace("\\", "/")
    command_format = "python {script_Path} {path_of_dspf_file_1} {path_of_dspf_file_2} {output_file_directory}"
    parser = argparse.ArgumentParser(description=command_format)
    parser.add_argument('dspf_1', type=str)
    parser.add_argument('dspf_2', type=str)
    parser.add_argument('output', type=str, default=".")
    args = parser.parse_args()

    try:
        file_path_1 = args.dspf_1
        file_path_2 = args.dspf_2
        output_path = args.output
    except:
        print(f"\n\nGive Command As Follows : {command_format}")
    

    compareDspf(file_path_1, file_path_2, output_path)



# python -u "c:\Users\dtco-gf\Desktop\AUTOMATION_TEAM\DSPF\cboa_experiment\DSPF\22FDX\compare_dspf_files.py" "C:\Users\dtco-gf\Desktop\AUTOMATION_TEAM\DSPF\cboa_experiment\DSPF\22FDX\SC12T_INVX8_CSC20R_CBoA.nominal.dspf" "C:\Users\dtco-gf\Desktop\AUTOMATION_TEAM\DSPF\cboa_experiment\DSPF\22FDX\SC12T_INVX8_CSC20R.nominal.dspf" "."



