import numpy as np

def substr_average_per_column(matrix):
    col_averages = np.mean(matrix, axis=0)
    print ('col_averages:', col_averages.shape, col_averages)
    matrix_centered = matrix - col_averages
    np.savetxt('MatrixCenteredCol.out', matrix_centered, fmt='%10.5f')
    return matrix_centered


def approx_error(X, E, diag, eps=1e-1): # E - eigenValues, D - eigenvectors;
    print('E.shape =', E.shape)
    print('diag.shape =', diag.shape, 'diag =', diag) #either I can construct a matrix out of it, or just multiply by needed values;
    print('X.shape =', X.shape)

    Y = substr_average_per_column(np.dot(X, E))# E.T, X))
    #D_inv = [1/i if i != 0 else 0 for i in diag]
    #print ('D inverse', D_inv)
    mask = abs(diag)>abs(diag).max()*eps
    print('mask.sum()', mask.sum())

    #error = np.dot(Y_matr, D_inv )#, Y_matr.T)
    #error = np.dot(Y_squared, D_inv) # the way I calculate it through matrices:
       
    error = np.einsum("il,l,il->i", Y[:, mask], 1/diag[mask], Y[:, mask]) #Y
    
    #print('err:\n', error, '\n', error2)
    #np.savetxt('ApproxError.out', error2, fmt='%10.5f')
    return error


def approx_error2(X, E, diag, eps=1e-1): # E - eigenValues, D - eigenvectors;
    print('E.shape =', E.shape)
    print('diag.shape =', diag.shape, 'diag =', diag) #either I can construct a matrix out of it, or just multiply by needed values;
    print('X.shape =', X.shape)

    Y = substr_average_per_column(np.dot(X, E))# E.T, X))
    treshold = abs(diag.max())*eps
    D_inv = [1/i if abs(i) > treshold else 0 for i in diag]

    #Alternative:
    diag_len = diag.shape[0]
    d = np.zeros((diag_len, diag_len), int)
    np.fill_diagonal(d, [1,2,3])
    prod1 = np.dot(Y, d)
    prod2 = np.dot(prod1, Y.T)
    error = np.diag(prod2)

    return error

def extend_with_Fweights(arr, fweights):
    print('arr.shape =', arr.shape, 'fweights.shape =', fweights.shape)
    if (arr.shape != fweights.shape):
        raise error('Sizes of arrays are different. Check it!')
    else:
        extened_arr = []

        for i in range(0, arr.shape[0]):
            #print(arr[i], fweights[i])
            # fweights[i] <- Number of times I need to repeat the item from arr;
            for j in range(0, int(fweights[i])):
                extened_arr.append(arr[i])
        
        ext = np.array(extened_arr)
        print ('Extended error: ', ext.shape)
        return extened_arr 


######### Input: ############
path = 'ChiaraTS_diff-weights/geOpt/' #'100k_interrupt/without_const_par/' #'water_2/alternative/1/'#'10k_777/2-extend/2_only/' #'100k_interrupt/'#' 
matrix = np.loadtxt(path +'MatrixNormalized.out')#('MatrixNormalized.out') <-Repeat everything with normalized matrix;

fweights_in = np.loadtxt(path +'Fweights.out')
print('matrix shape:', matrix.shape)
print('fweights shape:', fweights_in.shape)
print('Fweights:', fweights_in)
##############################

######### calculate Cov, eigenvalues, eigenvectors:
covariance = np.cov(matrix.T, fweights=fweights_in) # was matrix.T
print('Covariance shape:', covariance.shape)
np.savetxt('Covariance.out', covariance, fmt='%10.5f')

eigen_values, eigen_vectors = np.linalg.eigh(covariance)
#print('eigenValues:', eigen_values.shape, eigen_values)
#print('eigenVectors', eigen_vectors.shape, eigen_vectors)
np.savetxt('eigenValues.out', eigen_values)
np.savetxt('eigenVectors.out', eigen_vectors, fmt='%10.5f')


######## Approximate error: ################### 
err = approx_error(matrix, eigen_vectors, eigen_values)
# TODO: duplicate error, according to fweights:
err_ext = extend_with_Fweights(err, fweights_in)
np.savetxt('ApproxError.out', err, fmt='%10.5f') #err_ext


err = approx_error2(matrix, eigen_vectors, eigen_values)
# TODO: duplicate error, according to fweights:
err_ext = extend_with_Fweights(err, fweights_in)
np.savetxt('ApproxError2.out', err, fmt='%10.5f') #err_ext
###########################################################


# Rotate data:
# ? Multiply matrix[101* 5659] by eigenvectors[101*101]:
# Also I have to calculate average and sybtract it! 
mean = np.mean(matrix)
print('mean =', mean)
rotatedmatrix = np.dot(matrix - mean, eigen_vectors)
print('rotated matrix', rotatedmatrix.shape)
np.savetxt('rotatedmatrix.out', rotatedmatrix, fmt='%10.5f')

import matplotlib.pyplot as plt
#last 5, because the last are the greatest -> principle components;
for index in range(matrix.shape[1]-1, matrix.shape[1]-5, -1):
    plt.clf()
    plt.plot(rotatedmatrix[:, index])
    plt.savefig('projected_parameter_{:04d}.png'.format(index))

#for matrix.shape :
# For every row: 
autocorrelation = np.array([np.convolve(matrix[i,:], matrix[i,:]) for i in range(0, matrix.shape[0])])
print('autocorrelation', autocorrelation.shape)
np.savetxt('autocorrelation.out', autocorrelation, fmt = '%10.5f')
#autocorrelation =[ np.convlove(matrix[i,:], matrix[i,:]) ]

