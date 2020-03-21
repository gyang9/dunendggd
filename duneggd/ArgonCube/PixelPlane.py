""" PixelPlane.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class PixelPlaneBuilder(gegede.builder.Builder):
    """ Class to build PixelPlane geometry.

    """

    def configure(self,PCB_dimension,Pixel_dimension,Asic_dimension,NPixel,NAsic,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                PCB_dimension: Outer dimensions of the PCB panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """

        self.PCB_dx = PCB_dimension['dx']
        self.PCB_dy = PCB_dimension['dy']
        self.PCB_dz = PCB_dimension['dz']

        self.Pixel_dx = Pixel_dimension['dx']
        self.Pixel_dy = Pixel_dimension['dy']
        self.Pixel_dz = Pixel_dimension['dz']

        self.Asic_dx = Asic_dimension['dx']
        self.Asic_dy = Asic_dimension['dy']
        self.Asic_dz = Asic_dimension['dz']

        self.PCB_Material   = 'FR4'
        self.Pixel_Material = 'Gold'
        self.Asic_Material  = 'Silicon'

        self.NPixel         = NPixel
        self.NAsic          = NAsic

        self.Material       = 'LAr'
        self.halfDimension  = { 'dx':   self.PCB_dx
                                        +self.Pixel_dx
                                        +self.Asic_dx,

                                'dy':   self.PCB_dy,

                                'dz':   self.PCB_dz}

    def construct(self,geom):
        """ Construct the geometry.

        """

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('PixelPlaneBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct PCB panel
        PCB_shape = geom.shapes.Box('PCB_panel',
                                       dx = self.PCB_dx,
                                       dy = self.PCB_dy,
                                       dz = self.PCB_dz)

        PCB_lv = geom.structure.Volume('volTPCPCB',
                                            material=self.PCB_Material,
                                            shape=PCB_shape)

        # Place PCB panel into main LV
        pos = [-self.Pixel_dx+self.Asic_dx,Q('0m'),Q('0m')]

        PCB_pos = geom.structure.Position('PCB_pos',
                                                pos[0],pos[1],pos[2])

        PCB_pla = geom.structure.Placement('PCB_pla',
                                                volume=PCB_lv,
                                                pos=PCB_pos)

        main_lv.placements.append(PCB_pla.name)

        # Construct Pixel
        Pixel_shape = geom.shapes.Box('Pixel',
                                       dx = self.Pixel_dx,
                                       dy = self.Pixel_dy,
                                       dz = self.Pixel_dz)

        Pixel_lv = geom.structure.Volume('volTPCPixel',
                                            material=self.Pixel_Material,
                                            shape=Pixel_shape)

        for n in range(self.NPixel):
            for m in range(self.NPixel):
                # Place Pixel into PCB board
                pos = [self.PCB_dx+self.Asic_dx,-self.PCB_dy+self.PCB_dy/self.NPixel*(1+2*n),-self.PCB_dz+self.PCB_dz/self.NPixel*(1+2*m)]

                Pixel_pos = geom.structure.Position('Pixel_pos'+str(n)+'.'+str(m),
                                                        pos[0],pos[1],pos[2])

                Pixel_pla = geom.structure.Placement('Pixel_pla'+str(n)+'.'+str(m),
                                                        volume=Pixel_lv,
                                                        pos=Pixel_pos)

                main_lv.placements.append(Pixel_pla.name)

        # Construct ASIC
        Asic_shape = geom.shapes.Box('Asic',
                                       dx = self.Asic_dx,
                                       dy = self.Asic_dy,
                                       dz = self.Asic_dz)

        Asic_lv = geom.structure.Volume('volTPCAsic',
                                            material=self.Asic_Material,
                                            shape=Asic_shape)

        for n in range(self.NAsic):
            for m in range(self.NAsic):
                # Place ASICs into PCB board
                pos = [-self.PCB_dx-self.Pixel_dx,-self.PCB_dy+self.PCB_dy/self.NAsic*(1+2*n),-self.PCB_dz+self.PCB_dz/self.NAsic*(1+2*m)]

                Asic_pos = geom.structure.Position('Asic_pos'+str(n)+'.'+str(m),
                                                        pos[0],pos[1],pos[2])

                Asic_pla = geom.structure.Placement('Asic_pla'+str(n)+'.'+str(m),
                                                        volume=Asic_lv,
                                                        pos=Asic_pos)

                main_lv.placements.append(Asic_pla.name)

