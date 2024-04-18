#redistribute, but in Python, and detects duplicate symmetries 
#to avoid wasting cpus.

import argparse
import os 
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num_proc',  help='approximate number of proc.',type=int)
args = parser.parse_args()



def read_sizeBP():
    sizeBP = open('sizeBP.dat','r')
    sizeBP_read = sizeBP.readlines()
    sizeBP.close()
    size_of_matrix = []
    size_of_matrix_cubed = []
    symmetries = []
    for jj in range(0,len(sizeBP_read)):
        current_line = sizeBP_read[jj].split()
        two_j = current_line[4]
        parity = current_line[6]
        sym = two_j+'_'+parity
        size = int(current_line[2])
        size_of_matrix.append(size)
        size_of_matrix_cubed.append(size**3)
        symmetries.append(sym)

    #detects which symmetries will be opened twice. 

    return size_of_matrix,size_of_matrix_cubed,symmetries

def read_sizeH():
    sizeH = open('sizeH.dat','r')
    sizeH_read = sizeH.readlines()
    sizeH.close()
    size_of_matrix = []
    size_of_matrix_cubed = []
    symmetries = []
    for jj in range(0,len(sizeH_read)):
        current_line = sizeH_read[jj].split()
        mult = current_line[9]
        ang = current_line[10]
        parity = current_line[11]
        sym = mult+'_'+ang+'_'+parity
        size = int(current_line[8])
        size_of_matrix.append(size)
        size_of_matrix_cubed.append(size**3)
        symmetries.append(sym)

    #detects which symmetries will be opened twice. 

    return size_of_matrix_cubed,symmetries

def main(estimate_num_cpu):


    #print(already_done_boolean_array)
    if os.path.exists('sizeBP.dat'):
        size_of_matrix_cubed,symmetries = read_sizeBP()
    elif os.path.exists('sizeH.dat'):
        print('size H implemented - but not tested')
        size_of_matrix_cubed,symmetries = read_sizeH()
    else:
        print('no sizeBP or sizeH - check directory')
        exit()

    already_found = []
    already_done_boolean_array = []
    for sym in symmetries:
        if sym in already_found:
            already_done_boolean_array.append(True)
        else:
            already_done_boolean_array.append(False)
            already_found.append(sym)

    sum_of_cubed_sizes = sum(size_of_matrix_cubed)

    import math as m


    mindim = 1
    start = 1
    finish = 0

    dist_dat = open('DISTRIBUTE.DAT','w')

    for jj in range(0,len(size_of_matrix_cubed)):
        start = finish+1

        if already_done_boolean_array[jj]:
            #if this is a symmetry that's going to be looked at twice - only give it a single core the second time.
            #the code skips it, so better than giving it 10 cores that are wasted.
            r = mindim
        else:
            size_cubed = size_of_matrix_cubed[jj] 
            distr = float(size_cubed) / sum_of_cubed_sizes * estimate_num_cpu
            r = m.sqrt(distr) + mindim 


        finish = start + int(r) * int(r) -1 
        string = '{:6}{:6}{:6}{:6}\n'
        dist_dat.write(string.format(start-1,finish-1,int(r),int(r)))
    dist_dat.close()
    print('You need {} processors'.format(finish))

if args.num_proc:
    if args.num_proc > 0:
        main(args.num_proc)
    else:
        print('invalid num procs.')
else:
    print('run again with -n num_procs')