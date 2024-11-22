import concurrent.futures
from tkinter import filedialog as fd

from FileTypes import AtomicCoordinatesXYZfile


def splittingFile(path):
    systemSize: float = 18.1462749444
    xyzFile = AtomicCoordinatesXYZfile(path, atomicSystemSize=systemSize)

    xyzFile.SplitTrajectory()
    xyzFile.buildFramesList()

    frames = xyzFile._frames
    return frames

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


if __name__ == "__main__":
    main()