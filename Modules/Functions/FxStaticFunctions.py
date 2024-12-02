import os
import subprocess
import time
from functools import wraps


def FxRelativeExport(exportPath:str=None, dirName:str=None):
    if dirName is None:
        dirName = "PythonOutput"
    if exportPath is None:
        exportPath = self.currentDirPath + f"/{dirName}/"
    else:
        exportPath += f"/{dirName}/"
    if not os.path.exists(exportPath):
        os.mkdir(exportPath)

def FxTravisShellCmdBuilder(xyzFilePath: str, travisInstructions:str=None) -> str:
    executable= "travis"
    argumentFrameFile= f" -p {xyzFilePath}"
    argumentInstructionsFile = f" -i {travisInstructions}"
    travisBashCommand = executable + argumentFrameFile + argumentInstructionsFile
    return travisBashCommand

def FxAssignThreadsToTasks(numThreads:int=1, inputToMultithread:list=[]) -> dict:
    threadsTasksMap:        dict    = {}
    inputPerThread: int     = len(inputToMultithread) // numThreads
    remainingInputs:int     = len(inputToMultithread)
    i=0
    while remainingInputs>0:
        threadTasks:list    = inputToMultithread[:inputPerThread]
        threadsTasksMap[i] = threadTasks

        inputToMultithread = inputToMultithread[inputPerThread:]
        i += 1
        remainingInputs -= inputPerThread
        if remainingInputs<inputPerThread: inputPerThread=1
    return threadsTasksMap

    # def decorator(func):
    #     @wraps(func)
    #     def inner(*args, **kwargs):
    #         result = func(*args, **kwargs)
    #         return result
    #     return inner
    # return decorator

def makeDir(pathToWrite):
    if not os.path.exists(pathToWrite):
        os.mkdir(pathToWrite)

def FxProcessTime(func):
    @wraps(func)
    def inner(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        endTime = time.time()
        timeSpent = endTime-startTime
        if timeSpent<0.001:
            print(f"Function {func.__name__} executed in {int(timeSpent*1_000_000)} µs")
        elif timeSpent<5:
            print(f"Function {func.__name__} executed in {float(timeSpent*1_000):.2f} ms")
        else:
            h, m = divmod(timeSpent, 3_600)
            m, s = divmod(m, 60)
            print(f"Function {func.__name__} executed in {int(h)}:{int(m)}:{int(s)}")
        return result
    return inner

def MolecularAnalysis(frame, travisInstructions:str=None, workingDir:str=None, timeBeforeKill:float=0.2) -> None:
        # Checking presence of instructions file
        # if travisInstructions is None:
        #     travisInstructionDefaultPath = os.path.join(self.currentDirPath, "TravisInstruction.txt")
        #     if os.path.exists(travisInstructionDefaultPath):
        #         travisInstructions = travisInstructionDefaultPath
        #     else:
        #         print("Warning: No Travis instructions file specified, building default instructions")
        #         travisInstructions = self.BuildTravisInstructions()
        # # Checking presence of working directory                
        # workingDir = "C:/Users/JL252842/Documents/Thesis/Python/TestFiles/xyz/logs" if workingDir is None else workingDir
        # End of Checks

        travisBashCommand = FxTravisShellCmdBuilder(frame, travisInstructions)
        travisApp = subprocess.Popen(travisBashCommand, cwd=workingDir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(timeBeforeKill)
        travisApp.terminate()
        return

