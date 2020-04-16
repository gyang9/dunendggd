""" ArCLight.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ArCLightBuilder(gegede.builder.Builder):
    """ Class to build ArCLight geometry.

    """

    def configure(self,WLS_dimension,SiPM_dimension,SiPM_Mask,SiPM_PCB,Mirror,N_SiPM,N_Mask,**kwargs):

        # Read dimensions form config file
        self.WLS_dx             = WLS_dimension['dx']
        self.WLS_dy             = WLS_dimension['dy']
        self.WLS_dz             = WLS_dimension['dz']

        self.Mirror_dd          = WLS_dimension['mirror_dd']

        self.TPB_dz             = WLS_dimension['tpb_dz']

        self.SiPM_dx            = SiPM_dimension['dx']
        self.SiPM_dy            = SiPM_dimension['dy']
        self.SiPM_dz            = SiPM_dimension['dz']
        self.SiPM_gap           = SiPM_dimension['gap']

        self.SiPM_Mask_dx       = SiPM_Mask['dx']
        self.SiPM_Mask_dy       = SiPM_Mask['dy']
        self.SiPM_Mask_dz       = SiPM_Mask['dz']
        self.SiPM_Mask_gap      = SiPM_Mask['gap']

        self.SiPM_PCB_dx        = SiPM_PCB['dx']
        self.SiPM_PCB_dy        = SiPM_PCB['dy']
        self.SiPM_PCB_dz        = SiPM_PCB['dz']
        self.SiPM_PCB_gap       = SiPM_PCB['gap']

        self.N_SiPM             = int(N_SiPM)
        self.N_Mask             = int(N_Mask)

        # Material definitons
        self.WLS_Material       = 'EJ280WLS'
        self.Mirror_Material    = 'ESR'
        self.TPB_Material       = 'TPB'
        self.SiPM_Material      = 'Silicon'
        self.SiPM_Mask_Material = 'PVT'
        self.SiPM_PCB_Material  = 'FR4'

        self.Material           = 'LAr'

        # Toggle mirror ON/OFF
        self.Mirror             = Mirror

        if not self.Mirror:
            self.WLS_dx = self.WLS_dx + 2*self.Mirror_dd
            self.WLS_dy = self.WLS_dy + 2*self.Mirror_dd
            self.WLS_dz = self.WLS_dz + self.Mirror_dd
            self.Mirror_dd = 0

        # Force the SiPMs to stick out by 10um from the Mask to ensure seamless coupling of optical photons
        self.SiPM_Couple        = self.Mirror_dd+Q('10um')
        self.SiPM_dx            = self.SiPM_Mask_dx+self.SiPM_Couple

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension      = { 'dx':   self.WLS_dx
                                            +2*self.Mirror_dd
                                            +self.SiPM_Mask_dx
                                            +self.SiPM_PCB_dx,

                                    'dy':   self.N_Mask*self.SiPM_PCB_dy
                                            +(self.N_Mask-1)*self.SiPM_PCB_gap,

                                    'dz':   self.WLS_dz
                                            +self.Mirror_dd
                                            +self.TPB_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ArCLightBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        if self.Mirror:
            # Construct Mirror LV
            Mirror_shape = geom.shapes.Box('Mirror_shape',
                                           dx = self.WLS_dx+2*self.Mirror_dd,
                                           dy = self.WLS_dy+2*self.Mirror_dd,
                                           dz = self.WLS_dz+self.Mirror_dd)

            Mirror_lv = geom.structure.Volume('volMirror',
                                                material=self.Mirror_Material,
                                                shape=Mirror_shape)

            # Place Mirror into main LV
            pos = [self.SiPM_Mask_dx+self.SiPM_PCB_dx,Q('0mm'),-self.TPB_dz]

            Mirror_pos = geom.structure.Position('Mirror_pos',
                                                    pos[0],pos[1],pos[2])

            Mirror_pla = geom.structure.Placement('Mirror_pla',
                                                    volume=Mirror_lv,
                                                    pos=Mirror_pos)

            main_lv.placements.append(Mirror_pla.name)

        # Construct WLS panel
        WLS_shape = geom.shapes.Box('WLS_panel_shape',
                                       dx = self.WLS_dx,
                                       dy = self.WLS_dy,
                                       dz = self.WLS_dz)

        WLS_lv = geom.structure.Volume('volWLS',
                                            material=self.WLS_Material,
                                            shape=WLS_shape)

        # Place WLS panel into main LV
        pos = [self.SiPM_Mask_dx+self.SiPM_PCB_dx,Q('0mm'),-self.TPB_dz+self.Mirror_dd]

        WLS_pos = geom.structure.Position('WLS_pos',
                                                pos[0],pos[1],pos[2])

        WLS_pla = geom.structure.Placement('WLS_pla',
                                                volume=WLS_lv,
                                                pos=WLS_pos)

        main_lv.placements.append(WLS_pla.name)


        # Construct TPB LV
        TPB_shape = geom.shapes.Box('TPB_LAr_shape',
                                       dx = self.WLS_dx,
                                       dy = self.WLS_dy,
                                       dz = self.TPB_dz)

        TPB_lv = geom.structure.Volume('volTPB_LAr',
                                            material=self.Material,
                                            shape=TPB_shape)

        # Place TPB LV next to WLS plane
        pos = [self.SiPM_Mask_dx+self.SiPM_PCB_dx,Q('0mm'),self.WLS_dz+self.Mirror_dd]

        TPB_pos = geom.structure.Position('TPB_pos',
                                                pos[0],pos[1],pos[2])

        TPB_pla = geom.structure.Placement('TPB_pla',
                                                volume=TPB_lv,
                                                pos=TPB_pos)

        main_lv.placements.append(TPB_pla.name)

        # Construct and place SiPMs and the corresponding Masks
        for n in range(self.N_Mask):
            # Construct Mask LV
            SiPM_Mask_shape = geom.shapes.Box('SiPM_Mask_shape_'+str(n),
                                           dx = self.SiPM_Mask_dx,
                                           dy = self.SiPM_Mask_dy,
                                           dz = self.SiPM_Mask_dz)

            SiPM_Mask_lv = geom.structure.Volume('volSiPM_Mask_'+str(n),
                                                material=self.SiPM_Mask_Material,
                                                shape=SiPM_Mask_shape)

            # Place Mask LV next to WLS plane
            pos = [-self.WLS_dx-2*self.Mirror_dd+self.SiPM_PCB_dx,-(self.N_Mask-1)*self.SiPM_Mask_dy-(self.N_Mask-1)*self.SiPM_Mask_gap+(2*n)*self.SiPM_Mask_dy+(2*n)*self.SiPM_Mask_gap,-self.TPB_dz+self.Mirror_dd]

            SiPM_Mask_pos = geom.structure.Position('SiPM_Mask_pos_'+str(n),
                                                    pos[0],pos[1],pos[2])

            SiPM_Mask_pla = geom.structure.Placement('SiPM_Mask_pla_'+str(n),
                                                    volume=SiPM_Mask_lv,
                                                    pos=SiPM_Mask_pos)

            main_lv.placements.append(SiPM_Mask_pla.name)

            for m in range(int(self.N_SiPM/self.N_Mask)):
                # Construct SiPM LV
                SiPM_shape = geom.shapes.Box('SiPM_shape_'+str(2*n+m),
                                               dx = self.SiPM_dx,
                                               dy = self.SiPM_dy,
                                               dz = self.SiPM_dz)

                SiPM_lv = geom.structure.Volume('volSiPM_'+str(2*n+m),
                                                    material=self.SiPM_Material,
                                                    shape=SiPM_shape)

                # Place SiPMs next to WLS plane
                posipm = [-self.WLS_dx-2*self.Mirror_dd+self.SiPM_PCB_dx+self.SiPM_Couple,pos[1]-(self.N_SiPM/self.N_Mask-1)*self.SiPM_dy-(self.N_SiPM/self.N_Mask-1)*self.SiPM_gap+(2*m)*self.SiPM_dy+(2*m)*self.SiPM_gap,-self.TPB_dz+self.Mirror_dd]

                SiPM_pos = geom.structure.Position('SiPM_pos_'+str(2*n+m),
                                                        posipm[0],posipm[1],posipm[2])

                SiPM_pla = geom.structure.Placement('SiPM_pla_'+str(2*n+m),
                                                        volume=SiPM_lv,
                                                        pos=SiPM_pos)

                main_lv.placements.append(SiPM_pla.name)

        # Construct and place SiPM PCBs
        for n in range(self.N_Mask):
            # Construct PCB LV
            SiPM_PCB_shape = geom.shapes.Box('SiPM_PCB_shape_'+str(n),
                                           dx = self.SiPM_PCB_dx,
                                           dy = self.SiPM_PCB_dy,
                                           dz = self.SiPM_PCB_dz)

            SiPM_PCB_lv = geom.structure.Volume('volSiPM_PCB_'+str(n),
                                                material=self.SiPM_PCB_Material,
                                                shape=SiPM_PCB_shape)

            # Place SiPM PCBs next to SiPM Masks
            pos = [-self.WLS_dx-2*self.Mirror_dd-self.SiPM_Mask_dx,-(self.N_Mask-1)*self.SiPM_PCB_dy-(self.N_Mask-1)*self.SiPM_PCB_gap+(2*n)*self.SiPM_PCB_dy+(2*n)*self.SiPM_PCB_gap,-self.TPB_dz+self.Mirror_dd]

            SiPM_PCB_pos = geom.structure.Position('SiPM_PCB_pos_'+str(n),
                                                    pos[0],pos[1],pos[2])

            SiPM_PCB_pla = geom.structure.Placement('SiPM_PCB_pla_'+str(n),
                                                    volume=SiPM_PCB_lv,
                                                    pos=SiPM_PCB_pos)

            main_lv.placements.append(SiPM_PCB_pla.name)
