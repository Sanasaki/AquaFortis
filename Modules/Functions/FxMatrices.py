import numpy as np
from FxStaticFunctions import FxProcessTime


# @FxProcessTime
def periodicBoundaryConditions(
          distanceArray:    np.ndarray, 
          atomicSystemSize: float
          ) -> np.ndarray:
        
    distanceArray = np.where(distanceArray>(atomicSystemSize/2), atomicSystemSize-distanceArray, distanceArray)

    return distanceArray

    

