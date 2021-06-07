import pandas as pd
import numpy as np
import yaml

#TODO: double-check this; 
block_id = {'general' : 1, 
            'atoms'   : 2,
            'bonds'   : 3,
            'offdiagonal':4,
            'angles'  : 5,
            'torsions' : 6,
            'hydrogen': 7,
}


ommit_blocks = ['general', 'info', None]

def all_block_params(in_yaml_file, blockname):
    all_block_params = [list(ff[blockname].values()) for ff in in_yaml_file]
    all_block_params = [item for sublist in all_block_params for item in sublist] #flatten the list

    #all_block_params = [item for sublist in all_block_params for item in sublist] #flatten the list
    all_block_params = flatten_list(all_block_params)
    #print ("LEN all_block_params:", len(all_block_params))
    #[print(type(i[0])) for i in all_block_params]

    block_params = np.array(all_block_params)
    #print (blockname, "block params:", block_params)#, block_params)
    return block_params


def flatten_list(lst):
    print ("\n Flattening list:")
    print(" >  Len LST:", len(lst))
    new_flat_list = []
    for l in lst:
        if (type(l[0]) == list):
            print ("This item:", l[0])
            new_flat_list.extend(l)

        else:
            new_flat_list.append(l)

    #print(any(isinstance(el, list) for el in lst))

    print(" <  Len LST:", len(new_flat_list), " and the whole list: ", new_flat_list) # new_flat_list
    flat_np = np.array(new_flat_list)
    print("  flat shape:", type(flat_np), flat_np.shape, flat_np)
    return new_flat_list


def min_max_per_block(in_yaml_file, blockname):
    block_params = all_block_params(in_yaml_file, blockname)
    print(" >>", blockname, ">>" , block_params.shape)
    
    #MIN_MAX:
    #min_block_params = np.amin(block_params, axis = 0 )
    #max_block_params = np.amax(block_params, axis = 0 )

    #Quartiles: 
    min_block_params = np.percentile(block_params, 25, axis = 0 )
    max_block_params = np.percentile(block_params, 75, axis = 0)


    min_max = np.vstack((min_block_params, max_block_params))
    print(name, 'MINMAX:', min_max.shape)
    return min_max


with open('/Users/anna/DataBase/FF-Tool/dataBase.yml', 'r') as f:
    yaml_file = yaml.load(f)
    #print('YAML file:', yaml_file, '\n')

    #[f.pop(None) for f in yaml_file] # To exclude None from the Keys.

    #block_names = yaml_file[0].keys() - ommit_blocks
    #print ('Block names:', block_names)

    #[print('KK = ', ff['atoms'].keys()) for ff in yaml_file]

    
    out_str = str()
    
    # Hacky way: 
    block_names = ['atoms', 'bonds', 'offdiagonal' , 'angles', 'torsions', 'hydrogen']
    #block_names = ['angles']

    for name in block_names:
        # Gathering all the params together; 
        min_max = min_max_per_block(yaml_file, name)

        for i in range(0, min_max.shape[1]):
            #s = str(block_id[name]) + ' * ' +  str(i+1) + ' *  '+ str(min_max[0][i]) + '   ' + str(min_max[1][i]) + '\n'
            s = str(block_id[name]) + '  ' +  str(i+1) + '  '+ str(min_max[0][i]) + '   ' + str(min_max[1][i]) + '\n'
            out_str += s
    
    print("OUT_STR:\n", out_str)

    with open("universal-quartile-ranges", "w") as text_file:
        text_file.write(out_str)


print("Worked!")
#print(df.head())