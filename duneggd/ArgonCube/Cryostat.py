""" Cryostat.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class CryostatBuilder(gegede.builder.Builder):
    """ Class to build Cryostat geometry.

    """

    def configure(self,Kapton_thickness,Bucket_thickness,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                WLS_dimension: Outer dimensions of the WLS panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """

        self.Kapton_thickness   = Kapton_thickness
        self.Bucket_thickness   = Bucket_thickness

        self.Kapton_Material    = 'Kapton'
        self.Material           = 'G10'

    def construct(self,geom):
        """ Construct the geometry.

        """

        htpc_builder = self.get_builder('HalfTPC')

        self.halfDimension  = { 'dx':   htpc_builder.halfDimension['dx']+self.Kapton_thickness+2*self.Bucket_thickness,
                                'dy':   htpc_builder.halfDimension['dy']+2*self.Kapton_thickness+2*self.Bucket_thickness,
                                'dz':   htpc_builder.halfDimension['dz']+2*self.Kapton_thickness+2*self.Bucket_thickness}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('CryostatBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct Kapton layer
        Kapton_shape = geom.shapes.Box('Kapton_panel',
                                       dx = htpc_builder.halfDimension['dx']+self.Kapton_thickness,
                                       dy = htpc_builder.halfDimension['dy']+2*self.Kapton_thickness,
                                       dz = htpc_builder.halfDimension['dz']+2*self.Kapton_thickness)

        Kapton_lv = geom.structure.Volume('volKapton',
                                            material=self.Kapton_Material,
                                            shape=Kapton_shape)

        # Place Kapton layer into main LV
        pos = [Q('0m'),Q('0m'),Q('0m')]

        Kapton_pos = geom.structure.Position('Kapton_pos',
                                                pos[0],pos[1],pos[2])

        Kapton_pla = geom.structure.Placement('Kapton_pla',
                                                volume=Kapton_lv,
                                                pos=Kapton_pos)

        main_lv.placements.append(Kapton_pla.name)

        # Build HalfTPC
        pos = [-self.Kapton_thickness,Q('0cm'),Q('0cm')]

        htpc_lv = htpc_builder.get_volume()

        htpc_pos = geom.structure.Position(htpc_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        htpc_pla = geom.structure.Placement(htpc_builder.name+'_pla',
                                                volume=htpc_lv,
                                                pos=htpc_pos)

        main_lv.placements.append(htpc_pla.name)

