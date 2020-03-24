""" BucketAss.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class BucketAssBuilder(gegede.builder.Builder):
    """ Class to build BucketAss geometry.

    """

    def configure(self,Bucket_dimension,Backplate_dimension,LAr_level,Offset_fullDimension,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                WLS_dimension: Outer dimensions of the WLS panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """

        self.Bucket_dx          = Bucket_dimension['dx']
        self.Bucket_dy          = Bucket_dimension['dy']
        self.Bucket_dz          = Bucket_dimension['dz']
        self.Bucket_dd          = Bucket_dimension['dd']

        self.Backplate_dx       = Backplate_dimension['dx']
        self.Backplate_dy       = Backplate_dimension['dy']
        self.Backplate_dz       = Backplate_dimension['dz']

        self.Offset_det         = Offset_fullDimension['det']

        self.LAr_dy             = LAr_level
        self.GAr_dy             = self.Bucket_dy-self.LAr_dy

        self.Bucket_Material    = 'G10'
        self.Backplate_Material = 'G10'
        self.LArPhase_Material  = 'LAr'
        self.GArPhase_Material  = 'GAr'

        self.Material           = 'G10'

    def construct(self,geom):
        """ Construct the geometry.

        """

        innerDetector_builder   = self.get_builder('InnerDetector')

        self.halfDimension  = { 'dx':   self.Bucket_dx,
                                'dy':   self.Bucket_dy,
                                'dz':   self.Bucket_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('BucketAssBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct LAr Phase Volume
        larPhase_shape = geom.shapes.Box('LArPhase',
                                        dx = self.Bucket_dx-self.Bucket_dd*2,
                                        dy = self.LAr_dy,
                                        dz = self.Bucket_dz-self.Bucket_dd*2)

        larPhase_lv = geom.structure.Volume('volLArPhase',
                                        material=self.LArPhase_Material,
                                        shape=larPhase_shape)

        # Place LAr Phase Volume inside Bucket volume
        pos = [Q('0cm'),-self.GAr_dy,Q('0cm')]

        larPhase_pos = geom.structure.Position('larPhase_pos',
                                                pos[0],pos[1],pos[2])

        larPhase_pla = geom.structure.Placement('larPhase_pla',
                                                volume=larPhase_lv,
                                                pos=larPhase_pos)

        main_lv.placements.append(larPhase_pla.name)

        # Construct GAr Phase Volume
        garPhase_shape = geom.shapes.Box('GArPhase',
                                        dx = self.Bucket_dx-self.Bucket_dd*2,
                                        dy = self.GAr_dy,
                                        dz = self.Bucket_dz-self.Bucket_dd*2)

        garPhase_lv = geom.structure.Volume('volGArPhase',
                                        material=self.GArPhase_Material,
                                        shape=garPhase_shape)

        # Place GAr Phase Volume inside Bucket volume
        pos = [Q('0cm'),self.LAr_dy,Q('0cm')]

        garPhase_pos = geom.structure.Position('garPhase_pos',
                                                pos[0],pos[1],pos[2])

        garPhase_pla = geom.structure.Placement('garPhase_pla',
                                                volume=garPhase_lv,
                                                pos=garPhase_pos)

        main_lv.placements.append(garPhase_pla.name)

        # Build InnerDetector
        pos = [Q('0cm'),-self.Bucket_dy+innerDetector_builder.halfDimension['dy']+self.Offset_det,Q('0cm')]

        innerDetector_lv = innerDetector_builder.get_volume()

        innerDetector_pos = geom.structure.Position(innerDetector_builder.name+'_pos_L',
                                                pos[0],pos[1],pos[2])

        innerDetector_pla = geom.structure.Placement(innerDetector_builder.name+'_pla_L',
                                                volume=innerDetector_lv,
                                                pos=innerDetector_pos)

        main_lv.placements.append(innerDetector_pla.name)

