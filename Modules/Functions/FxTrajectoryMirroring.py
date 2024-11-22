# #!/bin/bash
# if [ -z "$trajectoryFile" ]; then
#   echo "No trajecory .xyz file specified"
#   exit 1
# else
#   trajectoryDir=$(dirname "$trajectoryFile")
#   # cd "$trajectoryDir"
#   mkdir "$trajectoryFile-MDframes"
#   atomNumber=$(echo "$(head -n 1 "$trajectoryFile")" | awk '{print $1}')
#   split -l $(("$atomNumber"+2)) --numeric-suffixes=1 "$trajectoryFile" "$trajectoryFile-MDframes/${1%.xyz}"-f
#   for frame in "$trajectoryFile-MDframes/${1%.xyz}"-f*; do
#     mv "$frame" "$frame.xyz"
#   done
# fi

import sys
from MolecularDynamicsTrajectory import MolecularDynamicsTrajectory

# testPath = "C:/Users/JL252842/Documents/Thesis/Python/TestFiles/xyz/frames/80HNO3-20H2O-1-pos-1-f1.xyz"
# xyzTestFile.SplitTrajectory()
# xyzTestFile.MultiThreadedTravisFrames(threadNumber=12)

testPath = "C:/Users/JL252842/Documents/Thesis/Python/TestFiles/xyz/80HNO3-20H2O-1-pos-1.xyz"
xyzTestFile = MolecularDynamicsTrajectory(testPath)
testPandas = xyzTestFile._ChunkBuildFrom()
# testChildren = xyzTestFile.BuildChildren()
# size = sys.getsizeof(testPandas)
# sizeKo = size // 1024
# sizeMo = sizeKo // 1024
# print(size, "o")
# print(sizeKo, "Ko")
# print(sizeMo, "Mo")
# testPathTwo = "C:/Users/JL252842/Documents/Thesis/Python/TestFiles/xyz/aWholeNewOne.xyz"
# for child in xyzTestFile._children:
    # child.Write(testPathTwo)





