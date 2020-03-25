""" ArCLight.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ArCLightBuilder(gegede.builder.Builder):
    """ Class to build ArCLight geometry.

    """

    def configure(self,WLS_dimension,SiPM_dimension,SiPM_mask,SiPM_pcb,Mirror,NSiPM,NMask,**kwargs):

        # Read dimensions form config file
        self.WLS_dx             = WLS_dimension['dx']
        self.WLS_dy             = WLS_dimension['dy']
        self.WLS_dz             = WLS_dimension['dz']

        self.Mirror_d           = WLS_dimension['mirror_d']

        self.TPB_dz             = WLS_dimension['tpb_dz']

        self.SiPM_dx            = SiPM_dimension['dx']
        self.SiPM_dy            = SiPM_dimension['dy']
        self.SiPM_dz            = SiPM_dimension['dz']
        self.SiPM_gap           = SiPM_dimension['gap']

        self.SiPM_mask_dx       = SiPM_mask['dx']
        self.SiPM_mask_dy       = SiPM_mask['dy']
        self.SiPM_mask_dz       = SiPM_mask['dz']
        self.SiPM_mask_gap      = SiPM_mask['gap']

        self.SiPM_pcb_dx        = SiPM_pcb['dx']
        self.SiPM_pcb_dy        = SiPM_pcb['dy']
        self.SiPM_pcb_dz        = SiPM_pcb['dz']
        self.SiPM_pcb_gap       = SiPM_pcb['gap']

        self.NSiPM              = NSiPM
        self.NMask              = NMask

        # Material definitons
        self.WLS_Material       = 'EJ280WLS'
        self.Mirror_Material    = 'ESR'
        self.TPB_Material       = 'TPB'
        self.SiPM_Material      = 'Silicon'
        self.SiPM_mask_Material = 'PVT'
        self.SiPM_pcb_Material  = 'FR4'

        self.Material           = 'LAr'

        # Toggle mirror ON/OFF
        self.Mirror             = Mirror

        if not self.Mirror:
            self.WLS_dx = self.WLS_dx + 2*self.Mirror_d
            self.WLS_dy = self.WLS_dy + 2*self.Mirror_d
            self.WLS_dz = self.WLS_dz + self.Mirror_d
            self.Mirror_d = 0

        # Force the SiPMs to stick out by 10um from the maske to ensure seamless coupling of optical photons
        self.SiPM_couple        = self.Mirror_d+Q('10um')
        self.SiPM_dx            = self.SiPM_mask_dx+self.SiPM_couple

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension      = { 'dx':   self.WLS_dx
                                            +2*self.Mirror_d
                                            +self.SiPM_mask_dx
                                            +self.SiPM_pcb_dx,

                                    'dy':   self.NMask*self.SiPM_pcb_dy
                                            +(self.NMask-1)*self.SiPM_pcb_gap,

                                    'dz':   self.WLS_dz
                                            +self.Mirror_d
                                            +self.TPB_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ArCLightBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        if self.Mirror:
            # Construct Mirror LV
            Mirror_shape = geom.shapes.Box('Mirror_LAr_layer',
                                           dx = self.WLS_dx+2*self.Mirror_d,
                                           dy = self.WLS_dy+2*self.Mirror_d,
                                           dz = self.WLS_dz+self.Mirror_d)

            Mirror_lv = geom.structure.Volume('volMirror_LAr',
                                                material=self.Mirror_Material,
                                                shape=Mirror_shape)

            # Place Mirror into main LV
            pos = [self.SiPM_mask_dx+self.SiPM_pcb_dx,Q('0mm'),-self.TPB_dz]

            Mirror_pos = geom.structure.Position('Mirror_pos',
                                                    pos[0],pos[1],pos[2])

            Mirror_pla = geom.structure.Placement('Mirror_pla',
                                                    volume=Mirror_lv,
                                                    pos=Mirror_pos)

            main_lv.placements.append(Mirror_pla.name)

        # Construct WLS panel
        WLS_shape = geom.shapes.Box('WLS_panel',
                                       dx = self.WLS_dx,
                                       dy = self.WLS_dy,
                                       dz = self.WLS_dz)

        WLS_lv = geom.structure.Volume('volWLS',
                                            material=self.WLS_Material,
                                            shape=WLS_shape)

        # Place WLS panel into main LV
        pos = [self.SiPM_mask_dx+self.SiPM_pcb_dx,Q('0mm'),-self.TPB_dz+self.Mirror_d]

        WLS_pos = geom.structure.Position('WLS_pos',
                                                pos[0],pos[1],pos[2])

        WLS_pla = geom.structure.Placement('WLS_pla',
                                                volume=WLS_lv,
                                                pos=WLS_pos)

        main_lv.placements.append(WLS_pla.name)


        # Construct TPB LV
        TPB_shape = geom.shapes.Box('TPB_LAr_layer',
                                       dx = self.WLS_dx,
                                       dy = self.WLS_dy,
                                       dz = self.TPB_dz)

        TPB_lv = geom.structure.Volume('volTPB_LAr',
                                            material=self.Material,
                                            shape=TPB_shape)

        # Place TPB LV next to WLS plane
        pos = [self.SiPM_mask_dx+self.SiPM_pcb_dx,Q('0mm'),self.WLS_dz+self.Mirror_d]

        TPB_pos = geom.structure.Position('TPB_pos',
                                                pos[0],pos[1],pos[2])

        TPB_pla = geom.structure.Placement('TPB_pla',
                                                volume=TPB_lv,
                                                pos=TPB_pos)

        main_lv.placements.append(TPB_pla.name)

        # Construct and place SiPMs and the corresponding masks
        for n in range(self.NMask):
            # Construct Mask LV
            SiPM_mask_shape = geom.shapes.Box('SiPM_mask'+str(n),
                                           dx = self.SiPM_mask_dx,
                                           dy = self.SiPM_mask_dy,
                                           dz = self.SiPM_mask_dz)

            SiPM_mask_lv = geom.structure.Volume('volSiPM_Mask'+str(n),
                                                material=self.SiPM_mask_Material,
                                                shape=SiPM_mask_shape)

            # Place Mask LV next to WLS plane
            pos = [-self.WLS_dx-2*self.Mirror_d+self.SiPM_pcb_dx,-(self.NMask-1)*self.SiPM_mask_dy-(self.NMask-1)*self.SiPM_mask_gap+(2*n)*self.SiPM_mask_dy+(2*n)*self.SiPM_mask_gap,-self.TPB_dz+self.Mirror_d]

            SiPM_mask_pos = geom.structure.Position('SiPM_mask_pos'+str(n),
                                                    pos[0],pos[1],pos[2])

            SiPM_mask_pla = geom.structure.Placement('SiPM_mask_pla'+str(n),
                                                    volume=SiPM_mask_lv,
                                                    pos=SiPM_mask_pos)

            main_lv.placements.append(SiPM_mask_pla.name)

            for m in range(self.NSiPM/self.NMask):
                # Construct SiPM LV
                SiPM_shape = geom.shapes.Box('SiPM'+str(2*n+m),
                                               dx = self.SiPM_dx,
                                               dy = self.SiPM_dy,
                                               dz = self.SiPM_dz)

                SiPM_lv = geom.structure.Volume('volSiPM'+str(2*n+m),
                                                    material=self.SiPM_Material,
                                                    shape=SiPM_shape)

                # Place SiPMs next to WLS plane
                posipm = [-self.WLS_dx-2*self.Mirror_d+self.SiPM_pcb_dx+self.SiPM_couple,pos[1]-(self.NSiPM/self.NMask-1)*self.SiPM_dy-(self.NSiPM/self.NMask-1)*self.SiPM_gap+(2*m)*self.SiPM_dy+(2*m)*self.SiPM_gap,-self.TPB_dz+self.Mirror_d]

                SiPM_pos = geom.structure.Position('SiPM_pos'+str(2*n+m),
                                                        posipm[0],posipm[1],posipm[2])

                SiPM_pla = geom.structure.Placement('SiPM_pla'+str(2*n+m),
                                                        volume=SiPM_lv,
                                                        pos=SiPM_pos)

                main_lv.placements.append(SiPM_pla.name)

        # Construct and place SiPM PCBs
        for n in range(self.NMask):
            # Construct PCB LV
            SiPM_pcb_shape = geom.shapes.Box('SiPM_pcb'+str(n),
                                           dx = self.SiPM_pcb_dx,
                                           dy = self.SiPM_pcb_dy,
                                           dz = self.SiPM_pcb_dz)

            SiPM_pcb_lv = geom.structure.Volume('volSiPM_PCB'+str(n),
                                                material=self.SiPM_pcb_Material,
                                                shape=SiPM_pcb_shape)

            # Place SiPM PCBs next to SiPM Masks
            pos = [-self.WLS_dx-2*self.Mirror_d-self.SiPM_mask_dx,-(self.NMask-1)*self.SiPM_pcb_dy-(self.NMask-1)*self.SiPM_pcb_gap+(2*n)*self.SiPM_pcb_dy+(2*n)*self.SiPM_pcb_gap,-self.TPB_dz+self.Mirror_d]

            SiPM_pcb_pos = geom.structure.Position('SiPM_pcb_pos'+str(n),
                                                    pos[0],pos[1],pos[2])

            SiPM_pcb_pla = geom.structure.Placement('SiPM_pcb_pla'+str(n),
                                                    volume=SiPM_pcb_lv,
                                                    pos=SiPM_pcb_pos)

            main_lv.placements.append(SiPM_pcb_pla.name)
