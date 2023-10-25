#import numpy as np
from numpy import ogrid, sqrt, zeros, vstack, logical_and
from scipy.sparse import lil_array
from scipy.sparse.linalg import spsolve
from math import ceil


#Function definiton (uber function is at the bottom)
#Geometry init
def init_l(dx, width, geo, l_top=None):
    """
    Initialize the geometry array 'l' based on the provided parameters.

    Parameters:
    dx (float): The spacing or resolution for discretizing the 'l' array.
    width (float): The width of the 'l' array.
    geo (list): A list describing the geometry of the system.
                Each element in the list should be a sublist with the format:
                [height, lambda_value, cap_info]
                where 'height' is the height of the geometry segment,
                'lambda_value' is the corresponding lambda value,
                and 'cap_info' is an optional sublist with capillary information.
                The capillary information should have the format:
                [r1, r2, cap_low, lambda_cap],
                where 'r1' and 'r2' are the radii of the capillary,
                'cap_low' is the lower bound of the capillary segment,
                and 'lambda_cap' is the lambda value for the capillary.
    l_top (float or None): The lambda value for the top layer of the system.
                           If None, the top layer lambda value will be set to 0.

    Returns:
    tuple: A tuple containing three elements:
           - l (numpy.ndarray): The geometry array 'l' with lambda values.
           - water_mask (numpy.ndarray): A binary array denoting water locations.
           - center (float): The center position of the capillary segment.

    Note:
    - The lambda value for water is set to a default value of 0.6089.
    - The 'l' array represents the lambda values of the system geometry.
    - The 'water_mask' array is a binary array with True values representing water locations.
    """
    l_water = 0.6089 #from wiki
    #Initialize the geometry array of l(i, j)
    #calculate total system height
    height = sum([sublist[0] for sublist in geo])
    l = zeros((int(height/dx), int(width/dx)))
    #Fill the geometry array
    lower_bound = 0

    for i in geo:
        l_height = int(i[0]/dx)
        l[lower_bound:(lower_bound+l_height)] = i[1]

        #Fill in capillary

        if len(i) == 3:
            cap_info = i[2]
            # Extract capillary information and set variables
            r1 = cap_info[0] / dx # Inner radius of capillary
            r2 = cap_info[1] / dx  # Outer radius of capillary
            cap_low = int(lower_bound + cap_info[2]/dx) # Lower bound of capillary
            cap_high = int(cap_low+2*r2)  # Upper bound of capillary height
            center = cap_low  + r2 # Center of the capillary
            # Create 2D distance array
            ly, lx = ogrid[cap_low:cap_high+1, 0:ceil(2*r2)+1]
            dist = sqrt((ly - center) ** 2 + lx ** 2)
            # Fudge coefficient, helps to fill all elements
            eps = 0.25
            
            # Set lambda in the Water zone
            l[cap_low:cap_high + 1, 0:ceil(2 * r2) + 1][dist <= r1] = l_water

            # Set capillary lambda
            l[cap_low:cap_high + 1, 0:ceil(2 * r2) + 1][logical_and(r1 - eps < dist, dist < r2 + eps)] = cap_info[-1]
            


        lower_bound += l_height
    
    #Make binary water mask
    water_mask = l==l_water

    return l, water_mask, center


###Linear system of eqs
def init_Ab(l, t_top, t_water, water_mask, q, dx, l_top):  
    """
    Initialize the coefficient matrix A, the solution vector b, and the padding value for the heat equation solver.

    Args:
        l (ndarray): Geometry array of size (ny, nx) representing the thermal conductivity at each grid point.
        t_top (float): Temperature at the top boundary.
        t_water (float): Temperature of the water.
        water_mask (ndarray): Binary array indicating the locations of water cells in the grid.
        q (float): Heat flow at the bottom boundary.
        dx (float): Grid spacing.
        l_top (float, optional): Thermal conductivity at the top boundary. Defaults to None.

    Returns:
        csr_matrix: Coefficient matrix A of size (N, N), where N is the total number of grid points.
        ndarray: Solution vector b of size (N,).
        int: Padding value (1 or 2) used for grid shape modification.

    Notes:
        - This function initializes the coefficient matrix A, the solution vector b, and determines the required padding for the grid based on the input parameters.
        - The heat equation is solved on a 2D grid with ny rows and nx columns.
        - The function handles both Dirichlet and convective boundary conditions.
        - For Dirichlet boundary conditions, the temperature values at the boundaries are fixed.
        - For convective boundary conditions, a convective heat flow term is added to the top boundary.
    """
    # Define the grid parameters
    ny, nx = l.shape
    
    # Shape modification for padding
    if l_top == None:
        pad = 1
        ny += pad # Padding for bottom ghost cell
    else:
        pad = 2
        ny += pad # Adds padding for top ghost cell
    
    # Create the coefficient matrix A and b vector
    A = lil_array((nx*ny, nx*ny))
    b = zeros((nx*ny))

    
    # Pad l to avoid indexing problems
    line = l[0]
    l = vstack((line,l))
    if pad == 2:
        line = l[-1]
        l = vstack((l,line))
    
    # Pad water_mask
    line = water_mask[0]
    water_mask = vstack((line,water_mask))
    if pad == 2:
        line = water_mask[-1]
        water_mask = vstack((water_mask,line))
    
    # Constants in b
    # Top
    b[(len(b)-nx):] = t_top
        
    # Water
    b[water_mask.flatten()] = t_water

    
    # Bottom boundary derivative
    b[:nx] = -(0.1/1000)*q/l[1,-1] #h*q/lambda  #q is in (w/m^2), i take its as h thick, and /1e3

    
    #Loop over A and fill in elements

    #CONSTANT BC
    if l_top == None:
        print("CONSTANT BC")
        
        # Medium
        for i in range(1,ny-1):
            for j in range(1,nx-1):
                k = i*nx+j

                if not water_mask[i,j]:
                    ip = 2/(1/l[i+1,j]+1/l[i,j]) #i+1,j
                    im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
                    jp = 2/(1/l[i,j+1]+1/l[i,j]) #i,j+1
                    jm = 2/(1/l[i,j-1]+1/l[i,j]) #i,j-1
                    diagonal = -(ip+im+jp+jm)

                    A[k,k] = diagonal
                    A[k,k+nx] = ip
                    A[k,k-nx] = im
                    A[k,k+1] = jp
                    A[k,k-1] = jm

                # Constant for water
                else:
                    A[k,k]=1 # This misses first elements of each row of water_mask because of j range

        # Sides is 3 element average with k corrected coefficents
        for i in range(1,ny-1):
            # Left
            if not water_mask[i,0]:
                k = i*nx
                ip = 2/(1/l[i+1,j]+1/l[i,j]) #i+1,j
                im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
                jp = 2/(1/l[i,j+1]+1/l[i,j]) #i,j+1
                diagonal = -(ip+im+jp)

                A[k,k] = diagonal
                A[k,k+nx] = ip
                A[k,k-nx] = im
                A[k,k+1] = jp

            else:
                k = i*nx
                A[k,k] = 1 #water mask first element fix
   
            # Right
            k = i*nx+nx-1
            ip = 2/(1/l[i+1,j]+1/l[i,j]) #i+1,j
            im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
            jm = 2/(1/l[i,j-1]+1/l[i,j]) #i,j-1
            diagonal = -(ip+im+jm)

            A[k,k] = diagonal
            A[k,k+nx] = ip
            A[k,k-nx] = im
            A[k,k-1] = jm

        # Bottom derivative (q bc)
        for j in range(0,nx):
            k = j
            A[k,k] = 1
            A[k,k+nx] = -1

            # Top is constant temp (includig when convective bc)
            k = (ny-1)*nx+j
            A[k,k] = 1
        
        
    #CONVECTIVE BC
    else:
        print("CONVECTIVE BC")
        
        # Top 
        i = ny-2
        for j in range(1,nx-1):
                k = i*nx+j
                # Convective heat flow
                ip = ((0.1/1000)*l_top) #i+1,j #sussy
                
                im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
                jp = 2/(1/l[i,j+1]+1/l[i,j]) #i,j+1
                jm = 2/(1/l[i,j-1]+1/l[i,j]) #i,j-1
                diagonal = -(ip+im+jp+jm)

                A[k,k] = diagonal
                A[k,k+nx] = ip
                A[k,k-nx] = im
                A[k,k+1] = jp
                A[k,k-1] = jm
        
        # Top corner elements
        # Left
        j = 0
        k = i*nx+j
        
        ip = ((0.1/1000)*l_top) #i+1,j
        im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
        jp = 2/(1/l[i,j+1]+1/l[i,j]) #i,j+1
        diagonal = -(ip+im+jp)
        
        A[k,k] = diagonal
        A[k,k+nx] = ip
        A[k,k-nx] = im
        A[k,k+1] = jp
        
        # Right
        j = nx-1
        k = i*nx+j
        ip = ((0.1/1000)*l_top) #i+1,j

        im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
        jm = 2/(1/l[i,j-1]+1/l[i,j]) #i,j-1
        diagonal = -(ip+im+jm)
        
        A[k,k] = diagonal
        A[k,k+nx] = ip
        A[k,k-nx] = im
        A[k,k-1] = jm
            
        # Medium
        for i in range(1,ny-2):
            for j in range(1,nx-1):
                k = i*nx+j

                if not water_mask[i,j]:
                    ip = 2/(1/l[i+1,j]+1/l[i,j]) #i+1,j
                    im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
                    jp = 2/(1/l[i,j+1]+1/l[i,j]) #i,j+1
                    jm = 2/(1/l[i,j-1]+1/l[i,j]) #i,j-1
                    diagonal = -(ip+im+jp+jm)

                    A[k,k] = diagonal
                    A[k,k+nx] = ip
                    A[k,k-nx] = im
                    A[k,k+1] = jp
                    A[k,k-1] = jm
                    
                else:
                    A[k,k]=1
            
        # Sides is 3 element average with k corrected coefficents
        for i in range(1,ny-2):
            # Left
            if not water_mask[i,0]:

                k = i*nx
                ip = 2/(1/l[i+1,j]+1/l[i,j]) #i+1,j
                im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
                jp = 2/(1/l[i,j+1]+1/l[i,j]) #i,j+1
                diagonal = -(ip+im+jp)

                A[k,k] = diagonal
                A[k,k+nx] = ip
                A[k,k-nx] = im
                A[k,k+1] = jp

            else:
                k = i*nx
                A[k,k] = 1 # Water mask first element fix
   
            # Right
            k = i*nx+nx-1
            ip = 2/(1/l[i+1,j]+1/l[i,j]) #i+1,j
            im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
            jm = 2/(1/l[i,j-1]+1/l[i,j]) #i,j-1
            diagonal = -(ip+im+jm)

            A[k,k] = diagonal
            A[k,k+nx] = ip
            A[k,k-nx] = im
            A[k,k-1] = jm

            
        # Bottom derivative
        for j in range(0,nx):
            k = j
            A[k,k] = 1
            A[k,k+nx] = -1

            # Top is constant temp (includig when convective bc)
            k = (ny-1)*nx+j
            A[k,k] = 1

                    


    A = A.tocsr()
    
    return A, b, pad


#Itterative temp fitter
def t_fit_loop(self, A, b, pad, l, t_to_fit, t_error, maxiter, water_mask):
    """
    Solve the linear system for temperature distribution.

    Args:
        A (sparse matrix): Coefficient matrix of the linear system.
        b (array): Right-hand side vector of the linear system.
        pad (int): Padding value (1 or 2) used for grid shape modification.
        l (2D array): Geometry matrix.
        t_to_fit (float): Target temperature value to fit.
        t_error (float): Acceptable error for convergence.
        maxiter (int): Maximum number of iterations allowed.
        water_mask (2D boolean array): Mask indicating the water regions.

    Returns:
        T (2D array): Temperature distribution matrix.
        t (float): Adjusted target temperature after convergence.
    """
    t = t_to_fit
    ny, nx = l.shape
    
    iteration = 0
    diff = 1
    
    # Pad water_mask
    line = water_mask[0]
    water_mask = vstack((line,water_mask))
    if pad == 2:
        line = water_mask[-1]
        water_mask = vstack((water_mask,line))
        
    b[water_mask.flatten()] = t_to_fit
    
    while abs(diff)>t_error and iteration < maxiter:
        
        # Solve the linear system
        T = spsolve(A, b)

        # Reshape the solution vector into a 2D array
        if pad == 2:
            T = T[nx:][:-nx].reshape((ny, nx))
        else:
            T = T[nx:].reshape((ny, nx))
            
        # Calculate inner surface temp
        bot_t = T[0].mean()
        
        # Adjust guess
        diff = t_to_fit - bot_t

        iteration+=1
        t += diff
        b[water_mask.flatten()] = t

        print(iteration, diff)
    
    return T, t


#Uber black box
def fit_water_t(self, geo, width, t_to_fit, q, t_top, l_top):
    """
    Fit water temperature distribution based on the given parameters.

    Args:
        geo (array): Geometry information.
        width (float): Width of the region.
        t_to_fit (float): Target temperature value to fit.
        q (float): Heat flux.
        t_top (float): Temperature at the top boundary.
        l_top (2D array, optional): Top boundary condition.

    Returns:
        t (float): Adjusted target water temperature after convergence.
        T (2D array): Temperature distribution matrix.
    """
    dx = 0.1
    
    # Init geometry
    l, water_mask, center = init_l(dx, width, geo)
    # Init eq. system
    A, b, pad = init_Ab(l, t_top, t_to_fit, water_mask, q, dx, l_top)
    
    print("init done")
    
    # Fit desired water temperature
    t_error = 0.001
    maxiter = 20

    T,t = t_fit_loop(self, A, b, pad, l, t_to_fit, t_error, maxiter, water_mask)
    
    return t