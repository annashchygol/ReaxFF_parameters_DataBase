import numpy as np

params_ranges = './params-ranges'
gen_params = './ga-param' 

ranges = np.loadtxt(params_ranges)
params = np.loadtxt(gen_params)

print ("RANGES shape = ", ranges.shape)
print("PARAMS shape = ", params.shape)

print("Some params:",  params[0:5] ) 
print("MIN / MAX ranges:", ranges[0][4], ranges[0][5])

# min -> column #4
# max -> column #5
for l in zip(params, ranges):

    r_min = min(l[1][4], l[1][5])
    r_max = max(l[1][4], l[1][5])

    if l[0] < r_min or l[0] > r_max:
        print(l[0], l[1][4], l[1][5]) 
    else:
        print ("Fine!")