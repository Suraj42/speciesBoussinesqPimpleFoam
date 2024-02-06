# Python code to read the evaporation simulation data

import csv
import numpy as np
import scipy.integrate as integrate
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def evaporationBox(drop_center,box_width,box_height,diffusion_flux_0_interpolator,diffusion_flux_1_interpolator, \
                        convective_flux_0_interpolator,convective_flux_1_interpolator):

        ## we define a box with width box_width and height box_height

        # integration along upper part of the box,
        # y=box_height, drop_center-box_width/2 < x < drop_center+box_width/2

        def upper_diffusion_flux(xx):
            if isinstance(xx, float):
                return diffusion_flux_1_interpolator(xx,box_height)
            else: # array is passed
                result = []
                for x in xx:
                    result.append(diffusion_flux_1_interpolator(x,box_height))
                return np.array(result)

        def upper_convective_flux(xx):

            if isinstance(xx, float):
                return convective_flux_1_interpolator(xx,box_height)
            else: ## array is passed
                result = []
                for x in xx:
                    result.append(convective_flux_1_interpolator(x,box_height))
                return np.array(result)

        def lateral_diffusion_flux(yy):

            if isinstance(yy, float):
                return diffusion_flux_0_interpolator(drop_center+box_width/2.0,yy) - \
                diffusion_flux_0_interpolator(drop_center-box_width/2.0,yy)

            else: ## array is passed
                result = []
                for y in yy:
                    result.append(diffusion_flux_0_interpolator(drop_center+box_width/2.0,y) - \
                    diffusion_flux_0_interpolator(drop_center-box_width/2.0,y))

                return np.array(result)

        def lateral_convective_flux(yy):
            result = []

            if isinstance(yy, float):
                return convective_flux_0_interpolator(drop_center+box_width/2.0,yy) - \
                convective_flux_0_interpolator(drop_center-box_width/2.0,yy)

            else: ## array is passed

                for y in yy:
                    result.append(convective_flux_0_interpolator(drop_center+box_width/2.0,y) - \
                    convective_flux_0_interpolator(drop_center-box_width/2.0,y))
            #print(result)       
            return np.array(result)

        # integration of fluxes over upper boundary
        total_upper_diffusion_flux = integrate.quad(upper_diffusion_flux ,\
                                        drop_center-box_width/2.0,drop_center+box_width/2.0)[0]

        total_upper_convective_flux = integrate.quad(upper_convective_flux,\
                                        drop_center-box_width/2.0,drop_center+box_width/2.0)[0]
        
        # plot fluxes
        # using start value of 1E-05 for eg., produces nan warnings, the total lat. conv. flux remains unchanged with nan warnings
        yy_space = np.linspace(5E-05,box_height,100) # for lateral diffusion  
        xx_space = np.linspace(drop_center-box_width/2.0,drop_center+box_width/2.0,200)

        # integration of lateral flux over the edges of the box
        # TODO currently not working because of masked elements
        total_lateral_diffusion_flux = integrate.quad(lateral_diffusion_flux,1E-04,box_height)[0]
        total_lateral_convective_flux = integrate.quad(lateral_convective_flux,1E-04,box_height)[0]

        total_box_flux = total_upper_diffusion_flux + total_upper_convective_flux + total_lateral_diffusion_flux + total_lateral_convective_flux
        
        # totalFlux = []
        # totalFlux.append(total_box_flux)
        # box_size = []
        # box_size.append(box_height)
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-3, -3))

        plt.figure()
        plt.plot(yy_space,lateral_diffusion_flux(yy_space),label="Diffusion ")
        plt.plot(yy_space,lateral_convective_flux(yy_space),label="Convection ")
        plt.plot(yy_space,lateral_diffusion_flux(yy_space)+lateral_convective_flux(yy_space),label="Sum")
        plt.xlabel("Y / (m)")
        plt.ylabel("Flux  / $\mathrm{(mol/m^2s)}$")
        plt.gca().xaxis.set_major_formatter(formatter)
        plt.gca().yaxis.set_major_formatter(formatter)
        #plt.title("Fluxes perpendicular to $\Sigma$")
        plt.legend()
        plt.savefig("fluxes_box_" + str(box_height) + "_lateral_boundary.pdf",bbox_inches='tight')

        plt.figure()
        plt.plot(xx_space,upper_diffusion_flux(xx_space),label="Diffusion")
        plt.plot(xx_space,upper_convective_flux(xx_space),label="Convection")
        plt.plot(xx_space,upper_diffusion_flux(xx_space)+upper_convective_flux(xx_space),label="Sum")
        plt.xlabel("X / (m)")
        plt.ylabel("Flux / $\mathrm{(mol/m^2s)}$")
        plt.gca().xaxis.set_major_formatter(formatter)
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.legend()
        plt.savefig("fluxes_box_" + str(box_height) + "_upper_boundary.pdf",bbox_inches='tight')

        #######
        print("Total upper diffusion flux for box "+ str(box_height) + ": " + str(total_upper_diffusion_flux))
        print("Total upper convectice flux for box "+ str(box_height) + ": " + str(total_upper_convective_flux))
        print("Total lateral diffusion flux for box "+ str(box_height) + ": " + str(total_lateral_diffusion_flux))
        print("Total lateral convective flux for box "+ str(box_height) + ": " + str(total_lateral_convective_flux))

        print("total_box_flux for box " + str(box_height) + ": " + str(total_box_flux))

        return total_box_flux

def readEvaportationSimData(dataFile,diffusion_coefficient):

        ### Read CSV File ###
        with open(dataFile, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            # Read header
            header = next(csv_reader)

            # Create dictionary for each column
            columns = {col: [] for col in header}

            # Read in data for each column
            for row in csv_reader:
                for col, data in zip(header, row):
                    columns[col].append(data)
        ###########

        ### Select specific column of interest ###
        print("Available fields [from csv header]:")
        print(header)
        # physical fields
        conc = columns['C'] # concentration field
        cellID = columns['Cell ID'] # id of the point
        cellType = columns['Cell Type'] # type of the cell
        #coordX = columns['coordX']
        #coordY = columns['coordY']
        coords_0 = columns['coords_0']
        coords_1 = columns['coords_1']
        U_0 = columns['U_0'] # x-component of velocity
        U_1 = columns['U_1'] # y-component of velocity
        Gradc_0 = columns['Gradc_0'] # x-component of grad conc
        Gradc_1 = columns['Gradc_1'] # y-component of grad conc
        p = columns['p']
        p_rgh = columns['p_rgh']
        # blocks
        BlockName = columns['Block Name']
        BlockNamesList = set(BlockName) # reduce to unique entries

        # dictionary for the different meshes
        meshes = {}

        for mesh in BlockNamesList:
            meshes[mesh] = {}
            meshes[mesh]["C"] = [] # empty list for conc
            meshes[mesh]["cellID"] = [] # empty list for cellID
            meshes[mesh]["cellType"] = [] # empty list for cellType
            #meshes[mesh]["coordX"] = [] # empty list for coordX
            #meshes[mesh]["coordY"] = [] # empty list for coordY
            meshes[mesh]["coords_0"] = [] # empty list for coords_0
            meshes[mesh]["coords_1"] = [] # empty list for coords_1
            meshes[mesh]["U_0"] = [] # empty list for U_0
            meshes[mesh]["U_1"] = [] # empty list for U_1
            meshes[mesh]["Gradc_0"] = [] # empty list for Gradc_0
            meshes[mesh]["Gradc_1"] = [] # empty list for Gradc_1
            meshes[mesh]["p"] = [] # empty list for p
            meshes[mesh]["p_rgh"] = [] # empty list for p_rgh

        ### Loop over all elements in original csv file to populate the mesh dictionaries
        for ii in range(0,len(cellID)):
            # Store elements, do proper type conversion
            #print(BlockName[ii])
            meshes[BlockName[ii]]["C"].append(float(conc[ii]))
            meshes[BlockName[ii]]["cellID"].append(int(cellID[ii]))
            meshes[BlockName[ii]]["cellType"].append(cellType[ii])
            #meshes[BlockName[ii]]["coordX"].append(float(coordX[ii]))
            #meshes[BlockName[ii]]["coordY"].append(float(coordY[ii]))
            meshes[BlockName[ii]]["coords_0"].append(float(coords_0[ii]))
            meshes[BlockName[ii]]["coords_1"].append(float(coords_1[ii]))
            meshes[BlockName[ii]]["U_0"].append(float(U_0[ii]))
            meshes[BlockName[ii]]["U_1"].append(float(U_1[ii]))
            meshes[BlockName[ii]]["Gradc_0"].append(float(Gradc_0[ii]))
            meshes[BlockName[ii]]["Gradc_1"].append(float(Gradc_1[ii]))
            meshes[BlockName[ii]]["p"].append(float(p[ii]))
            meshes[BlockName[ii]]["p_rgh"].append(float(p_rgh[ii]))

        ####### compute flux vector fields for "internal field" from data
        ## compute convective flux vector field
        meshes["internal"]["conv_flux_0"] = np.array(meshes["internal"]["U_0"])*np.array(meshes["internal"]["C"])
        meshes["internal"]["conv_flux_1"] = np.array(meshes["internal"]["U_1"])*np.array(meshes["internal"]["C"])
        ## compute diffusion flux vector field
        meshes["internal"]["diffusion_flux_0"] = -np.array(meshes["internal"]["Gradc_0"])*diffusion_coefficient
        meshes["internal"]["diffusion_flux_1"] = -np.array(meshes["internal"]["Gradc_1"])*diffusion_coefficient

        return [BlockNamesList,meshes]
