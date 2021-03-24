""" ModuleArray.py

Original Author: A. Mastbaum, Rutgers

A bank of ND modules (NDBuckets)
"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class ModuleArrayBuilder(gegede.builder.Builder):
    """ Class to build Module Array geometry."""

    def configure(self, N_ModuleX, N_ModuleZ, TopLArHeight, **kwargs):
        self.Material   = 'LAr'

        # Read dimensions form config file
        self.N_ModuleX  = N_ModuleX
        self.N_ModuleZ  = N_ModuleZ
        #self.TopHeight = TopHeight
        self.TopLArHeight = TopLArHeight

        # Subbuilders
        self.NDBucket_builder = self.get_builder('NDBucket')
        #self.Tub_builder = self.get_builder('Tub')
        self.Grating_builder = self.get_builder('Grating')

    def construct(self,geom):
        """ Construct the geometry."""

        #arraydz = self.NDBucket_builder.halfDimension['dz'] * self.N_ModuleZ
        arraydz = self.Grating_builder.halfDimension['dy']
        GratingHeight = 0 #self.Grating_builder.halfDimension['dx'] / 2
        self.halfDimension  = { 'dx':   self.NDBucket_builder.halfDimension['dx']*self.N_ModuleX,
                                'dy':   self.NDBucket_builder.halfDimension['dy'] + self.TopLArHeight + GratingHeight, # + self.TopHeight,
                                'dz':   arraydz} #self.Tub_builder.halfDimension['dy']}

        print(self.halfDimension)
        print(self.Grating_builder.halfDimension)

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleArrayBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        ## Service area, a volume of GAr above the modules
        #Service_shape = geom.shapes.Box('Service_shape',
        #                                dx=self.NDBucket_builder.halfDimension['dx'],
        #                                dy=self.TopHeight,
        #                                dz=self.Tub_builder.halfDimension['dy'])

        #Service_lv = geom.structure.Volume('Service_lv',
        #                                   material='GAr',
        #                                   shape=Service_shape)

        #Tub_lv = self.Tub_builder.get_volume()

        # Build Array
        for i in range(self.N_ModuleX):
            # Place an array of modules
            for j in range(self.N_ModuleZ):
                pos = [
                    -self.halfDimension['dx']+(2*i+1)*self.NDBucket_builder.halfDimension['dx'],
                    -self.halfDimension['dy']+self.NDBucket_builder.halfDimension['dy'],
                    -arraydz+(2*j+1)*self.NDBucket_builder.halfDimension['dz']
                ]

                Module_lv = self.NDBucket_builder.get_volume()

                Module_pos = geom.structure.Position(self.NDBucket_builder.name+'_pos_'+str(i)+'.'+str(j),
                                                        pos[0],pos[1],pos[2])

                Module_pla = geom.structure.Placement(self.NDBucket_builder.name+'_pla_'+str(i)+'.'+str(j),
                                                        volume=Module_lv,
                                                        pos=Module_pos,
                                                        copynumber=2*j+i)

                main_lv.placements.append(Module_pla.name)

            # Add grating
            Grating_lv = self.Grating_builder.get_volume()
            pos = [
                -self.halfDimension['dx']+(2*i+1)*self.NDBucket_builder.halfDimension['dx'],
                -self.halfDimension['dy']+2*self.NDBucket_builder.halfDimension['dy']+self.Grating_builder.halfDimension['dx'],
                Q('0mm')
            ]
            Grating_pos = geom.structure.Position('Grating_pos_'+str(i),pos[0],pos[1],pos[2])
            Grating_rot = geom.structure.Rotation('Grating_rot_'+str(i),x='0deg',y='-90deg',z='-90deg')
            Grating_pla = geom.structure.Placement('Grating_pla_'+str(i),volume=Grating_lv,pos=Grating_pos,rot=Grating_rot,copynumber=i)
            main_lv.placements.append(Grating_pla.name)

            ## Place service placeholder
            #pos = [
            #    -self.halfDimension['dx']+(2*i+1)*self.NDBucket_builder.halfDimension['dx'],
            #    self.halfDimension['dy']-self.TopHeight,#+2*self.NDBucket_builder.halfDimension['dy']+self.TopHeight,
            #    Q('0cm')#(arraydz-self.Tub_builder.halfDimension['dy'])
            #]

            #Service_pos = geom.structure.Position('Service_pos_'+str(i),
            #                                        pos[0],pos[1],pos[2])

            #Service_pla = geom.structure.Placement('Service_pla_'+str(i),
            #                                        volume=Service_lv,
            #                                        pos=Service_pos,
            #                                        copynumber=i)

            #main_lv.placements.append(Service_pla.name)

            ## Place tub in GAr
            #pos = [Q('0mm'), self.TopHeight-self.Tub_builder.halfDimension['dx'], Q('0mm')]
            #Tub_pos = geom.structure.Position('Tub_pos_'+str(i),pos[0],pos[1],pos[2])
            #Tub_rot = geom.structure.Rotation('Tub_rot_'+str(i),x='0deg',y='90deg',z='-90deg')
            #Tub_pla = geom.structure.Placement('Tub_pla_'+str(i),volume=Tub_lv,pos=Tub_pos,rot=Tub_rot,copynumber=i)
            #Service_lv.placements.append(Tub_pla.name)

