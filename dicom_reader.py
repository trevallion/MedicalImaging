import numpy as np
import pydicom
import os
from pydicom.data import get_testdata_files

def get_data(directory_name):
    
    filenames = os.listdir(directory_name) #get_testdata_files('CT_small.dcm')
    datasets = []

    for filename in filenames:
        dataset = pydicom.dcmread(os.path.join(directory_name,filename))
        datasets.append(dataset)
    
    # If there is only one slice, add extra copies of it.
    if(len(datasets) < 2):
        for i in range(0,10):
            datasets.append(dataset)
    
    datasets.sort(key=lambda d: d.SliceLocation)

    slices = len(datasets)
    rows = int(datasets[0].Rows)
    columns = int(datasets[0].Columns)
    pixelWidth = float(datasets[0].PixelSpacing[0])
    pixelHeight = float(datasets[0].PixelSpacing[1])
    sliceThickness = float(datasets[0].SliceThickness)
    highBit = int(datasets[0].HighBit)
    normalizingValue = pow(2,highBit - 1)
    rescaleSlope = float(datasets[0].RescaleSlope)
    rescaleIntercept = float(datasets[0].RescaleIntercept)
    windowCenter = (datasets[0].get('WindowCenter',normalizingValue / 2))[0]
    windowWidth = (datasets[0].get('WindowWidth',normalizingValue))[0]
    
    print(windowCenter)
    print(windowWidth)
    
    bottomOfWindow = windowCenter - windowWidth / 2
    topOfWindow = windowCenter + windowWidth / 2
    
    print("Rescale Slope: " + str(rescaleSlope))
    print("Rescale Intercept : " + str(rescaleIntercept))
    print("Pixel Height: " + str(pixelHeight))
    print("Pixel Width: " + str(pixelWidth))
    print("Slice Thickness: " + str(sliceThickness))
    print("Bottom of Window: " + str(bottomOfWindow))
    print("Top of Window: " + str(topOfWindow))
    print("Normalizing Value: " + str(normalizingValue))
    
    pixelData = np.zeros((slices, rows, columns),dtype=float)

    for index,dataset in enumerate(datasets):
        #pixelData[:,:,index] = (dataset.pixel_array[:,:] * rescaleSlope + rescaleIntercept) / normalizingValue
        #pixelData[:,:,index] = dataset.pixel_array[:,:] / normalizingValue
        pixelData[index,:,:] = rescaleAndWindowPixelValue(dataset.pixel_array[:,:], bottomOfWindow, windowWidth, rescaleSlope, rescaleIntercept, normalizingValue) / normalizingValue
        
    maxXExtent = pixelWidth * columns
    maxYExtent = pixelHeight * rows
    maxZExtent = sliceThickness * slices
    
    return maxXExtent, maxYExtent, maxZExtent, pixelData

def rescaleAndWindowPixelValue(pixelValue, bottomOfWindow, windowWidth, rescaleSlope, rescaleIntercept, normalizingValue):
    # apply rescale calculation
    rescaledPixelValue = pixelValue * rescaleSlope + rescaleIntercept
    
    # apply windowing calculation
    return rescaledPixelValue / normalizingValue * windowWidth + bottomOfWindow