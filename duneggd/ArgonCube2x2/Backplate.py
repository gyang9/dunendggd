""" Backplate.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class BackplateBuilder(gegede.builder.Builder):
    """ Class to build Backplate geometry.

    """

    def configure(self,Backplate_dimension,Backplate_gap,Backplate_btm_off,**kwargs):

        # Read dimensions form config file
        self.Backplate_dx           = Backplate_dimension['dx']
        self.Backplate_dy           = Backplate_dimension['dy']
        self.Backplate_dz           = Backplate_dimension['dz']

        self.Backplate_gap_dy       = Backplate_gap['dy']
        self.Backplate_gap_dz       = Backplate_gap['dz']

        self.Backplate_btm_off      = Backplate_btm_off

        # Material definitons
        self.Gap_Material   = 'LAr'

        self.Material       = 'G10'

    def construct(self,geom):
        """ Construct the geometry.

        """
        tpcplane_builder = self.get_builder('TPCPlane')

        self.N_Gap = tpcplane_builder.N_UnitsY

        self.Backplate_top_off = self.Backplate_dy-tpcplane_builder.halfDimension['dy']-self.Backplate_btm_off

        self.halfDimension  = { 'dx':   self.Backplate_dx,
                                'dy':   self.Backplate_dy,
                                'dz':   self.Backplate_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('BackplateBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct Backplate Center Volume
        backplateCenter_shape = geom.shapes.Box('BackplateCenter',
                                        dx = self.Backplate_dx,
                                        dy = tpcplane_builder.halfDimension['dy'],
                                        dz = self.Backplate_dz)

        backplateCenter_lv = geom.structure.Volume('volBackplateCenter',
                                        material=self.Material,
                                        shape=backplateCenter_shape)

        # Place Backplate Center Volume inside Backplate volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        backplateCenter_pos = geom.structure.Position('backplateCenter_pos',
                                                pos[0],pos[1],pos[2])

        backplateCenter_pla = geom.structure.Placement('backplateCenter_pla',
                                                volume=backplateCenter_lv,
                                                pos=backplateCenter_pos)

        #main_lv.placements.append(backplateCenter_pla.name)

        # Construct Backplate Gap Volume
        backplateGap_shape = geom.shapes.Box('BackplateGap',
                                        dx = self.Backplate_dx,
                                        dy = self.Backplate_gap_dy,
                                        dz = self.Backplate_gap_dz)

        backplateGap_lv = geom.structure.Volume('volBackplateGap',
                                        material=self.Gap_Material,
                                        shape=backplateGap_shape)

        # Place Backplate Gap Volume inside Backplate volume
        for i in range(2):
            for j in range(self.N_Gap):
                pos = [Q('0cm'),tpcplane_builder.halfDimension['dy']/self.N_Gap*(3-2*j)-self.Backplate_top_off+self.Backplate_btm_off,(-1)**i*(self.Backplate_dz-self.Backplate_gap_dz)]

                backplateGap_pos = geom.structure.Position('backplateGap_pos'+str(i*self.N_Gap+j),
                                                        pos[0],pos[1],pos[2])

                backplateGap_pla = geom.structure.Placement('backplateGap_pla'+str(i*self.N_Gap+j),
                                                        volume=backplateGap_lv,
                                                        pos=backplateGap_pos)

                main_lv.placements.append(backplateGap_pla.name)

