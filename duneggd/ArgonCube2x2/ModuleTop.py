""" ModuleTop.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ModuleTopBuilder(gegede.builder.Builder):
    """ Class to build ModuleTop geometry.

    """

    def configure(self,ModuleTop_dimension,Flange_dimension,PillowTop_dimension,PillowSide_dimension,PillowBottom_dy,AngleBarTop_dimension,AngleBarSide_dimension,Angle_Length,Angle_dd,N_Angle,LAr_Level_Flange,**kwargs):

        # Read dimensions form config file
        self.ModuleTop_dx       = ModuleTop_dimension['dx']
        self.ModuleTop_dy       = ModuleTop_dimension['dy']
        self.ModuleTop_dz       = ModuleTop_dimension['dz']

        self.Flange_dx          = Flange_dimension['dx']
        self.Flange_dy          = Flange_dimension['dy']
        self.Flange_dz          = Flange_dimension['dz']

        self.PillowTop_dx       = PillowTop_dimension['dx']
        self.PillowTop_dy       = PillowTop_dimension['dy']
        self.PillowTop_dz       = PillowTop_dimension['dz']

        self.PillowSide_dx      = PillowSide_dimension['dx']
        self.PillowSide_dy      = PillowSide_dimension['dy']
        self.PillowSide_dz      = PillowSide_dimension['dz']
        self.PillowSide_dd      = PillowSide_dimension['dd']

        self.PillowBottom_dy    = PillowBottom_dy

        self.AngleBarTop_dx     = AngleBarTop_dimension['dx']
        self.AngleBarTop_dy     = AngleBarTop_dimension['dy']
        self.AngleBarTop_dz     = AngleBarTop_dimension['dz']
        self.AngleBarTop_gap    = AngleBarTop_dimension['gap']

        self.AngleBarSide_dx    = AngleBarSide_dimension['dx']
        self.AngleBarSide_dy    = AngleBarSide_dimension['dy']
        self.AngleBarSide_dz    = AngleBarSide_dimension['dz']

        self.Angle_Length       = Angle_Length
        self.Angle_dd           = Angle_dd
        self.N_Angle            = N_Angle
        self.Angle_gap          = (self.AngleBarTop_dz-self.Angle_Length*self.N_Angle)/(self.N_Angle-1)

        self.GAr_dy             = LAr_Level_Flange
        self.LAr_dy             = self.ModuleTop_dy-self.GAr_dy

        # Material definitons
        self.ModuleTop_Material = 'Steel'
        self.LArPhase_Material  = 'LAr'
        self.GArPhase_Material  = 'GAr'

        self.Material           = 'Air'

        # Subbuilders
        self.Backplate_builder  = self.get_builder('Backplate')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.ModuleTop_dx,
                                'dy':   self.ModuleTop_dy,
                                'dz':   self.ModuleTop_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleTopBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct LAr Phase ModuleTop Volume
        LArPhaseModuleTop_shape = geom.shapes.Box('LArPhaseModuleTop_shape',
                                        dx = self.ModuleTop_dx,
                                        dy = self.LAr_dy,
                                        dz = self.ModuleTop_dz)

        LArPhaseModuleTop_lv = geom.structure.Volume('volLArPhaseModuleTop',
                                        material=self.LArPhase_Material,
                                        shape=LArPhaseModuleTop_shape)

        # Place LAr Phase ModuleTop Volume inside ModuleTop volume
        pos = [Q('0cm'),-self.GAr_dy,Q('0cm')]

        LArPhaseModuleTop_pos = geom.structure.Position('LArPhaseModuleTop_pos',
                                                pos[0],pos[1],pos[2])

        LArPhaseModuleTop_pla = geom.structure.Placement('LArPhaseModuleTop_pla',
                                                volume=LArPhaseModuleTop_lv,
                                                pos=LArPhaseModuleTop_pos)

        main_lv.placements.append(LArPhaseModuleTop_pla.name)

        # Construct GAr Phase ModuleTop Volume
        GArPhaseModuleTop_shape = geom.shapes.Box('GArPhaseModuleTop_shape',
                                        dx = self.ModuleTop_dx,
                                        dy = self.GAr_dy,
                                        dz = self.ModuleTop_dz)

        GArPhaseModuleTop_lv = geom.structure.Volume('volGArPhaseModuleTop',
                                        material=self.GArPhase_Material,
                                        shape=GArPhaseModuleTop_shape)

        # Place GAr Phase ModuleTop Volume inside ModuleTop volume
        pos = [Q('0cm'),self.LAr_dy,Q('0cm')]

        GArPhaseModuleTop_pos = geom.structure.Position('GArPhaseModuleTop_pos',
                                                pos[0],pos[1],pos[2])

        GArPhaseModuleTop_pla = geom.structure.Placement('GArPhaseModuleTop_pla',
                                                volume=GArPhaseModuleTop_lv,
                                                pos=GArPhaseModuleTop_pos)

        main_lv.placements.append(GArPhaseModuleTop_pla.name)

        # Construct Flange Volume
        Flange_shape = geom.shapes.Box('Flange_shape',
                                        dx = self.Flange_dx,
                                        dy = self.Flange_dy,
                                        dz = self.Flange_dz)

        Flange_lv = geom.structure.Volume('volFlange',
                                        material=self.ModuleTop_Material,
                                        shape=Flange_shape)

        # Place Flange Volume inside Module Top volume
        pos = [Q('0cm'),self.ModuleTop_dy-self.Flange_dy,Q('0cm')]

        Flange_pos = geom.structure.Position('Flange_pos',
                                                pos[0],pos[1],pos[2])

        Flange_pla = geom.structure.Placement('Flange_pla',
                                                volume=Flange_lv,
                                                pos=Flange_pos)

        main_lv.placements.append(Flange_pla.name)

        # Construct Pillow Top Volume
        PillowTop_shape = geom.shapes.Box('PillowTop_shape',
                                        dx = self.PillowTop_dx,
                                        dy = self.PillowTop_dy,
                                        dz = self.PillowTop_dz)

        PillowTop_lv = geom.structure.Volume('volPillowTop',
                                        material=self.ModuleTop_Material,
                                        shape=PillowTop_shape)

        # Place Pillow Top Volume inside Module Top volume
        pos = [Q('0cm'),self.ModuleTop_dy-2*self.Flange_dy-self.PillowTop_dy,Q('0cm')]

        PillowTop_pos = geom.structure.Position('PillowTop_pos',
                                                pos[0],pos[1],pos[2])

        PillowTop_pla = geom.structure.Placement('PillowTop_pla',
                                                volume=PillowTop_lv,
                                                pos=PillowTop_pos)

        main_lv.placements.append(PillowTop_pla.name)

        # Construct Pillow Side Volume
        PillowSide_shape = geom.shapes.Box('PillowSide_shape',
                                        dx = self.PillowSide_dx,
                                        dy = self.PillowSide_dy,
                                        dz = self.PillowSide_dz)

        PillowSide_lv = geom.structure.Volume('volPillowSide',
                                        material=self.ModuleTop_Material,
                                        shape=PillowSide_shape)

        # Place Pillow Side Volume inside Module Top volume
        pos = [Q('0cm'),self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-self.PillowSide_dy,Q('0cm')]

        PillowSide_pos = geom.structure.Position('PillowSide_pos',
                                                pos[0],pos[1],pos[2])

        PillowSide_pla = geom.structure.Placement('PillowSide_pla',
                                                volume=PillowSide_lv,
                                                pos=PillowSide_pos)

        main_lv.placements.append(PillowSide_pla.name)

        # Construct Pillow Cavity Volume
        PillowCavity_shape = geom.shapes.Box('PillowCavity_shape',
                                        dx = self.PillowSide_dx-2*self.PillowSide_dd,
                                        dy = self.PillowSide_dy-self.PillowBottom_dy,
                                        dz = self.PillowSide_dz-2*self.PillowSide_dd)

        PillowCavity_lv = geom.structure.Volume('volPillowCavity',
                                        material=self.Material,
                                        shape=PillowCavity_shape)

        # Place Pillow Cavity Volume inside Module Top volume
        pos = [Q('0cm'),self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-self.PillowSide_dy+self.PillowBottom_dy,Q('0cm')]

        PillowCavity_pos = geom.structure.Position('PillowCavity_pos',
                                                pos[0],pos[1],pos[2])

        PillowCavity_pla = geom.structure.Placement('PillowCavity_pla',
                                                volume=PillowCavity_lv,
                                                pos=PillowCavity_pos)

        main_lv.placements.append(PillowCavity_pla.name)

        # Construct Angle Bar Top Volume
        AngleBarTop_shape = geom.shapes.Box('AngleBarTop_shape',
                                        dx = self.AngleBarTop_dx,
                                        dy = self.AngleBarTop_dy,
                                        dz = self.AngleBarTop_dz)

        AngleBarTop_lv = geom.structure.Volume('volAngleBarTop',
                                        material=self.ModuleTop_Material,
                                        shape=AngleBarTop_shape)

        # Place Angle Bar Top L Volume inside Module Top volume
        pos = [-self.AngleBarTop_gap-self.AngleBarTop_dx,self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-2*self.PillowSide_dy-self.AngleBarTop_dy,Q('0cm')]

        AngleBarTop_L_pos = geom.structure.Position('AngleBarTop_L_pos',
                                                pos[0],pos[1],pos[2])

        AngleBarTop_L_pla = geom.structure.Placement('AngleBarTop_L_pla',
                                                volume=AngleBarTop_lv,
                                                pos=AngleBarTop_L_pos)

        main_lv.placements.append(AngleBarTop_L_pla.name)

        # Place Angle Bar Top R Volume inside Module Top volume
        pos = [self.AngleBarTop_gap+self.AngleBarTop_dx,self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-2*self.PillowSide_dy-self.AngleBarTop_dy,Q('0cm')]

        rot_y = Q('180.0deg')

        AngleBarTop_R_rot = geom.structure.Rotation('AngleBarTop_R_rot',
                                                y=rot_y)

        AngleBarTop_R_pos = geom.structure.Position('AngleBarTop_R_pos',
                                                pos[0],pos[1],pos[2])

        AngleBarTop_R_pla = geom.structure.Placement('AngleBarTop_R_pla',
                                                volume=AngleBarTop_lv,
                                                pos=AngleBarTop_R_pos,
                                                rot=AngleBarTop_R_rot)

        main_lv.placements.append(AngleBarTop_R_pla.name)

        # Construct Angle Base Volume
        AngleBase_shape = geom.shapes.Box('AngleBase_shape',
                                        dx = self.AngleBarTop_dx,
                                        dy = self.Angle_dd,
                                        dz = self.Angle_Length)

        AngleBase_lv = geom.structure.Volume('volAngleBase',
                                        material=self.ModuleTop_Material,
                                        shape=AngleBase_shape)

        # Place Angle Base Volume Module Top volume
        for i in range(2):
            for j in range(self.N_Angle):
                pos = [(-1)**i*(self.AngleBarTop_gap+AngleBase_shape[1]),self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-2*self.PillowSide_dy-2*self.AngleBarTop_dy-self.Angle_dd,-(self.N_Angle-1-2*j)*self.Angle_Length-(self.N_Angle-1-2*j)*self.Angle_gap]

                AngleBase_pos = geom.structure.Position('AngleBase_pos_'+str(i*self.N_Angle+j),
                                                        pos[0],pos[1],pos[2])

                AngleBase_pla = geom.structure.Placement('AngleBase_pla_'+str(i*self.N_Angle+j),
                                                        volume=AngleBase_lv,
                                                        pos=AngleBase_pos)

                main_lv.placements.append(AngleBase_pla.name)

        # Construct Angle Side Volume
        AngleSide_shape = geom.shapes.Box('AngleSide_shape',
                                        dx = self.Angle_dd,
                                        dy = self.AngleBarTop_dx-self.Angle_dd,
                                        dz = self.Angle_Length)

        AngleSide_lv = geom.structure.Volume('volAngleSide',
                                        material=self.ModuleTop_Material,
                                        shape=AngleSide_shape)

        # Place Angle Side Volume Module Top volume
        for i in range(2):
            for j in range(self.N_Angle):
                pos = [(-1)**i*(self.AngleBarTop_gap+2*self.AngleBarTop_dx-AngleSide_shape[1]),self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-2*self.PillowSide_dy-2*self.AngleBarTop_dy-2*self.Angle_dd-AngleSide_shape[2],-(self.N_Angle-1-2*j)*self.Angle_Length-(self.N_Angle-1-2*j)*self.Angle_gap]

                AngleSide_pos = geom.structure.Position('AngleSide_pos_'+str(i*self.N_Angle+j),
                                                        pos[0],pos[1],pos[2])

                AngleSide_pla = geom.structure.Placement('AngleSide_pla_'+str(i*self.N_Angle+j),
                                                        volume=AngleSide_lv,
                                                        pos=AngleSide_pos)

                main_lv.placements.append(AngleSide_pla.name)

        # Construct Angle Bar Side Volume
        AngleBarSide_shape = geom.shapes.Box('AngleBarSide_shape',
                                        dx = self.AngleBarSide_dx,
                                        dy = self.AngleBarSide_dy,
                                        dz = self.AngleBarSide_dz)

        AngleBarSide_lv = geom.structure.Volume('volAngleBarSide',
                                        material=self.ModuleTop_Material,
                                        shape=AngleBarSide_shape)

        # Place Angle Bar Side Volume Module Top volume
        for i in range(2):
            pos = [(-1)**i*(self.AngleBarTop_gap+2*self.AngleBarTop_dx+2*self.Backplate_builder.halfDimension['dx']+self.AngleBarSide_dx),self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-2*self.PillowSide_dy-2*self.AngleBarTop_dy-2*self.Angle_dd-2*AngleSide_shape[2]+self.AngleBarSide_dy,Q('0cm')]

            AngleBarSide_pos = geom.structure.Position('AngleBarSide_pos_'+str(i*self.N_Angle+j),
                                                    pos[0],pos[1],pos[2])

            AngleBarSide_pla = geom.structure.Placement('AngleBarSide_pla_'+str(i*self.N_Angle+j),
                                                    volume=AngleBarSide_lv,
                                                    pos=AngleBarSide_pos)

            main_lv.placements.append(AngleBarSide_pla.name)

        # Build Backplate L
        pos = [self.AngleBarTop_gap+2*self.AngleBarTop_dx+self.Backplate_builder.halfDimension['dx'],-self.halfDimension['dy']+self.Backplate_builder.halfDimension['dy'],Q('0cm')]

        Backplate_lv = self.Backplate_builder.get_volume()

        Backplate_pos = geom.structure.Position(self.Backplate_builder.name+'_pos_L',
                                                pos[0],pos[1],pos[2])

        Backplate_pla = geom.structure.Placement(self.Backplate_builder.name+'_pla_L',
                                                volume=Backplate_lv,
                                                pos=Backplate_pos)

        main_lv.placements.append(Backplate_pla.name)

        # Build Backplate R
        pos = [-self.AngleBarTop_gap-2*self.AngleBarTop_dx-self.Backplate_builder.halfDimension['dx'],-self.halfDimension['dy']+self.Backplate_builder.halfDimension['dy'],Q('0cm')]

        Backplate_lv = self.Backplate_builder.get_volume()

        Backplate_pos = geom.structure.Position(self.Backplate_builder.name+'_pos_R',
                                                pos[0],pos[1],pos[2])

        Backplate_pla = geom.structure.Placement(self.Backplate_builder.name+'_pla_R',
                                                volume=Backplate_lv,
                                                pos=Backplate_pos)

        main_lv.placements.append(Backplate_pla.name)

