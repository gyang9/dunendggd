""" TPC.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class TPCBuilder(gegede.builder.Builder):
    """ Class to build TPC geometry.

    """

    def configure(self,Drift_Length,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                WLS_dimension: Outer dimensions of the WLS panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """
        self.Drift_Length       = Drift_Length

        # Give some clearance within fieldcage for possible precision errors
        self.Drift_Length       = self.Drift_Length-Q('0.5mm')/2

        self.Active_Material    = 'LAr'
        self.Material           = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        optdet_builder      = self.get_builder('OpticalDet')
        tpcplane_builder    = optdet_builder.get_builder('TPCPlane')

        self.halfDimension  = { 'dx':   self.Drift_Length
                                        +tpcplane_builder.halfDimension['dx'],

                                'dy':   tpcplane_builder.halfDimension['dy'],
                                'dz':   tpcplane_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('TPCBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build TPCPlane
        pos = [-self.Drift_Length,Q('0mm'),Q('0mm')]

        tpcplane_lv = tpcplane_builder.get_volume()

        tpcplane_pos = geom.structure.Position(tpcplane_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        tpcplane_pla = geom.structure.Placement(tpcplane_builder.name+'_pla',
                                                volume=tpcplane_lv,
                                                pos=tpcplane_pos)

        main_lv.placements.append(tpcplane_pla.name)

        # Construct TPCActive
        TPCActive_shape = geom.shapes.Box('TPCActive',
                                        dx =    self.Drift_Length,
                                        dy =    tpcplane_builder.halfDimension['dy'],
                                        dz =    tpcplane_builder.halfDimension['dz'])

        TPCActive_lv = geom.structure.Volume('volTPCActive',
                                        material=self.Active_Material,
                                        shape=TPCActive_shape)

        # Place TPCActive
        pos = [tpcplane_builder.halfDimension['dx'],Q('0cm'),Q('0cm')]

        TPCActive_pos = geom.structure.Position('TPCActive_pos',
                                                pos[0],pos[1],pos[2])

        TPCActive_pla = geom.structure.Placement('TPCActive_pla',
                                                volume=TPCActive_lv,
                                                pos=TPCActive_pos)

        main_lv.placements.append(TPCActive_pla.name)

