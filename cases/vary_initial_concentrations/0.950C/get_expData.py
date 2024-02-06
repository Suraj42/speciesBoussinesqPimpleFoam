import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
import csv
import pandas as pd
import sys
#sys.path.append('/usr/local/lib/python3.8/dist-packages/')
#from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


####### Problem parameters ########
# Define inner region
x_inner_left = 0.0955
x_inner_right = 0.1065
height_inner = 0.0105765
film_center = 0.1015
x_left_film_center = x_inner_left + 4.5E-03 + 1.5E-03
# Define outer region
x_outer_left = 0.0
x_outer_right = 0.203
height_outer = 0.1
#################

concentration_matrix = np.load('../../../data/experimental_concentration_data/concentration_matrix_0_1.npy')
nan_rows = np.isnan(concentration_matrix).all(axis=1)
concentration_matrix = concentration_matrix[~nan_rows]
#print(filtered_arr)
# Iterate over the rows and copy values from the row before NaN row
for i in range(0, concentration_matrix.shape[0]):
    if np.isnan(concentration_matrix[i]).any():
        concentration_matrix[i] = concentration_matrix[i-1]
print("concentration_matrix: " + str(concentration_matrix.shape))

x1 = np.linspace(x_inner_left, x_inner_right, concentration_matrix.shape[1])
y1 = np.linspace(0, height_inner, concentration_matrix.shape[0])
yf = np.flipud(y1)
# Perform bilinear interpolation
interp_func = interp2d(x1, yf, concentration_matrix, kind='quintic')
f_inner = np.vectorize(interp_func)
# the function f_inner is defined onto the inner domain
# def f_inner(x,y):
#     # continous function with non-zero value inside inner region
#     # (plus some safety margins)

#     #return 0.5*(x**2+y**2)
#     return 1.0

###############
x_focus_point = x_left_film_center

def inside_check(x, y):
    # check if given points are in the extension domain
    # works for arrays
    # will return 1 if points (x, y) are in the inner domain
    # will return 0 if the points (x, y) are in the outer domain

    val = np.zeros_like(x)  # Initialize an array with zeros of the same shape as x

    mask_x = np.logical_and(x_inner_left <= x, x <= x_inner_right)  # Create a boolean mask for x
    mask_y = np.logical_and(0 <= y, y <= height_inner)  # Create a boolean mask for y

    mask = np.logical_and(mask_x, mask_y)  # Combine the masks

    val[mask] = 1  # Set the elements where the condition is True to 1

    return val

def extended_function(x,y):
    # pointwise evaluation of the extended function
    if(inside_check(x,y)==1):
        # point is inside, evaluate f_inner
        return f_inner(x,y)
    else:

        return_value = 0.0 # preset return_value

        # compute the connection ray
        # compute the normalized ray vector
        ray_vector = np.array([x-x_focus_point,y])
        ray_vector = ray_vector/np.linalg.norm(ray_vector) # normalize the vector
        # compute the ray angle
        cos_alpha = ray_vector[0]

        # compute critical ray angles (directions) with respect to the inner box
        ray_vector_right_crictical_inner = np.array([x_inner_right-x_focus_point,height_inner])
        ray_vector_right_crictical_inner = ray_vector_right_crictical_inner/np.linalg.norm(ray_vector_right_crictical_inner)
        cos_alpha_critical_right_inner = ray_vector_right_crictical_inner[0]

        ray_vector_left_crictical_inner = np.array([x_inner_left-x_focus_point,height_inner])
        ray_vector_left_crictical_inner = ray_vector_left_crictical_inner/np.linalg.norm(ray_vector_left_crictical_inner)
        cos_alpha_critical_left_inner = ray_vector_left_crictical_inner[0]

        # compute critical ray angles (directions) with respect to the outer box
        ray_vector_right_critical_outer = np.array([x_outer_right-x_focus_point,height_outer])
        ray_vector_right_critical_outer = ray_vector_right_critical_outer/np.linalg.norm(ray_vector_right_critical_outer)
        cos_alpha_critical_right_outer = ray_vector_right_critical_outer[0]

        ray_vector_left_critical_outer = np.array([x_outer_left-x_focus_point,height_outer])
        ray_vector_left_critical_outer = ray_vector_left_critical_outer/np.linalg.norm(ray_vector_left_critical_outer)
        cos_alpha_critical_left_outer = ray_vector_left_critical_outer[0]

        # ray equation gamma(s) = focus_point + s*ray_vector
        def parametrized_ray(s,normal_vector):
            return np.array([x_focus_point,0.0])+s*normal_vector

        # compute intersection with inner box
        if(cos_alpha > cos_alpha_critical_right_inner):
            # ray hits right part of inner box

            # compute the parameter for inner intersection point
            ray_parameter_inner_intersection = (x_inner_right-x_focus_point)/ray_vector[0]

        elif(cos_alpha < cos_alpha_critical_left_inner):
            # ray hits right part of the inner box

            # compute the parameter for inner intersection point
            ray_parameter_inner_intersection = (x_inner_left-x_focus_point)/ray_vector[0]

        else:
            # the ray hits the top part of the inner box

            # compute the parameter for inner intersection point
            ray_parameter_inner_intersection = height_inner/ray_vector[1]

        # compute inner intersection point from ray parameter
        inner_intersection_point = parametrized_ray(ray_parameter_inner_intersection,ray_vector)
        # get the boundary value from the inner boundary
        inner_boundary_value = f_inner(inner_intersection_point[0],inner_intersection_point[1])

        ###################

        # compute intersection with outer box
        if(cos_alpha > cos_alpha_critical_right_outer):
            # ray hits right part of outer box

            # compute the parameter for outer intersection point
            ray_parameter_outer_intersection = (x_outer_right-x_focus_point)/ray_vector[0]
            #return_value = 1.0 # dummy/debug code

        elif(cos_alpha < cos_alpha_critical_left_outer):
            # ray hits left part of outer box

            # compute the parameter for outer intersection point
            ray_parameter_outer_intersection = (x_outer_left-x_focus_point)/ray_vector[0]
            #return_value = 0.0 # dummy/debug code

        else:
            # ray hits top part of outer box

            # compute the parameter for outer intersection point
            ray_parameter_outer_intersection = height_outer/ray_vector[1]
            #return_value = -1.0 # dummy/debug code

        # compute outer intersection point from ray parameter
        outer_intersection_point = parametrized_ray(ray_parameter_outer_intersection,ray_vector)

        # compute value at point of interest (x,y) using a convex combination of outer and inner intersection points

        # Compute gamma parameter for (x,y). By definition of the normal, we have
        # parametrized_ray(s=norm(np.array([x-x_focus_point,y])))=(x,y)
        local_ray_parameter = np.linalg.norm(np.array([x-x_focus_point,y]))
        # Compute the rescaled_ray_parameter which is zero at the inner intersection point logical_and
        # one at the outer intersection point
        rescaled_ray_parameter = (local_ray_parameter-ray_parameter_inner_intersection)/(ray_parameter_outer_intersection-ray_parameter_inner_intersection)

        return_value = inner_boundary_value*(1.0-rescaled_ray_parameter)

        return return_value

extended_function_vectorized = np.vectorize(extended_function)

########################
### Ploting results ####
########################

# # define a grid for the whole space
# x_space = np.linspace(x_outer_left,x_outer_right,1000)
# y_space = np.linspace(0.0,height_outer,1000)

# # Generate the meshgrid from the grid points
# X, Y = np.meshgrid(x_space, y_space)
# # Calculate the function values for each point in the meshgrid
# Z1 = f_inner(X, Y)
# Z2 = inside_check(X,Y)
# Z3 = extended_function_vectorized(X,Y)

# # Create a 2D colormap plot
# plt.figure(dpi=150)
# plt.pcolormesh(X, Y, Z3, cmap='viridis_r', shading = 'nearest')
# plt.colorbar(label='concentration, $mol /$ $m^{3}$')

# # Add the inner box
# plt.axvline(x=x_inner_left, ymin=0.0, ymax=height_inner, color='red', linestyle='-')
# plt.axvline(x=x_inner_right, ymin=0.0, ymax=height_inner, color='red', linestyle='-')
# plt.plot([x_inner_left, x_inner_right], [height_inner, height_inner], color='red', linestyle='-')

# # Set labels and title
# plt.xlabel('X (in m)')
# plt.ylabel('Y (in m)')

# # Display the plot
# plt.savefig("ray_extension.pdf", bbox_inches = 'tight')


########################
### Ploting results ####
########################
cells = pd.read_csv('cellCentres.csv', delimiter = ', ', engine='python')#

x1 = cells['x']
y1 = cells['y']
z1 = cells['z']
print(len(x1))
Z11 = f_inner(x1, y1)
print("done f inner")
Z22 = inside_check(x1, y1)
print("done inside check")
Z33 = extended_function_vectorized(x1, y1)
#print(Z33)
print("done extended ray calc")

# Save the array to a file
with open('constant/initialFieldValues.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for el in Z33:
        writer.writerow([float(el)])

print("Done writing file with interpolated field values")

