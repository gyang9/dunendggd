""" ArCLight.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ArCLightBuilder(gegede.builder.Builder):
    """ Class to build ArCLight geometry.

    """

    def configure(self,WLS_dimension,SiPM_dimension,NSiPM,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                WLS_dimension: Outer dimensions of the WLS panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """

        self.WLS_dx     = WLS_dimension['dx']
        self.WLS_dy     = WLS_dimension['dy']
        self.WLS_dz     = WLS_dimension['dz']

        self.SiPM_dx    = SiPM_dimension['dx']
        self.SiPM_dy    = SiPM_dimension['dy']
        self.SiPM_dz    = SiPM_dimension['dz']

        self.ESR_d          = Q('1um')/2
        self.DC_dz          = Q('1um')/2
        self.TPB_dz         = Q('1um')/2
        self.PVT_dx         = self.SiPM_dx-self.ESR_d
        self.ArC_PCB_dx     = Q('1.5mm')/2

        self.WLS_Material       = 'EJ280WLS'
        self.ESR_Material       = 'ESR'
        self.DC_Material        = 'DC'
        self.TPB_Material       = 'TPB'
        self.PVT_Material       = 'PVT'
        self.ArC_PCB_Material   = 'FR4'
        self.SiPM_Material      = 'Silicon'

        self.NSiPM          = NSiPM

        self.Material       = 'LAr'
        self.halfDimension  = { 'dx':   self.WLS_dx
                                        +self.ESR_d
                                        +self.SiPM_dx
                                        +self.ArC_PCB_dx,

                                'dy':   self.WLS_dy
                                        +2*self.ESR_d,

                                'dz':   self.WLS_dz
                                        +self.ESR_d
                                        +self.DC_dz
                                        +self.TPB_dz}

    def construct(self,geom):
        """ Construct the geometry.

        """

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ArCLightBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct WLS panel
        WLS_shape = geom.shapes.Box('WLS_panel',
                                       dx = self.WLS_dx,
                                       dy = self.WLS_dy,
                                       dz = self.WLS_dz)

        WLS_lv = geom.structure.Volume('volWLS',
                                            material=self.WLS_Material,
                                            shape=WLS_shape)

        # Place WLS panel into main LV
        pos = [self.PVT_dx+self.ArC_PCB_dx,Q('0m'),self.ESR_d-self.DC_dz-self.TPB_dz]

        WLS_pos = geom.structure.Position('WLS_pos',
                                                pos[0],pos[1],pos[2])

        WLS_pla = geom.structure.Placement('WLS_pla',
                                                volume=WLS_lv,
                                                pos=WLS_pos)

        main_lv.placements.append(WLS_pla.name)

        # Construct ESR LV
        ESR_shape = geom.shapes.Box('ESR_film',
                                       dx = self.WLS_dx+2*self.ESR_d,
                                       dy = self.WLS_dy+2*self.ESR_d,
                                       dz = self.WLS_dz+self.ESR_d)

        ESR_lv = geom.structure.Volume('volESR',
                                            material=self.ESR_Material,
                                            shape=ESR_shape)

        # Place ESR LV into WLS panel
        pos = [Q('0m'),Q('0m'),-self.ESR_d]

        ESR_pos = geom.structure.Position('ESR_pos',
                                                pos[0],pos[1],pos[2])

        ESR_pla = geom.structure.Placement('ESR_pla',
                                                volume=ESR_lv,
                                                pos=ESR_pos)

        WLS_lv.placements.append(ESR_pla.name)

        # Construct DC LV
        DC_shape = geom.shapes.Box('DC_film',
                                       dx = self.WLS_dx+2*self.ESR_d,
                                       dy = self.WLS_dy+2*self.ESR_d,
                                       dz = self.DC_dz)

        DC_lv = geom.structure.Volume('volDC',
                                            material=self.DC_Material,
                                            shape=DC_shape)

        # Place DC LV next to WLS plane
        pos = [Q('0m'),Q('0m'),(self.WLS_dz+self.DC_dz)]

        DC_pos = geom.structure.Position('DC_pos',
                                                pos[0],pos[1],pos[2])

        DC_pla = geom.structure.Placement('DC_pla',
                                                volume=DC_lv,
                                                pos=DC_pos)

        WLS_lv.placements.append(DC_pla.name)

        # Construct TPB LV
        TPB_shape = geom.shapes.Box('TPB_layer',
                                       dx = self.WLS_dx+2*self.ESR_d,
                                       dy = self.WLS_dy+2*self.ESR_d,
                                       dz = self.TPB_dz)

        TPB_lv = geom.structure.Volume('volTPB',
                                            material=self.TPB_Material,
                                            shape=TPB_shape)

        # Place TPB LV next to WLS plane
        pos = [Q('0m'),Q('0m'),(self.DC_dz+self.TPB_dz)]

        TPB_pos = geom.structure.Position('TPB_pos',
                                                pos[0],pos[1],pos[2])

        TPB_pla = geom.structure.Placement('TPB_pla',
                                                volume=TPB_lv,
                                                pos=TPB_pos)

        DC_lv.placements.append(TPB_pla.name)

        # Construct PVT LV
        PVT_shape = geom.shapes.Box('PVT_bar',
                                       dx = self.PVT_dx,
                                       dy = self.WLS_dy,
                                       dz = self.WLS_dz)

        PVT_lv = geom.structure.Volume('volPVT',
                                            material=self.PVT_Material,
                                            shape=PVT_shape)

        # Place PVT LV next to WLS plane
        pos = [-self.WLS_dx-self.ESR_d*2-self.PVT_dx,Q('0m'),self.ESR_d]

        PVT_pos = geom.structure.Position('PVT_pos',
                                                pos[0],pos[1],pos[2])

        PVT_pla = geom.structure.Placement('PVT_pla',
                                                volume=PVT_lv,
                                                pos=PVT_pos)

        ESR_lv.placements.append(PVT_pla.name)

        # Construct ArC_PCB LV
        ArC_PCB_shape = geom.shapes.Box('ArC_PCB_bar',
                                       dx = self.ArC_PCB_dx,
                                       dy = self.WLS_dy,
                                       dz = self.WLS_dz)

        ArC_PCB_lv = geom.structure.Volume('volArCPCB',
                                            material=self.ArC_PCB_Material,
                                            shape=ArC_PCB_shape)

        # Place ArC_PCB LV next to WLS plane
        pos = [-self.PVT_dx-self.ArC_PCB_dx,Q('0m'),Q('0m')]

        ArC_PCB_pos = geom.structure.Position('ArC_PCB_pos',
                                                pos[0],pos[1],pos[2])

        ArC_PCB_pla = geom.structure.Placement('ArC_PCB_pla',
                                                volume=ArC_PCB_lv,
                                                pos=ArC_PCB_pos)

        PVT_lv.placements.append(ArC_PCB_pla.name)

        for n in range(self.NSiPM):
            # Construct SiPM LV
            SiPM_shape = geom.shapes.Box('SiPM'+str(n),
                                           dx = self.SiPM_dx,
                                           dy = self.SiPM_dy,
                                           dz = self.SiPM_dz)

            SiPM_lv = geom.structure.Volume('volSiPM'+str(n),
                                                material=self.SiPM_Material,
                                                shape=SiPM_shape)

            # Place SiPMs next to WLS plane
            pos = [-self.WLS_dx-self.SiPM_dx,-self.WLS_dy+self.WLS_dy/self.NSiPM*(1+2*n),Q('0m')]

            SiPM_pos = geom.structure.Position('SiPM_pos'+str(n),
                                                    pos[0],pos[1],pos[2])

            SiPM_pla = geom.structure.Placement('SiPM_pla'+str(n),
                                                    volume=SiPM_lv,
                                                    pos=SiPM_pos)

            WLS_lv.placements.append(SiPM_pla.name)
