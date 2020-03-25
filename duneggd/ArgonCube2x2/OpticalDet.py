""" OpticalDet.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class OpticalDetBuilder(gegede.builder.Builder):
    """ Class to build OpticalDet geometry.

    """

    def configure(self,Gap_LightTile,Gap_LightTile_PixelPlane,N_TilesY,**kwargs):

        # Read dimensions form config file
        self.Gap_LightTile              = Gap_LightTile
        self.Gap_LightTile_PixelPlane   = Gap_LightTile_PixelPlane
        self.N_TilesY                   = N_TilesY

        # Material definitons
        self.Material       = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        arclight_builder    = self.get_builder('ArCLight')
        tpcplane_builder    = self.get_builder('TPCPlane')
        pixelplane_builder  = tpcplane_builder.get_builder('PixelPlane')

        self.halfDimension  = { 'dx':   tpcplane_builder.halfDimension['dx']
                                        +arclight_builder.halfDimension['dx']
                                        +self.Gap_LightTile_PixelPlane,

                                'dy':   tpcplane_builder.halfDimension['dy'],
                                'dz':   arclight_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('OpticalDetBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build ArCLight Array
        for i in range(self.N_TilesY):
            pos = [tpcplane_builder.halfDimension['dx']+self.Gap_LightTile_PixelPlane,(-self.N_TilesY+1+2*i)*(arclight_builder.halfDimension['dy']+self.Gap_LightTile),Q('0cm')]

            arclight_lv = arclight_builder.get_volume()

            arclight_pos = geom.structure.Position(arclight_builder.name+'_pos_'+str(i),
                                                pos[0],pos[1],pos[2])

            arclight_pla = geom.structure.Placement(arclight_builder.name+'_pla_'+str(i),
                                                    volume=arclight_lv,
                                                    pos=arclight_pos)

            main_lv.placements.append(arclight_pla.name)

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
            pos = [-arclight_builder.halfDimension['dx']-self.Gap_LightTile_PixelPlane-pixelplane_builder.Pixel_dx+pixelplane_builder.Asic_dx,(-self.N_TilesY+1+2*i)*(arclight_builder.halfDimension['dy']+self.Gap_LightTile),Q('0cm')]

            pcb_pos = geom.structure.Position('pcb_pos'+str(i),
                                                    pos[0],pos[1],pos[2])

            pcb_pla = geom.structure.Placement('pcb_pla'+str(i),
                                                    volume=pcb_lv,
                                                    pos=pcb_pos)

            main_lv.placements.append(pcb_pla.name)
