import asyncio
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
from tkinter import filedialog as fd

from FileTypes import AtomicCoordinatesXYZfile
from FxStaticFunctions import FxAssignThreadsToTasks, FxProcessTime


@FxProcessTime
def splittingFile(path):
    systemSize: float = 18.1462749444
    xyzFile = AtomicCoordinatesXYZfile(path, atomicSystemSize=systemSize)

    xyzFile.SplitTrajectory()
    xyzFile.buildFramesList()

    frames = xyzFile._frames
    return frames

@FxProcessTime
def applyingSpeciation(frames):
    speciations = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    # with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        for frame in frames:
            frameObject = AtomicCoordinatesXYZfile(frame, toInitialize=True)
            frameName = frameObject.name.split("f")[-1]
            future = executor.submit(frameObject.getSpeciation)
            # results[frame] = future.result()
            # resultFile = frameObject.currentDirPath + "Speciation.txt"
            speciations[frameName]= future.result()
            # print(speciations)
            # with open(resultFile, newline='\n', mode='a') as f:
                # print(f"{frameObject.name}: {future.result()}", file=f) 
    return speciations

@FxProcessTime
def writingFile(speciations, name):
    # print(speciations)
    path = rf'C:\Users\JL252842\Documents\Thesis\Python\TestFiles\xyz\{name}-speciation.txt'
    with open(path, 'w')as outfile:
        for key, item in speciations.items():
            outfile.write(f"{key} {item}\n")

def main(**argv):
    path: str = fd.askopenfilename(title='Select a file',
                                   initialdir=r'C:\Users\JL252842\Documents\Thesis\Python\TestFiles/')

    xyzFile = AtomicCoordinatesXYZfile(path, 18.1462749444, toInitialize=True)
    # speciation = xyzFile.getSpeciation()
    # print(speciation)
    frames = splittingFile(path)
    speciations = applyingSpeciation(frames)
    writingFile(speciations, xyzFile.name)



    
    # print(xyzFile.getSpeciation())
    # print(12//7)
     
    # # tasks = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    # tasks = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

    # Threads = FxAssignThreadsToTasks(3, tasks)
    # print(Threads)
    
if __name__ == "__main__":
    main()