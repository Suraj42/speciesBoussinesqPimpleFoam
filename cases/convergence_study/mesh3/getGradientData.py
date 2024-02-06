# trace generated using paraview version 5.11.0
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XML MultiBlock Data Reader'
mesh3_14000vtm = XMLMultiBlockDataReader(registrationName='mesh3_14000.vtm', FileName=['/media/ssd-daten/speciesBoussinesqPimpleFoam/cases/convergence_study/mesh3/VTK/mesh3_14000.vtm'])
mesh3_14000vtm.CellArrayStatus = ['C', 'p', 'p_rgh', 'rhok', 'U']
mesh3_14000vtm.PointArrayStatus = ['C', 'p', 'p_rgh', 'rhok', 'U']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# get the material library
materialLibrary1 = GetMaterialLibrary()

# get display properties
mesh3_14000vtmDisplay = GetDisplayProperties(mesh3_14000vtm, view=renderView1)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# get opacity transfer function/opacity map for 'vtkBlockColors'
vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')

# get 2D transfer function for 'vtkBlockColors'
vtkBlockColorsTF2D = GetTransferFunction2D('vtkBlockColors')

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

#change interaction mode for render view
renderView1.InteractionMode = '2D'

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=mesh3_14000vtm)
calculator1.Function = ''

# Properties modified on calculator1
calculator1.Function = ''

# show data in view
calculator1Display = Show(calculator1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'
calculator1Display.ColorArrayName = [None, '']
calculator1Display.SelectTCoordArray = 'None'
calculator1Display.SelectNormalArray = 'None'
calculator1Display.SelectTangentArray = 'None'
calculator1Display.OSPRayScaleArray = 'C'
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.SelectOrientationVectors = 'None'
calculator1Display.ScaleFactor = 0.020299999415874483
calculator1Display.SelectScaleArray = 'C'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.GlyphTableIndexArray = 'C'
calculator1Display.GaussianRadius = 0.001014999970793724
calculator1Display.SetScaleArray = ['POINTS', 'C']
calculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator1Display.OpacityArray = ['POINTS', 'C']
calculator1Display.OpacityTransferFunction = 'PiecewiseFunction'
calculator1Display.DataAxesGrid = 'GridAxesRepresentation'
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.SelectInputVectors = ['POINTS', 'U']
calculator1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
calculator1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.8016524314880371, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
calculator1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.8016524314880371, 1.0, 0.5, 0.0]

# hide data in view
Hide(mesh3_14000vtm, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(calculator1Display, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# Properties modified on calculator1
calculator1.ResultArrayName = 'coords'

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on calculator1
calculator1.Function = 'coords'

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Point Data to Cell Data'
pointDatatoCellData1 = PointDatatoCellData(registrationName='PointDatatoCellData1', Input=calculator1)
pointDatatoCellData1.PointDataArraytoprocess = ['C', 'U', 'coords', 'p', 'p_rgh', 'rhok']

# show data in view
pointDatatoCellData1Display = Show(pointDatatoCellData1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
pointDatatoCellData1Display.Representation = 'Surface'
pointDatatoCellData1Display.ColorArrayName = [None, '']
pointDatatoCellData1Display.SelectTCoordArray = 'None'
pointDatatoCellData1Display.SelectNormalArray = 'None'
pointDatatoCellData1Display.SelectTangentArray = 'None'
pointDatatoCellData1Display.OSPRayScaleFunction = 'PiecewiseFunction'
pointDatatoCellData1Display.SelectOrientationVectors = 'coords'
pointDatatoCellData1Display.ScaleFactor = 0.020299999415874483
pointDatatoCellData1Display.SelectScaleArray = 'None'
pointDatatoCellData1Display.GlyphType = 'Arrow'
pointDatatoCellData1Display.GlyphTableIndexArray = 'None'
pointDatatoCellData1Display.GaussianRadius = 0.001014999970793724
pointDatatoCellData1Display.SetScaleArray = [None, '']
pointDatatoCellData1Display.ScaleTransferFunction = 'PiecewiseFunction'
pointDatatoCellData1Display.OpacityArray = [None, '']
pointDatatoCellData1Display.OpacityTransferFunction = 'PiecewiseFunction'
pointDatatoCellData1Display.DataAxesGrid = 'GridAxesRepresentation'
pointDatatoCellData1Display.PolarAxes = 'PolarAxesRepresentation'
pointDatatoCellData1Display.SelectInputVectors = [None, '']
pointDatatoCellData1Display.WriteLog = ''

# hide data in view
Hide(calculator1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(pointDatatoCellData1Display, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
pointDatatoCellData1Display.SetScalarBarVisibility(renderView1, True)

# Properties modified on pointDatatoCellData1
pointDatatoCellData1.PassPointData = 1

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Python Calculator'
pythonCalculator1 = PythonCalculator(registrationName='PythonCalculator1', Input=pointDatatoCellData1)
pythonCalculator1.Expression = ''

# Properties modified on pythonCalculator1
pythonCalculator1.Expression = ''

# show data in view
pythonCalculator1Display = Show(pythonCalculator1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
pythonCalculator1Display.Representation = 'Surface'
pythonCalculator1Display.ColorArrayName = [None, '']
pythonCalculator1Display.SelectTCoordArray = 'None'
pythonCalculator1Display.SelectNormalArray = 'None'
pythonCalculator1Display.SelectTangentArray = 'None'
pythonCalculator1Display.OSPRayScaleArray = 'C'
pythonCalculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
pythonCalculator1Display.SelectOrientationVectors = 'coords'
pythonCalculator1Display.ScaleFactor = 0.020299999415874483
pythonCalculator1Display.SelectScaleArray = 'C'
pythonCalculator1Display.GlyphType = 'Arrow'
pythonCalculator1Display.GlyphTableIndexArray = 'C'
pythonCalculator1Display.GaussianRadius = 0.001014999970793724
pythonCalculator1Display.SetScaleArray = ['POINTS', 'C']
pythonCalculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
pythonCalculator1Display.OpacityArray = ['POINTS', 'C']
pythonCalculator1Display.OpacityTransferFunction = 'PiecewiseFunction'
pythonCalculator1Display.DataAxesGrid = 'GridAxesRepresentation'
pythonCalculator1Display.PolarAxes = 'PolarAxesRepresentation'
pythonCalculator1Display.SelectInputVectors = ['POINTS', 'coords']
pythonCalculator1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
pythonCalculator1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.8016524314880371, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
pythonCalculator1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.8016524314880371, 1.0, 0.5, 0.0]

# hide data in view
Hide(pointDatatoCellData1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(pythonCalculator1Display, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
pythonCalculator1Display.SetScalarBarVisibility(renderView1, True)

# Properties modified on pythonCalculator1
pythonCalculator1.ArrayAssociation = 'Cell Data'

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on pythonCalculator1
pythonCalculator1.ArrayName = 'Gradc'

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on pythonCalculator1
pythonCalculator1.Expression = 'gradient(C)'

# update the view to ensure updated data information
renderView1.Update()

# get layout
layout1 = GetLayout()

# split cell
layout1.SplitHorizontal(0, 0.5)

# set active view
SetActiveView(None)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

# show data in view
pythonCalculator1Display_1 = Show(pythonCalculator1, spreadSheetView1, 'SpreadSheetRepresentation')

# assign view to a particular cell in the layout
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=2)

# Properties modified on spreadSheetView1
spreadSheetView1.FieldAssociation = 'Cell Data'

# export view
ExportView('/media/ssd-daten/speciesBoussinesqPimpleFoam/cases/convergence_study/mesh3/gradientData_14s.csv', view=spreadSheetView1, RealNumberNotation='Scientific',
    RealNumberPrecision=16)

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1166, 816)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [0.1014999970793724, 0.05000000074505806, 0.4372416341803258]
renderView1.CameraFocalPoint = [0.1014999970793724, 0.05000000074505806, 7.500000356230885e-05]
renderView1.CameraParallelScale = 0.11314705080831293

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).