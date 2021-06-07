# Numpy array analysis;

#TODO:
# 1. Get numpy arrays; 
# 2. Normalize array by ranges:

import numpy as np

def nullify(matr, eps = 0.0000000000000000001): # this can be done through lamda expressions:
	for (x,y), value in np.ndenumerate(matr):
		#print (' > value :', value)
		if value <= eps:
			value = 0
	return matr


def normalize(column, min_val, max_val):
	#logging.debug('Normalising parameter')
	eps = 0.000000000000001
	if abs(min_val - max_val) <= eps: # in fact - it's ill-defined condition.
		return np.zeros(column.shape) # this should be vector of 0s, not just one number; 
	elif abs(min_val) > eps and max_val:
		if min_val != max_val:
			return (column - min_val) / (max_val - min_val)
		else:
			return column / min_val
	elif abs(max_val) > eps:
		return (column / max_val) # < I receive an error here, while max_val == 0; 
	else:
		print('Went into this condition')
		return (column - min_val) # starting condition


def extractNeededKeys(dataBase, keys, minFF=None, maxFF=None):
	print('Extraction....')

	matrix = []
	normalized_matrix = []
	for block in keys:
		print('', block)

		for keyLst in keys[block]:
			# Num of params to be optimised; Be careful: inside array - indexing starts from 0; 
			indxsToOpt = np.array(keys[block][keyLst])
			updatedIndxsToOpt = indxsToOpt - 1 
			print('toOpt', indxsToOpt)
			keysLst = keyLst.split(', ')
			print('key', keyLst)
			
			for k in keysLst:
				print(k)
				#This is the exact key; parameters of which we should search in the dataBase:

				l = [it[block][k] for it in dataBase]
				arr = np.array(l)
				
				for columnIndex in updatedIndxsToOpt:

					if arr.ndim == 2:
						column = arr[:,columnIndex]

						if minFF and maxFF: #___Normalization_prep:
							min_val = minFF[block][k][columnIndex]
							max_val = maxFF[block][k][columnIndex]
							if (min_val == max_val):
								print('min/max val:', min_val, max_val, 'col = ', columnIndex)

						normalized_column = normalize(column, min_val, max_val) #(column - min_val) / (max_val - min_val)
						print('#',columnIndex, '= \n', column, '\n', normalized_column )
						matrix.append(column)
						normalized_matrix.append(normalized_column)

					elif arr.ndim == 3:
						print('Extra dim is needed')
						print('Shape:', arr.shape,'columnIndex', columnIndex)
						#print('#', columnIndex)
						#if columnIndex < np.shape(arr)[2]: <-excessive a bit;
						first  = arr[:,0,columnIndex]  # Level: Item in a  first list;
						second = arr[:,1,columnIndex] # Level: Item in a second list: 
						#print('First:', first)
						#print('Second:', second)
						matrix.append(first)
						matrix.append(second)

						# Here I should also treat them separately
						# Lines are duplictaed -> separate function out of it; 
						min_val = minFF[block][k][0][columnIndex]
						max_val = maxFF[block][k][0][columnIndex] # Ranges are the same for the same type of parameter; => 0 - is enough; 
						
						if (min_val == max_val):
							print('min/max val:', min_val, max_val, 'col = ', columnIndex)

						norm_first = normalize(first, min_val, max_val)

						#print('min/max val:', min_val, max_val)
						norm_second = normalize(second, min_val, max_val)
						normalized_matrix.append(norm_first)
						normalized_matrix.append(norm_second)

						# what problems do we get here ??? there is not even access to index; 
			Matrix = np.array(matrix).T # to have data by columns per each parameter;
			Matrix_norm = np.array(normalized_matrix).T
			#print('Matrix:', np.shape(Matrix),'\n', Matrix)
			np.savetxt('Matrix.out', Matrix, fmt = '%10.5f')
			#print('Matrix_norm:', Matrix_norm)
			Matrix_norm = nullify(Matrix_norm)
			np.savetxt('MatrixNormalized.out', Matrix_norm, fmt = '%10.5f')

	return Matrix