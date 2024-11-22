import asyncio
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing.pool import ThreadPool

from FileTypes import AtomicCoordinatesXYZfile
from FxStaticFunctions import FxAssignThreadsToTasks, FxProcessTime

# def writeFrame(frame):
#     framePath = "C:/Users/JL252842/Documents/Thesis/Python/TestFiles/xyz/framesNMT/" + f"{self.name}-{frameID}.xyz"
#     with open(framePath, "w") as f:
#         f.write(f"{self.atomNumber}\n")
#     frame.to_csv(framePath, sep=" ", mode="w", lineterminator='\n', index=False)

@FxProcessTime
def main(**argv):
    systemSize: float = 18.1462749444
    xyzFile = AtomicCoordinatesXYZfile("C:/Users/JL252842/Documents/Thesis/Python/TestFiles/xyz/80HNO3-20H2O-1-pos-LIGHT.xyz", atomicSystemSize=systemSize)

    xyzFile.SplitTrajectory()
    xyzFile.buildFramesList()

    frames = xyzFile._frames
    speciations = []
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    # with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        for frame in frames:
            frameObject = AtomicCoordinatesXYZfile(frame)
            future = executor.submit(frameObject.getSpeciation)
            # results[frame] = future.result()
            resultFile = frameObject.currentDirPath + "Speciation.txt"
            # speciations.append(future.result())
            # print(speciations)
            with open(resultFile, newline='\n', mode='a') as f:
                print(f"{frameObject.name}: {future.result()}", file=f) 



    
    # print(xyzFile.getSpeciation())
    # print(12//7)
     
    # # tasks = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    # tasks = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

    # Threads = FxAssignThreadsToTasks(3, tasks)
    # print(Threads)
    
if __name__ == "__main__":
    main()