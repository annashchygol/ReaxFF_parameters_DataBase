#Cut the columns, which are hittinp the boundary.
import numpy as np
import matplotlib.pyplot as plt

path = 'ChiaraTS_diff-weights/geOpt/'#'100k_interrupt/without_const_par/'# 'water_2/alternative/1/'
matrix = np.loadtxt(path +'MatrixNormalized.out')
orig_matr = np.loadtxt(path +'Matrix.out')
print('matrix shape =', matrix.shape)
# Columns of np.array:

counter = 0
#fig = plt.figure()

for i in range(0, matrix.shape[1]): #range(0,10)# loop through columns; 
    cur_col = matrix[:,i]
    # For now I'm checking if all of the elements are constant; 
    first_el = cur_col[0]
    last_el = cur_col[-1]
    count = np.count_nonzero(cur_col - last_el) # <- more logical to substract last element; 
    real_min = np.min(cur_col)
    real_max = np.max(cur_col)
    average = np.average(cur_col)
    
    #if (average >= 0.9 or average < 0.1):
    counter = counter + 1
    print('{:.6} {:d} {:.6} {:d}  {:.7}  {:1.4f} {:.7} {:1.4f} {:.7} {:1.4f} {:.10} {:1.4f}'.format(
        'i =', i+1 ,' #[!=0]:', count, ' min =', real_min,' max =', real_max, ' diff =', abs(real_max) - abs(real_min), ' average = ', average))

    print('{:.15} {:1.4f} {:1.4f}'.format('  >cur  col =', cur_col[0], cur_col[-1]))
    print('{:.15} {:1.4f} {:1.4f}'.format('  >orig col =', orig_matr[:,i][0], orig_matr[:,i][-1]))
    plt.plot(cur_col)
    plt.savefig('Column_{:3d}.png'.format(i+1), dpi = 100)
    plt.gcf().clear()
# Find the condition of constantly hitting the boundary.

print('counter =', counter)
print('cur_col =', cur_col)