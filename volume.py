import vtk
from vtk.util import numpy_support
import numpy as np
from dicom_reader import get_data

fileName = 'rbc_001.vtk'

ow = vtk.vtkOutputWindow()
ow.SendToStdErrOn()

#slices, rows, columns, volumePixelData = get_data()

#print(str(volumePixelData.shape))
# imageData = vtk.vtkImageData()
# imageData.SetDimensions(volumePixelData.shape)
# imageData.AllocateScalars(vtk.VTK_DOUBLE, 1)
# imageData.SetSpacing([1,1,1])
# imageData.SetOrigin([0,0,0])

# dataArray = numpy_support.numpy_to_vtk(volumePixelData.ravel(),deep=True,array_type=vtk.VTK_FLOAT)
# imageData.GetPointData().SetScalars(dataArray)

# dims = imageData.GetDimensions()

# for z in range(dims[2]):
#     for y in range(dims[1]):
#         for x in range(dims[0]):
#             imageData.SetScalarComponentFromDouble(x,y,z,0,150.0)

# Create the reader for the data.
reader = vtk.vtkUnstructuredGridReader()
reader.SetFileName(fileName)
reader.GetOutput().GetPointData().SetActiveScalars('smooth')
reader.Update()
#scalar_range = reader.GetOutput().GetScalarRange()

colors = vtk.vtkNamedColors()

# Create transfer mapping scalar value to opacity.
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(20, 0.0)
opacityTransferFunction.AddPoint(30, 0.1)
opacityTransferFunction.AddPoint(255, 0.9)

# Create transfer mapping scalar value to color.
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.2, 0.0)

# The property describes how the data will look.
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function knows how to render the data.
volumeMapper = vtk.vtkUnstructuredGridVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())
#volumeMapper.SetScalarRange(scalar_range)
#volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
#volumeMapper.SetInputData(imageData)

# The volume holds the mapper and the property and
# can be used to position/orient the volume.
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# Create the standard renderer, render window and interactor.
ren1 = vtk.vtkRenderer()

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren1.AddVolume(volume)
ren1.SetBackground(colors.GetColor3d("White"))
ren1.GetActiveCamera().Azimuth(45)
ren1.GetActiveCamera().Elevation(30)
ren1.ResetCameraClippingRange()
ren1.ResetCamera()

renWin.SetSize(600, 600)
renWin.Render()

iren.Start()

# # Create the mapper that creates graphics elements
# mapper = vtk.vtkDataSetMapper()
# mapper.SetInputData(imageData)

# # Create the Actor
# actor = vtk.vtkActor()
# actor.SetMapper(mapper)
# # show the edges of the image grid
# actor.GetProperty().SetRepresentationToWireframe()
# actor.GetProperty().SetColor(colors.GetColor3d("DarkSalmon"))

# # Create the Renderer
# renderer = vtk.vtkRenderer()
# renderer.AddActor(actor)
# renderer.ResetCamera()
# renderer.SetBackground(colors.GetColor3d("Silver"))

# # Create the RendererWindow
# renderer_window = vtk.vtkRenderWindow()
# renderer_window.AddRenderer(renderer)

# # Create the RendererWindowInteractor and display the vti file
# interactor = vtk.vtkRenderWindowInteractor()
# interactor.SetRenderWindow(renderer_window)
# interactor.Initialize()
# interactor.Start()

