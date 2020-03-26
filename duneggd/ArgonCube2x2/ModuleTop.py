""" ModuleTop.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ModuleTopBuilder(gegede.builder.Builder):
    """ Class to build ModuleTop geometry.

    """

    def configure(self,ModuleTop_dimension,Flange_dimension,PillowTop_dimension,PillowSide_dimension,PillowBottom_dy,AngleBar_dimension,Angle_length,Angle_dd,**kwargs):

        # Read dimensions form config file
        self.ModuleTop_dx       = ModuleTop_dimension['dx']
        self.ModuleTop_dy       = ModuleTop_dimension['dy']
        self.ModuleTop_dz       = ModuleTop_dimension['dz']

        self.Flange_dx          = Flange_dimension['dx']
        self.Flange_dy          = Flange_dimension['dy']
        self.Flange_dz          = Flange_dimension['dz']

        self.PillowTop_dx       = PillowTop_dimension['dx']
        self.PillowTop_dy       = PillowTop_dimension['dy']
        self.PillowTop_dz       = PillowTop_dimension['dz']

        self.PillowSide_dx      = PillowSide_dimension['dx']
        self.PillowSide_dy      = PillowSide_dimension['dy']
        self.PillowSide_dz      = PillowSide_dimension['dz']
        self.PillowSide_dd      = PillowSide_dimension['dd']

        self.PillowBottom_dy    = PillowBottom_dy

        self.AngleBar_dx        = AngleBar_dimension['dx']
        self.AngleBar_dy        = AngleBar_dimension['dy']
        self.AngleBar_dz        = AngleBar_dimension['dz']
        self.AngleBar_gap       = AngleBar_dimension['gap']

        # Material definitons
        self.ModuleTop_Material = 'Steel'

        self.Material           = 'GAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        #innerDetector_builder   = self.get_builder('InnerDetector')

        self.halfDimension  = { 'dx':   self.ModuleTop_dx,
                                'dy':   self.ModuleTop_dy,
                                'dz':   self.ModuleTop_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleTopBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct Flange Volume
        flange_shape = geom.shapes.Box('Flange',
                                        dx = self.ModuleTop_dx,
                                        dy = self.ModuleTop_dy,
                                        dz = self.ModuleTop_dz)

        flange_lv = geom.structure.Volume('volFlange',
                                        material=self.ModuleTop_Material,
                                        shape=flange_shape)

        # Place Flange Volume inside Bucket volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        flange_pos = geom.structure.Position('flange_pos',
                                                pos[0],pos[1],pos[2])

        flange_pla = geom.structure.Placement('flange_pla',
                                                volume=flange_lv,
                                                pos=flange_pos)

        main_lv.placements.append(flange_pla.name)

