import numpy as np
import pydicom
from pydicom.data import get_testdata_files

def get_data():
    filenames = get_testdata_files('CT_small.dcm')
    datasets = []

    for filename in filenames:
        dataset = pydicom.dcmread(filename)
        datasets.append(dataset)

    datasets.sort(key=lambda d: d.SliceLocation)

    slices = len(datasets)
    rows = int(datasets[0].Rows)
    columns = int(datasets[0].Columns)
    pixelWidth = float(datasets[0].PixelSpacing[0])
    pixelHeight = float(datasets[0].PixelSpacing[1])
    sliceThickness = float(datasets[0].SliceThickness)
    highBit = int(datasets[0].HighBit)
    normalizingValue = pow(2,highBit)
    rescaleSlope = float(datasets[0].RescaleSlope)
    rescaleIntercept = float(datasets[0].RescaleIntercept)
    
    print("Rescale Slope: " + str(rescaleSlope))
    print("Rescale Intercept : " + str(rescaleIntercept))

    pixelData = np.zeros((slices, rows, columns),dtype=float)

    for index,dataset in enumerate(datasets):
        pixelData[index,:,:] = (dataset.pixel_array[:,:] * rescaleSlope + rescaleIntercept) / normalizingValue
        #pixelData[index,:,:] = dataset.pixel_array[:,:] / normalizingValue
        #pixelData[index,:,:] = 100
    
    xCoords,yCoords,zCoords = np.mgrid[0:(columns + 1)*pixelWidth:pixelWidth, 0:(rows + 1)*pixelHeight, 0:(slices + 1) * sliceThickness:sliceThickness]
    
    return xCoords, yCoords, zCoords, pixelData