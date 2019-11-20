""" LArActive.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class LArActiveBuilder(gegede.builder.Builder):
    """ Class to build LArActive geometry.

    """

    def configure(self,Gap_ArCL_Pixel,Gap_Pixel_Pixel,Bar_width,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                WLS_dimension: Outer dimensions of the WLS panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """

        self.Gap_ArCL_Pixel     = Gap_ArCL_Pixel
        self.Gap_Pixel_Pixel    = Gap_Pixel_Pixel/2
        self.Bar_width          = Bar_width

        self.Bar_Material   = 'G10'
        self.Material       = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        arcl_builder = self.get_builder('ArCLight')
        pixel_builder = self.get_builder('PixelBoard')

        self.halfDimension  = { 'dx':   pixel_builder.halfDimension['dx']
                                        +arcl_builder.halfDimension['dx']
                                        +self.Gap_ArCL_Pixel
                                        +self.Bar_width,

                                'dy':   arcl_builder.halfDimension['dy']
                                        +2*self.Gap_Pixel_Pixel,

                                'dz':   pixel_builder.halfDimension['dz']
                                        +self.Gap_Pixel_Pixel}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('LArActiveBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build ArCLight
        pos = [pixel_builder.halfDimension['dx']+self.Gap_ArCL_Pixel-self.Bar_width,Q('0mm'),-pixel_builder.halfDimension['dz']+pixel_builder.PCB_border_dz-self.Gap_Pixel_Pixel]

        arcl_lv = arcl_builder.get_volume()

        arcl_pos = geom.structure.Position(arcl_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        arcl_pla = geom.structure.Placement(arcl_builder.name+"_pla",
                                                volume=arcl_lv,
                                                pos=arcl_pos)

        main_lv.placements.append(arcl_pla.name)

        # Build PixelBoard
        pos = [-arcl_builder.halfDimension['dx']-self.Gap_ArCL_Pixel-self.Bar_width,Q('0mm'),-self.Gap_Pixel_Pixel]


        pixel_lv = pixel_builder.get_volume()

        pixel_pos = geom.structure.Position(pixel_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        pixel_pla = geom.structure.Placement(pixel_builder.name+"_pla",
                                                volume=pixel_lv,
                                                pos=pixel_pos)

        main_lv.placements.append(pixel_pla.name)

        # Construct G10 Bar
        bar_shape = geom.shapes.Box('Bar',
                                        dx = self.Bar_width,
                                        dy = self.halfDimension['dy'],
                                        dz = arcl_builder.halfDimension['dz'])

        bar_lv = geom.structure.Volume('Bar_vol',
                                        material=self.Bar_Material,
                                        shape=bar_shape)

        # Place G10 Bar
        pos = [arcl_builder.halfDimension['dx']+self.Bar_width,Q('0cm'),Q('0cm')]

        bar_pos = geom.structure.Position('bar_pos',
                                                pos[0],pos[1],pos[2])

        bar_pla = geom.structure.Placement('bar_pla',
                                                volume=bar_lv,
                                                pos=bar_pos)

        arcl_lv.placements.append(bar_pla.name)

