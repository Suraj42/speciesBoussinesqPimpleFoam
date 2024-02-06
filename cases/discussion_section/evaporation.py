import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from evaporationLib import *
from matplotlib.ticker import ScalarFormatter
####

dataFile = '../convergence_study/mesh3/gradientData_14s.csv' # full data

## Some important parameters for the siumulation case
diffusion_coefficient = 1.32E-05 # in SI units m^2/s
left_cl_postion = 0.1 # x-coordinate in m
right_cl_position = 0.103 # x-coordinate in m
drop_center = 0.1015
plot_height = 0.0105765

interpolationMethod = 'cubic' # use linear to safe some time if needed

## read in data
[BlockList, meshes] = readEvaportationSimData(dataFile,diffusion_coefficient)
print("Meshes found [Based on 'Block Name']:")
print(BlockList)

# compute the maximum concentration for "internal" mesh
max_conc = max(meshes["internal"]["C"])
print("Maximum concentration is: "+str(max_conc)+" mol/m^3")
######

########## Create triangulation and interpolation ############

# create a triangulation of the (coords_0, coords_1) points
triang = mtri.Triangulation(meshes["internal"]["coords_0"], meshes["internal"]["coords_1"])

# Create a grid for the interpolation.
xi = np.linspace(0.0955, 0.1065, 500)
mesh_dx = xi[1]-xi[0] # linspace is equidistant
yi = np.linspace(0.0, 0.0105765, 500)
mesh_dy = yi[1]-yi[0] # linspace is equidistant
Xi, Yi = np.meshgrid(xi, yi)

# Linearly interpolate the data (x, y) on a grid defined by (xi, yi).
if(interpolationMethod=='cubic'):
    conc_interpolator = mtri.CubicTriInterpolator(triang, meshes["internal"]["C"], kind='geom')
else:
    conc_interpolator = mtri.LinearTriInterpolator(triang, meshes["internal"]["C"])

conc_interpolation = conc_interpolator(Xi, Yi)
conc_grad_interpolation = conc_interpolator.gradient(Xi, Yi) # compute values for the gradient
def diffusion_flux_0_interpolator(xx,yy):
    return -diffusion_coefficient*conc_interpolator.gradient(xx, yy)[0]
def diffusion_flux_1_interpolator(xx,yy):
    return -diffusion_coefficient*conc_interpolator.gradient(xx, yy)[1]

if(interpolationMethod=='cubic'):
    U_0_interpolator = mtri.CubicTriInterpolator(triang, meshes["internal"]["U_0"], kind='geom')
    U_1_interpolator = mtri.CubicTriInterpolator(triang, meshes["internal"]["U_1"], kind='geom')
else:
    U_0_interpolator = mtri.LinearTriInterpolator(triang, meshes["internal"]["U_0"])
    U_1_interpolator = mtri.LinearTriInterpolator(triang, meshes["internal"]["U_1"])

U_0_interpolation = U_0_interpolator(Xi,Yi)
U_1_interpolation = U_1_interpolator(Xi,Yi)
def convective_flux_0_interpolator(xx,yy):
    return(U_0_interpolator(xx,yy)*conc_interpolator(xx, yy))
def convective_flux_1_interpolator(xx,yy):
    return(U_1_interpolator(xx,yy)*conc_interpolator(xx, yy))

###################################################

## Compute interpolation of the fluxes
# convective flux
convective_flux_0_interpolation = U_0_interpolation*conc_interpolation
convective_flux_1_interpolation = U_1_interpolation*conc_interpolation
# diffusion flux
diffusion_flux_0_interpolation = - diffusion_coefficient*conc_grad_interpolation[0]
diffusion_flux_1_interpolation = - diffusion_coefficient*conc_grad_interpolation[1]

# Compute divergence of velocity field
U_divergence = np.gradient(U_0_interpolation,mesh_dx,mesh_dy)[0] + np.gradient(U_1_interpolation,mesh_dx,mesh_dy)[1]

# Compute Divergence of the fluxes
convective_flux_divergence = \
np.gradient(convective_flux_0_interpolation,mesh_dx,mesh_dy)[0] + np.gradient(convective_flux_1_interpolation,mesh_dx,mesh_dy)[1]
diffusion_flux_divergence = \
np.gradient(diffusion_flux_0_interpolation,mesh_dx,mesh_dy)[0]+np.gradient(diffusion_flux_1_interpolation,mesh_dx,mesh_dy)[1]
total_flux_divergence = convective_flux_divergence + diffusion_flux_divergence

################################################################
## Compute flux over a box and plot 
box_height=[0.0005, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0035, 0.004]
box_width=[0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.010, 0.011]
total_Flux = []

for i in range(len(box_height)):
    print("Run 'evaporationBox': " + str(box_height[i]))
    totalFlux = evaporationBox(drop_center,box_width[i],box_height[i],diffusion_flux_0_interpolator,diffusion_flux_1_interpolator, \
                convective_flux_0_interpolator,convective_flux_1_interpolator)
    total_Flux.append(totalFlux)
print("totalFlux = " + str(totalFlux))

plt.figure()
for k in range(len(box_height)):
    plt.plot(box_height[k], total_Flux[k], 'o-')#, label ='height above $\Sigma$: '+ str(box_height[k]))
#plt.plot(box_height, totalFlux, '-o')
plt.xlabel("height above $\Sigma$ (m)")
plt.ylabel("Total Flux")# (mol/s)")
plt.title("Total Flux via boxes")
plt.grid()
plt.ylim(0.0E-05,1.50E-05)
plt.legend()
#plt.savefig("total_flux_box_" + str(box_height) + ".pdf")
plt.savefig("total_flux_box_.pdf")

###############################################################
#################################################################
#################################################################
print("*** Creating plots ***")

### Plot 0:
plt.figure()

# Evaluate fluxes along a line
x_space = np.linspace((drop_center-0.0035),(drop_center+0.0035),300)
y_space = np.full_like(x_space, 1.0)

# x_space = np.linspace(0.0,0.011,300)
# y_space = np.full_like(x_space, 1.0)

distances = [0.0001, 0.00025,0.0005,0.00075,0.001]

x_space_shifted = x_space - x_space[0]
x_space_mod = np.linspace((0.006-0.0035),(0.006+0.0035),300)

formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-3, -3))  # Set the power limits to (-3, -3) to keep 10^-3 at the corner

for distance in distances: #-drop_center
    plt.plot((x_space_mod),diffusion_flux_1_interpolator(x_space,y_space*distance),label="y="+str(distance*1000.0)+" mm")

# Use ScalarFormatter to format the x-axis ticks

plt.gca().xaxis.set_major_formatter(formatter)
plt.gca().yaxis.set_major_formatter(formatter)

plt.axvline(x=(0.0045), color='black', linestyle='--',label='contact line')
plt.axvline(x=(0.0075), color='black', linestyle='--')

# plt.title("y-component of diffusive flux")
plt.xlabel("X / (m)")
plt.ylabel("Y-component of diffusive flux / $\mathrm{(mol/m^2s)}$")
plt.legend(loc='upper right',prop={'size': 9})#, bbox_to_anchor=(1.00, 1.0))
plt.savefig("diffusion_flux_Y_comp.pdf",bbox_inches='tight')
# plt.xlabel("x (mm)")
# plt.ylabel("y-component of diffusive flux $\mathrm{(mol/mm^2s)}$")
# plt.legend(loc='upper right',prop={'size': 9})#, bbox_to_anchor=(1.00, 1.0))
# plt.savefig("diffusion_flux_Y_comp_poster.pdf",bbox_inches='tight')

## Plot -1
plt.figure()
for distance in distances:
    plt.plot((x_space_mod),convective_flux_1_interpolator(x_space,y_space*distance),label="y="+str(distance*1000.0)+" mm")

plt.axvline(x=(0.0045), color='black', linestyle='--',label='contact line')
plt.axvline(x=(0.0075), color='black', linestyle='--')

plt.gca().xaxis.set_major_formatter(formatter)
plt.gca().yaxis.set_major_formatter(formatter)
#plt.title("y-component of convective flux")
plt.xlabel("X / (m)")
plt.ylabel("Y-component of convective flux / $\mathrm{(mol/m^2s)}$")
plt.legend(loc='lower right', prop={'size': 9}) #bbox_to_anchor=(1.00, 1.0)
plt.savefig("convective_flux_Y_comp.pdf",bbox_inches='tight')

# #### Plot1: Create a plot of concentration field with iso contours

# ## Define list of conc contours to draw
# conc_levels = np.asarray([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])*max_conc

# fig = plt.figure()
# ax = fig.add_subplot()
# sc = ax.scatter(meshes["internal"]["coords_0"], meshes["internal"]["coords_1"], c=np.array(meshes["internal"]["C"]), cmap = 'viridis_r')
# ax.tricontour(triang,meshes["internal"]["C"],levels=conc_levels, colors='red', linestyles='dotted')

# # Add a color bar to the plot
# cbar = plt.colorbar(sc)

# # Restrict to region of interest
# x_lim=[drop_center-plot_height/2, drop_center+plot_height/2]
# y_lim=[0, plot_height]


# ax.set_xlim(x_lim)
# ax.set_ylim(y_lim)

# # Set the axis labels
# ax.set_xlabel('X [m]')
# ax.set_ylabel('Y [m]')

# # draw integration box_width
# for j in range(len(box_height)):
#     ax.axhline(y=box_height[j], color='white', linestyle='-')
#     ax.axvline(x=drop_center-box_width[j]/2.0, color='white', linestyle='-')
#     ax.axvline(x=drop_center+box_width[j]/2.0, color='white', linestyle='-')

# Save the plot
#plt.savefig("concentration.pdf")

#sys.exit() ## TODO development stop

# #### Plot2:
# plt.figure()
# plt.pcolormesh(Xi, Yi, diffusion_flux_1_interpolation, cmap = 'viridis_r',shading='auto')
# plt.colorbar()
# plt.title("Y-Component of diffusion flux")
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.savefig("diffusion_flux_Y.pdf")

# #### Plot3:
# plt.figure()
# plt.pcolormesh(Xi, Yi, diffusion_flux_0_interpolation, cmap = 'viridis_r',shading='auto')
# plt.colorbar()
# plt.title("X-Component of diffusion flux")
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.savefig("diffusion_flux_X.pdf")

# #### Plot4:
# plt.figure()
# plt.pcolormesh(Xi, Yi, convective_flux_1_interpolation, cmap = 'viridis_r',shading='auto')
# plt.colorbar()
# plt.title("Y-Component of convective flux")
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.savefig("convective_flux_Y.pdf")

# #### Plot5:
# plt.figure()
# plt.pcolormesh(Xi, Yi, convective_flux_0_interpolation, cmap = 'viridis_r',shading='auto')
# plt.colorbar()
# plt.title("X-Component of convective flux")
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.savefig("convective_flux_X.pdf")


# run plot_divergence.py

print("*** DONE ***")
