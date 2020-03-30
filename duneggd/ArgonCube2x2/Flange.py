""" Flange.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class FlangeBuilder(gegede.builder.Builder):
    """ Class to build Flange geometry.

    """

    def configure(self,FlangeTop_dimension,FlangeMask_dimension,**kwargs):

        # Read dimensions form config file
        self.FlangeTop_dx       = FlangeTop_dimension['dx']
        self.FlangeTop_dy       = FlangeTop_dimension['dy']
        self.FlangeTop_dz       = FlangeTop_dimension['dz']

        self.FlangeMask_dx      = FlangeMask_dimension['dx']
        self.FlangeMask_dy      = FlangeMask_dimension['dy']
        self.FlangeMask_dz      = FlangeMask_dimension['dz']

        # Material definitons
        self.Flange_Material    = 'Steel'

        self.Material           = 'GAr'

        # Subbuilders
        self.Backplate_builder  = self.get_builder('Backplate')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.FlangeTop_dx,
                                'dy':   self.FlangeTop_dy+self.FlangeMask_dy,
                                'dz':   self.FlangeTop_dz}

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
        pos = [Q('0cm'),self.FlangeMask_dy,Q('0cm')]

        FlangeTop_pos = geom.structure.Position('FlangeTop_pos',
                                                pos[0],pos[1],pos[2])

        FlangeTop_pla = geom.structure.Placement('FlangeTop_pla',
                                                volume=FlangeTop_lv,
                                                pos=FlangeTop_pos)

        main_lv.placements.append(FlangeTop_pla.name)

        # Construct FlangeMask Volume
        FlangeMask_shape = geom.shapes.Box('FlangeMask_shape',
                                        dx = self.FlangeMask_dx,
                                        dy = self.FlangeMask_dy,
                                        dz = self.FlangeMask_dz)

        FlangeMask_lv = geom.structure.Volume('volFlangeMask',
                                        material=self.Flange_Material,
                                        shape=FlangeMask_shape)

        # Place FlangeMask Volume inside Flange volume
        pos = [Q('0cm'),-self.FlangeTop_dy,Q('0cm')]

        FlangeMask_pos = geom.structure.Position('FlangeMask_pos',
                                                pos[0],pos[1],pos[2])

        FlangeMask_pla = geom.structure.Placement('FlangeMask_pla',
                                                volume=FlangeMask_lv,
                                                pos=FlangeMask_pos)

        main_lv.placements.append(FlangeMask_pla.name)

