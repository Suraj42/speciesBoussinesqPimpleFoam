# speciesBoussinesqPimpleFoam
This repository contains the OpenFOAM solver used in the study "Imaging and simulation-based analysis of
evaporation flows over wetting edges". The vapor atmosphere above evaporating thin films is simulated. 
The thin films are printed through an ink-jet printing process and experimental measurements of 
the vapor field are obtained. The simulations provide additional information to understand the evaopration process
and mass transfer through the printed liquid film. 

The publication titled "Imaging and simulation-based analysis of evaporation flows over wetting edges" can be found
online for download [here](https://www.sciencedirect.com/science/article/pii/S0017931024005623). The experimental "data"
directory needed for post-processing and comaprison with simulations along with this repository is archived and found
[here](https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/4122.2). 

NOTE: For post-processing and reproduce Figure 13 in the publication it is essential to get the "data" folder from the archived
repository mentioned above. 

The pre-existing solver buoyantBoussinesqPimpleFoam within the OpenFOAM library is modified by us. 
The liquid interface acts as a part of the boundary of the domain and the mass transfer 
from this interface into the atmosphere is modeled and implemented through a Function object modifying 
the boundary condition. Functions Objects are provided (in folder src/functionObjects) to calculate the concentration 
at the interface  in time and subsequent evaluation of mass flux. The function objects have the value of the Henry coeffcient
in the suffix of their names. Post processing  is done with help of Jupyter notebooks 
and python scripts that use [Paraview](https://www.paraview.org/download/).  

## Description
The convergence study, cases with varying initial concentration on the liquid interface and case used for 
comparing the contour plots are in the folder "cases". The notebooks for evaluation and post processing are
in the folder "cases/notebooks" and figures are saved in "cases/figures". The python files for plots in the 
discussion section (quantification of diffusion and convection in the domain) of the article are in the folder 
"cases/discussion_section". 
The experimental data consists of the evaluated concentration matrix at different time intervals available in
the data folder. PNG files of the same are also provided for illustartion purposes. 
The solver is contained in the folder "solvers". There are two solvers namely, speciesBoussinesqPimpleFoam and 
speciesLaplacianFoam. The latter is modified from laplacianFoam by us and used for pure diffusion cases.

## OpenFOAM 

The openfoam version used is identified with git tag [v2206](https://develop.openfoam.com/Development/openfoam/-/tree/OpenFOAM-v2206?ref_type=tags).
The installation instructions are available in the same link. The solvers and function objects can be compiled after the
OpenFOAM installation/compilation by running ./Allwmake in the repository. The cases are run as ./Allrun with the Allrun script 
available within the cases. 

## Post-processing

There are python scripts inside each of the case folders that when run produce the desired data files for post-processing
with notebooks. In each case folder, after the case is run, the file "getVTK.sh" is run which produces the VTK files
needed by paraview to extract field data from the simulation. Then open paraview and select view->python shell. Within the
python shell open and run the file "getCSVFieldData.py" which extracts all the field data of the variables into a csv file. This file
is read by the jupyter notebooks for different times and as required. 






























