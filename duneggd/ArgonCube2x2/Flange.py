""" Flange.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class FlangeBuilder(gegede.builder.Builder):
    """ Class to build Flange geometry.

    """

    def configure(self,Flange_dimension,FlangeBtm_dimension,**kwargs):

        # Read dimensions form config file
        self.Flange_dx          = Flange_dimension['dx']
        self.Flange_dy          = Flange_dimension['dy']
        self.Flange_dz          = Flange_dimension['dz']

        self.FlangeBtm_dx       = FlangeBtm_dimension['dx']
        self.FlangeBtm_dy       = FlangeBtm_dimension['dy']
        self.FlangeBtm_dz       = FlangeBtm_dimension['dz']

        self.FlangeTop_dx       = self.Flange_dx
        self.FlangeTop_dy       = self.Flange_dy-self.FlangeBtm_dy
        self.FlangeTop_dz       = self.Flange_dz

        # Material definitons
        self.Flange_Material    = 'Steel'

        self.Material           = 'GAr'

        # Subbuilders
        self.Backplate_builder  = self.get_builder('Backplate')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Flange_dx,
                                'dy':   self.Flange_dy,
                                'dz':   self.Flange_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('FlangeBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct FlangeTop Volume
        FlangeTop_shape = geom.shapes.Box('FlangeTop_shape',
                                        dx = self.FlangeTop_dx,
                                        dy = self.FlangeTop_dy,
                                        dz = self.FlangeTop_dz)

        FlangeTop_lv = geom.structure.Volume('volFlangeTop',
                                        material=self.Flange_Material,
                                        shape=FlangeTop_shape)

        # Place FlangeTop Volume inside Flange volume
        pos = [Q('0cm'),-self.Flange_dy+2*self.FlangeBtm_dy+self.FlangeTop_dy,Q('0cm')]

        FlangeTop_pos = geom.structure.Position('FlangeTop_pos',
                                                pos[0],pos[1],pos[2])

        FlangeTop_pla = geom.structure.Placement('FlangeTop_pla',
                                                volume=FlangeTop_lv,
                                                pos=FlangeTop_pos)

        main_lv.placements.append(FlangeTop_pla.name)

        # Construct FlangeBtm Volume
        FlangeBtm_shape = geom.shapes.Box('FlangeBtm_shape',
                                        dx = self.FlangeBtm_dx,
                                        dy = self.FlangeBtm_dy,
                                        dz = self.FlangeBtm_dz)

        FlangeBtm_lv = geom.structure.Volume('volFlangeBtm',
                                        material=self.Flange_Material,
                                        shape=FlangeBtm_shape)

        # Place FlangeBtm Volume inside Flange volume
        pos = [Q('0cm'),-self.Flange_dy+self.FlangeBtm_dy,Q('0cm')]

        FlangeBtm_pos = geom.structure.Position('FlangeBtm_pos',
                                                pos[0],pos[1],pos[2])

        FlangeBtm_pla = geom.structure.Placement('FlangeBtm_pla',
                                                volume=FlangeBtm_lv,
                                                pos=FlangeBtm_pos)

        main_lv.placements.append(FlangeBtm_pla.name)

