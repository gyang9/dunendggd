""" OpticalDet.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class OpticalDetBuilder(gegede.builder.Builder):
    """ Class to build OpticalDet geometry.

    """

    def configure(self,Gap_LightTile,Gap_LightTile_Bucket,Gap_LightTile_PixelPlane,G10_bar_width,Gap_top,Gap_bottom,N_TilesY,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                WLS_dimension: Outer dimensions of the WLS panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """

        self.Gap_LightTile              = Gap_LightTile
        self.Gap_LightTile_PixelPlane   = Gap_LightTile_PixelPlane
        self.Gap_LightTile_Bucket       = Gap_LightTile_Bucket
        self.Bar_width                  = G10_bar_width
        self.Gap_top                    = Gap_top
        self.Gap_bottom                 = Gap_bottom
        self.N_TilesY                   = N_TilesY

        self.Bar_Material   = 'G10'
        self.Material       = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        arclight_builder    = self.get_builder('ArCLight')
        tpcplane_builder    = self.get_builder('TPCPlane')
        pixelplane_builder  = self.get_builder('PixelPlane')

        self.halfDimension  = { 'dx':   tpcplane_builder.halfDimension['dx']
                                        +arclight_builder.halfDimension['dx']
                                        +self.Gap_LightTile_PixelPlane
                                        +self.Bar_width,

                                'dy':   tpcplane_builder.halfDimension['dy']
                                        +self.Gap_top
                                        +self.Gap_bottom,

                                'dz':   arclight_builder.halfDimension['dz']
                                        +self.Gap_LightTile_Bucket}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('OpticalDetBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build ArCLight Array
        for i in range(self.N_TilesY):
            pos = [tpcplane_builder.halfDimension['dx']+self.Gap_LightTile_PixelPlane-self.Bar_width,(-self.N_TilesY+1+2*i)*(arclight_builder.halfDimension['dy']+self.Gap_LightTile),self.Gap_LightTile_Bucket]

            arclight_lv = arclight_builder.get_volume()

            arclight_pos = geom.structure.Position(arclight_builder.name+'_pos_'+str(i),
                                                pos[0],pos[1],pos[2])

            arclight_pla = geom.structure.Placement(arclight_builder.name+'_pla_'+str(i),
                                                    volume=arclight_lv,
                                                    pos=arclight_pos)

            main_lv.placements.append(arclight_pla.name)

        # Construct G10 Bar
        bar_shape = geom.shapes.Box('Bar',
                                        dx = self.Bar_width,
                                        dy = self.halfDimension['dy'],
                                        dz = arclight_builder.halfDimension['dz'])

        bar_lv = geom.structure.Volume('volTPCBar',
                                        material=self.Bar_Material,
                                        shape=bar_shape)

        # Place G10 Bar
        pos = [tpcplane_builder.halfDimension['dx']+arclight_builder.halfDimension['dx']+self.Gap_LightTile_PixelPlane,Q('0cm'),self.Gap_LightTile_Bucket]

        bar_pos = geom.structure.Position('bar_pos',
                                                pos[0],pos[1],pos[2])

        bar_pla = geom.structure.Placement('bar_pla',
                                                volume=bar_lv,
                                                pos=bar_pos)

        main_lv.placements.append(bar_pla.name)

        # Construct PCB Bar
        pcb_shape = geom.shapes.Box('PCBBar',
                                        dx = pixelplane_builder.PCB_dx,
                                        dy = pixelplane_builder.PCB_dy,
                                        dz = arclight_builder.halfDimension['dz'])

        pcb_lv = geom.structure.Volume('volPCBBar',
                                        material=pixelplane_builder.PCB_Material,
                                        shape=pcb_shape)

        # Place PCB Bars
        for i in range(tpcplane_builder.N_UnitsY):
            pos = [-arclight_builder.halfDimension['dx']-self.Gap_LightTile_PixelPlane-self.Bar_width-pixelplane_builder.Pixel_dx+pixelplane_builder.Asic_dx,(-self.N_TilesY+1+2*i)*(arclight_builder.halfDimension['dy']+self.Gap_LightTile),self.Gap_LightTile_Bucket]

            pcb_pos = geom.structure.Position('pcb_pos'+str(i),
                                                    pos[0],pos[1],pos[2])

            pcb_pla = geom.structure.Placement('pcb_pla'+str(i),
                                                    volume=pcb_lv,
                                                    pos=pcb_pos)

            main_lv.placements.append(pcb_pla.name)
