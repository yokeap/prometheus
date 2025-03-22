import argparse
import os
import numpy as np

from cad_gen.run_script import main_cad
from utils import *
import pandas as pd
import shutil
import glob 
import subprocess
import time
#from run_dexof import *
import sys 
from cfd_sim.run_cfd import *
from cad_gen.run_script import *
# from cfd_sim.dexof_reader_class import parse_dex_file
import GPyOpt
from subprocess import PIPE, run
import random
from numpy.random import seed

# initial parameters (mm unit)  
a=0.02856; b=0.03463;c=0.04748; 
# a_ext=0;c_ext=0                                # for exp2 set a_ext & c_ext = 2500 ; It define allowable extension in nose_length & tail legth during optimization. 
data_file_name='./data_bo/bo_hull.csv'      # data file name- change for each experiment
data_opt_name = './result_opt.csv'
#

sys.dont_write_bytecode = True
cad_storage_name= './cad_gen/design_points.csv'
cfd_storage_name= './cfd_sim/design_points.csv'

# stl storage
src= './cad_gen/stl_repo'
dst='./cfd_sim/stl_cfd'

# resistance initial
resistance_storage = [120.0449041] 

def delete_dir(loc):
    print('*Deleted directory:',loc)
    shutil.rmtree(loc)

def copy_dir(src,dst):
	print('*Copied directory from',src,'to destination:',dst)
	shutil.copytree(src, dst)

def deletefiles(loc):
	print('Deleted files from location:',loc)
	file_loc= loc+'/*'
	files = glob.glob(file_loc)
	for f in files:
		os.remove(f)

def deletefiles(loc):
    print('Deleted files from location',loc)
    file_loc = loc+'/*'
    files = glob.glob(file_loc)
    for f in files:
         os.remove(f)

def saveOpt(loc):
	print("Create files from location:", loc)
	files_loc = loc + "/*"
	files = glob.glob(files_loc)
	for f in files:
		os.mkdir(f)

def copy_file(src,dst):
     print('*Copied file from',src,'to destination:',dst)
     shutil.copy(src,dst)

def save_design_points(x):
    # np.set_printoptions(precision=4)
    # print(x)
    np.savetxt(cad_storage_name,x,  delimiter=',')
    np.savetxt(cfd_storage_name,x,  delimiter=',')
          
def run_cad_cfd(x):
    print('shape of x:',x.shape)
    print(str(x[0][0])+","+str(x[0][1])+","+str(x[0][2]))

    # needs a function for check boundary because x is random which can be extrapolate
    # feasibility =

    save_design_points(np.array([x[0][0],x[0][1],x[0][2]]))

    delete_dir(dst)
    # subprocess.call('./cad_gen/run_cad.sh')
    prev = os.path.abspath(os.getcwd()) # Save the real cwd
    print('prev is',prev)
    cad_gen_path= prev+'/cad_gen'
    os.chdir(cad_gen_path)
    main_cad()
    os.chdir(prev)
    copy_dir(src,dst)
    deletefiles(src)

    prev = os.path.abspath(os.getcwd()) # Save the real cwd
    print('prev is',prev)
    cfd_sim_path= prev+'/cfd_sim'
    print('func path is:',cfd_sim_path)
    os.chdir(cfd_sim_path)
    result = main_run()
    resistance_storage.append(result)
    print('****Resistance resistance_storage:',resistance_storage)
    os.chdir(prev)
    return result


def run_bo(run_id=0,aquistion='EI',seeds=0):
    global a_ext, c_ext
	################################################
    deletefiles('./cad_sim/fig_hull')
	
    # maximum boundary
    # bounds = [{'name': 'n', 'type': 'continuous', 'domain': (1,50)},
    #         {'name': 'theta', 'type': 'continuous', 'domain': (1,50)},
    #         {'name': 'a_ext', 'type': 'continuous', 'domain': (0,a_ext)},
    #         {'name': 'c_ext', 'type': 'continuous', 'domain': (0,c_ext)}]
    bounds = [{'name': 'a', 'type': 'continuous', 'domain': (0,0.1)},
            {'name': 'b', 'type': 'continuous', 'domain': (0,0.1)},
            {'name': 'c', 'type': 'continuous', 'domain': (0,0.1)},]

    print('Bound is:',bounds)
    max_time  = None 
    max_iter  = 50
    num_iter=10
    batch= int(max_iter/num_iter)
	
    #################################################
    already_saved_opt_file = len(glob.glob(data_opt_name))
    
    if(already_saved_opt_file > 0):
         print('saved opt file exist?:',already_saved_opt_file)
         deletefiles(data_opt_name)

    already_run = len(glob.glob(data_file_name))
    print('file exist?:',already_run)

    print('Batch is:',batch)

    # make predictable random (numpy.random.seed())
    seed(seeds)
    for i in range(num_iter): 
        if already_run==1:
            evals = pd.read_csv(data_file_name, index_col=0, delimiter="\t")
            Y = np.array([[x] for x in evals["Y"]])
            X = np.array(evals.filter(regex="var*"))
            myBopt2D = GPyOpt.methods.BayesianOptimization(run_cad_cfd, bounds,model_type = 'GP',X=X, Y=Y,
                                              acquisition_type=aquistion, normalize_Y=False, 
                                              exact_feval = True) 
            print('In other runs run')
        else: 
            #  createfiles(data_file_name)
             open(data_file_name,'w')
             myBopt2D = GPyOpt.methods.BayesianOptimization(f=run_cad_cfd,
                                              domain=bounds,
                                              model_type = 'GP',
                                              acquisition_type=aquistion,  normalize_Y=False, 
                                              exact_feval = True) 
             already_run=1
             print('In 1st run')
        print('------Running batch is:',i) 

        # --- Run the optimization 
        try:
            myBopt2D.run_optimization(batch,verbosity=True)
            pass   
        except KeyboardInterrupt:
            pass

        sim_data_x= myBopt2D.X
        myBopt2D.save_evaluations(data_file_name)

    print("Value of (a, b, c) that minimises the resistance : "+str(myBopt2D.x_opt))    
    print("Optimum resistance is: " + str(myBopt2D.fx_opt))

    myBopt2D.plot_acquisition()  
    myBopt2D.plot_convergence()


    np.savetxt(data_opt_name, ([myBopt2D.fx_opt, myBopt2D.x_opt[0], myBopt2D.x_opt[1], myBopt2D.x_opt[2]]), delimiter=",")

if __name__=='__main__':
    run=[1]; seeds=[17]	
    aqu2='LCB'
    
    for i in range(len(run)):
        run_bo(run[i],aqu2,seeds[i]) 