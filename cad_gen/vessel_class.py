import os
import sys
import numpy as np
freecad_libs = [
        '/usr/local/lib/FreeCAD.so',
        '/usr/lib/freecad-python3/lib/FreeCAD.so',
        '/usr/lib/freecad-python3/lib/',
]
# freecad_libs ='/usr/lib/freecad-python3/lib/'

for lib in freecad_libs:
 if os.path.exists(lib):
         path = os.path.dirname(lib)
         if path not in sys.path:
             sys.path.append(path)
         break

else:
 raise ValueError("FreeCAD library was not found!")

import FreeCAD                              # noqa
from FreeCAD import Units                   # noqa

femtools_libs = [
        '/usr/local/Mod/Fem/femtools',
        '/usr/share/freecad/Mod/Fem/femtools',
]
for lib in femtools_libs:
        if os.path.exists(lib):
            path = os.path.dirname(lib)
            if path not in sys.path:
                sys.path.append(path)
            path = os.path.abspath(os.path.join(lib, '..', '..'))
            if path not in sys.path:
                sys.path.append(path)
            path = os.path.abspath(os.path.join(lib, '..', '..', '..', 'Ext'))
            if path not in sys.path:
                sys.path.append(path)
            break
else:
        raise ValueError("femtools library was not found!")

from femtools.ccxtools import FemToolsCcx   # noqa
from femmesh.gmshtools import GmshTools     # noqa
import Mesh


class Vessel(object):
        """
        The base class to work with parametric pressure vessel models.
        """
        def __init__(self, filename: str, debug=True):
            """
            Creates a pressure vessel analysis class that can be used to run
            multiple simulations for the given design template by changing its
            parameters.
            """
            self.filename = filename
            self.debug = debug

            print("Opening:", filename)
            self.doc = FreeCAD.open(filename)
            self.exp_index= None 
       
       
            self.sketch_params = []
            obj = self.doc.getObject('Sketch007')
        
        
     
            """
            print('***Parametric properties are:***')
            print('Sketch is:')
            for c in obj.Constraints:
                if c.Name:
                    self.sketch_params.append(str(c.Name))
                    print(str(c.Name))
            """
        
        
        
    
        
        def set_medium_len(self, line_b):
            try: 
                obj = self.doc.getObject('Sketch007') 
                obj.setDatum('myhull_b', Units.Quantity(line_b , Units.Unit('mm')))
                self.doc.recompute()
            except: 
             print('failed in setting line_b length')        
        
        def set_low_len(self, line_a):
            try: 
                obj = self.doc.getObject('Sketch007') 
                obj.setDatum('myhull_a', Units.Quantity(line_a , Units.Unit('mm')))
                self.doc.recompute()
            # except: 
            #  print('failed in setting line_a length')
            except Exception as e:
                print(e)    
    
        def set_high_len(self, line_c):
            try: 
                obj = self.doc.getObject('Sketch007') 
                obj.setDatum('myhull_c', Units.Quantity(line_c , Units.Unit('mm')))
                self.doc.recompute()
            except: 
             print('failed in setting line_c length')
  
     
    
        def get_high_details(self):
         obj_spz = self.doc.getObject('Sketch007')  
         my_c=obj_spz.getDatum('myhull_c').getValueAs('mm')
         return(my_c)
    
        def get_medium_details(self):
         obj_spz = self.doc.getObject('Sketch007')  
         my_b=obj_spz.getDatum('myhull_b').getValueAs('mm')
         return(my_b)
    
        def get_low_details(self):
         obj_spz = self.doc.getObject('Sketch007')  
         my_a=obj_spz.getDatum('myhull_a').getValueAs('mm')
         return(my_a)




      
    
        def recompute(self):
            """
            Recompute the design after setting all parametric values of design
            """
            self.clean()
            self.doc.recompute()
        
    
        def create_stl(self,exp_index):   
            """
            Generate stl file from the current design
            """
            # try:
            self.recompute()
            __objs__= self.doc.getObject("Body")
            # self.recompute()
            # p = self.doc.activeDocument().Compound001
            # myLinks=p.Links
            # p.Links=myLinks
            # self.doc.activeDocument().recompute() 
            print(__objs__.Name, self.doc.Name)
            # stl_name= u"./stl_repo/ship"+str(exp_index)+".stl"
            stl_name= u"./stl_repo/ship_gen.stl"
            Mesh.export([__objs__], stl_name)
            del __objs__    
            # except Exception as e:
                # print(e)
     #     # print("An error occurred while creating stl file") 
        def get_exp_index(self) -> int:
            """
            Returns the experiment index of current design.
            """
            print('self index is:',self.exp_index)
            return self.exp_index
   
        def set_exp_index(self,exp_ind) -> int:
            """
            set the experiment index of current design
            """
            self.exp_index=exp_ind


 

        def clean(self):
            """
            Removes all temporary artifacts from the model.
            """
            if self.doc.getObject('CCX_Results'):
                self.doc.removeObject('CCX_Results')
            if self.doc.getObject('ResultMesh'):
                self.doc.removeObject('ResultMesh')
            if self.doc.getObject('ccx_dat_file'):
                self.doc.removeObject('ccx_dat_file')




if __name__ == '__main__':
        run()
