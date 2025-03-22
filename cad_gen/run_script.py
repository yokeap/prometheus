import numpy as np
from .vessel_class import Vessel
import math 
import matplotlib.pyplot as plt
def main_cad():
    remus_volume=193537.425  # in cubic cm 

    #optimal_nt=np.array([29.79,67.30,81.90,95,89.52,66.74,38.26,24.93])
    dp= np.loadtxt('./design_points.csv', delimiter=',')
    #print('design_points are:',dp,'shape:',dp.shape)

    #Importing vessel seed design
    vessel = Vessel('vessel_t.FCStd') 
    #dp= np.append(np.array([b,D]),ds[i])
    #print('******design point is:******',dp,'dp shape  is:',dp.shape)

    ######Setting vehicle details###

    #d= dp[1]


    line_a= dp[0]
    line_b= dp[1]
    line_c= dp[2]


    # a_ext=dp[4]
    # b_ext=dp[5]
    # c_ext=dp[6]

    # a=head_a+a_ext # type: ignore
    # b=head_b+b_ext
    # c=head_c+c_ext



    vessel.set_low_len(line_a)
    vessel.set_high_len(line_b)
    vessel.set_medium_len(line_c)

    ##########
    hull_line_h=vessel.get_high_details()
    print('----> hull line high:',hull_line_h)

    hull_line_m=vessel.get_medium_details()
    print('----> hull line medium:',hull_line_m)

    hull_line_l=vessel.get_low_details()
    print('----> hull line low:',hull_line_l)



    ###Get volume and apped to design point
    # volume=vessel.get_outer_volume()
    # hull= np.array(a,b,c)
    # dp=np.append(hull,volume)
    # print('******design point is:******',dp,'dp shape  is:',dp.shape)

    # np.savetxt('design_points.csv',dp,delimiter=',')
    #########
    # def estimate_low(a,d,x,n): 
    #     return 0.5*d*np.power((1-np.power(((x-a)/a),2)),(1/n))





    vessel.create_stl(1)

# main_cad()
