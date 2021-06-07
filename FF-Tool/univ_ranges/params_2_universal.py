import numpy as np


# TEMPLATE: 
# 0. block_num
# 1. item_num (COPY IT)
# 2. param_num
# 3. step_size (COPY IT)
# 4. prev_min
# 5. prev_max


# UNIVERSAL: 
# 0. block_num
# 1. param_num
# 2. MIN
# 3. MAX

def get_min_max(univ_ranges, block_num, param_num):
    for val in univ_ranges:
        if val[0] == block_num and val[1] == param_num:
            return(val[2] , val[3]) # MIN and MAX
    

template_params = './uio-params-ranges'
universal_params = './universal-quartile-ranges'
upd_params = 'uio-quart-ext-params'

template = 

(template_params)
universal = np.loadtxt(universal_params)

print("TEMPL_SHAPE =", template.shape)
print("UNIV_SHAPE =", universal.shape)

out_str = ''
out_ranges = np.empty(template.shape)

for t_line in template: 
    block_num = int(t_line[0])
    item_num = int(t_line[1])
    param_num = int(t_line[2])
    step_size = t_line[3]
    old_min = float(t_line[4])
    old_max = float(t_line[5])

    new_min_max = get_min_max(universal, block_num, param_num) # <- new_min_max for extended ranges;
    
    half_diff = (new_min_max[1] - new_min_max[0])/2
    min_max = (new_min_max[0] - half_diff, new_min_max[1] + half_diff) # To extednd a bit Quartiles ranges.
    #min_max = (min(old_min, new_min_max[0]), max(old_max ,new_min_max[1])) # An option for extended ranges.   

    #out_ranges = np.append(out_ranges, np.array([block_num, item_num, param_num, step_size, min_max[0], min_max[1]]))
    t_line[4] = min_max[0]
    t_line[5] = min_max[1]
    #TODO: MAKE a numpy array and print it out altogether
    out_str += str(block_num) + ' ' + str(item_num) + ' ' + str(param_num) + '  ' + str(step_size) + '  ' + str(min_max[0]) + '  ' + str(min_max[1]) + '\n'
    
    #print(block_num, item_num, param_num, step_size , min_max[0], min_max[1])
print ("OUT_STR:\n", out_str)
print ("OUT RANGES\n", template)

with open(upd_params, "w") as text_file:
        text_file.write(out_str)

#out = np.array()
