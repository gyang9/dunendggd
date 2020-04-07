""" Feedthrough.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class FeedthroughBuilder(gegede.builder.Builder):
    """ Class to build Feedthrough geometry.

    """

    def configure(self,TubeCenter_dimension,TubeSide_dimension,**kwargs):

        # Read dimensions form config file
        self.TubeCenter_rmin    = TubeCenter_dimension['rmin']
        self.TubeCenter_rmax    = TubeCenter_dimension['rmax']
        self.TubeCenter_dz      = TubeCenter_dimension['dz']

        self.TubeSide_rmin      = TubeSide_dimension['rmin']
        self.TubeSide_rmax      = TubeSide_dimension['rmax']
        self.TubeSide_dz_long   = TubeSide_dimension['dz_long']
        self.TubeSide_dz_short  = TubeSide_dimension['dz_short']
        self.TubeSide_Offset    = TubeSide_dimension['offset']

        # Material definitons
        self.Flange_Material    = 'Steel'
        self.Vacuum_Material    = 'GAr' #'Vacuum' CHANGE!!!!!
        self.Tube_Material      = 'Steel'
        self.GAr_Material       = 'GAr'

        self.Material           = 'Air'

        # Subbuilders
        self.Flange_builder     = self.get_builder('Flange')
        self.Pillow_builder     = self.get_builder('Pillow')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.Feedthrough_dx     = self.Pillow_builder.PillowSide_dx-2*self.Pillow_builder.PillowSide_dd
        self.Feedthrough_dy     = self.TubeSide_dz_long
        self.Feedthrough_dz     = self.Pillow_builder.PillowSide_dz-2*self.Pillow_builder.PillowSide_dd

        self.halfDimension  = { 'dx':   self.Feedthrough_dx,
                                'dy':   self.Feedthrough_dy,
                                'dz':   self.Feedthrough_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('FeedthroughBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct FlangePart Volume
        FlangePart_shape = geom.shapes.Box('FlangePart_shape',
                                        dx = self.halfDimension['dx'],
                                        dy = self.Flange_builder.halfDimension['dy'],
                                        dz = self.halfDimension['dz'])

        FlangePart_lv = geom.structure.Volume('volFlangePart',
                                        material=self.Flange_Material,
                                        shape=FlangePart_shape)

        # Place FlangePart Volume inside Feedthrough volume
        pos = [Q('0cm'),-self.halfDimension['dy']+2*self.Pillow_builder.PillowSide_dy+self.Flange_builder.halfDimension['dy'],Q('0cm')]

        FlangePart_pos = geom.structure.Position('FlangePart_pos',
                                                pos[0],pos[1],pos[2])

        FlangePart_pla = geom.structure.Placement('FlangePart_pla',
                                                volume=FlangePart_lv,
                                                pos=FlangePart_pos)

        main_lv.placements.append(FlangePart_pla.name)

        # Construct VacuumPart Volume
        VacuumPart_shape = geom.shapes.Box('VacuumPart_shape',
                                        dx = self.halfDimension['dx'],
                                        dy = self.Pillow_builder.PillowSide_dy-self.Pillow_builder.PillowBottom_dy,
                                        dz = self.halfDimension['dz'])

        VacuumPart_lv = geom.structure.Volume('volVacuumPart',
                                        material=self.Vacuum_Material,
                                        shape=VacuumPart_shape)

        # Place VacuumPart Volume inside Feedthrough volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.Pillow_builder.PillowBottom_dy+self.Pillow_builder.PillowSide_dy,Q('0cm')]

        VacuumPart_pos = geom.structure.Position('VacuumPart_pos',
                                                pos[0],pos[1],pos[2])

        VacuumPart_pla = geom.structure.Placement('VacuumPart_pla',
                                                volume=VacuumPart_lv,
                                                pos=VacuumPart_pos)

        main_lv.placements.append(VacuumPart_pla.name)

        # Construct PillowPart Volume
        PillowPart_shape = geom.shapes.Box('PillowPart_shape',
                                        dx = self.halfDimension['dx'],
                                        dy = self.Pillow_builder.PillowBottom_dy,
                                        dz = self.halfDimension['dz'])

        PillowPart_lv = geom.structure.Volume('volPillowPart',
                                        material=self.Flange_Material,
                                        shape=PillowPart_shape)

        # Place PillowPart Volume inside Feedthrough volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.Pillow_builder.PillowBottom_dy,Q('0cm')]

        PillowPart_pos = geom.structure.Position('PillowPart_pos',
                                                pos[0],pos[1],pos[2])

        PillowPart_pla = geom.structure.Placement('PillowPart_pla',
                                                volume=PillowPart_lv,
                                                pos=PillowPart_pos)

        main_lv.placements.append(PillowPart_pla.name)

        # Construct TubeCenter Volume
        TubeCenter_shape = geom.shapes.Tubs('TubeCenter_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeCenter_rmax,
                                        dz = self.TubeCenter_dz)

        TubeCenter_lv = geom.structure.Volume('volTubeCenter',
                                        material=self.Tube_Material,
                                        shape=TubeCenter_shape)

        # Construct TubeCenterGAr Volume
        TubeCenterGAr_shape = geom.shapes.Tubs('TubeCenterGAr_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeCenter_rmin,
                                        dz = self.TubeCenter_dz)

        TubeCenterGAr_lv = geom.structure.Volume('volTubeCenterGAr',
                                        material=self.GAr_Material,
                                        shape=TubeCenterGAr_shape)

        # Place TubeCenterGAr Volume inside TubeCenter volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        TubeCenterGAr_pos = geom.structure.Position('TubeCenterGAr_pos',
                                                pos[0],pos[1],pos[2])

        TubeCenterGAr_pla = geom.structure.Placement('TubeCenterGAr_pla',
                                                volume=TubeCenterGAr_lv,
                                                pos=TubeCenterGAr_pos)

        TubeCenter_lv.placements.append(TubeCenterGAr_pla.name)

        # Place TubeCenter Volume inside Feedthrough volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.TubeCenter_dz,Q('0cm')]

        rot_x = Q('90.0deg')

        TubeCenter_pos = geom.structure.Position('TubeCenter_pos',
                                                pos[0],pos[1],pos[2])

        TubeCenter_rot = geom.structure.Rotation('TubeCenter_rot',
                                                rot_x)

        TubeCenter_pla = geom.structure.Placement('TubeCenter_pla',
                                                volume=TubeCenter_lv,
                                                pos=TubeCenter_pos,
                                                rot=TubeCenter_rot)

        main_lv.placements.append(TubeCenter_pla.name)

        # Construct TubeSideLong Volume
        TubeSideLong_shape = geom.shapes.Tubs('TubeSideLong_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeSide_rmax,
                                        dz = self.TubeSide_dz_long)

        TubeSideLong_lv = geom.structure.Volume('volTubeSideLong',
                                        material=self.Tube_Material,
                                        shape=TubeSideLong_shape)

        # Construct TubeSideLongGAr Volume
        TubeSideLongGAr_shape = geom.shapes.Tubs('TubeSideLongGAr_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeSide_rmin,
                                        dz = self.TubeSide_dz_long)

        TubeSideLongGAr_lv = geom.structure.Volume('volTubeSideLongGAr',
                                        material=self.GAr_Material,
                                        shape=TubeSideLongGAr_shape)

        # Place TubeSideLongGAr Volume inside TubeSideLong volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        TubeSideLongGAr_pos = geom.structure.Position('TubeSideLongGAr_pos',
                                                pos[0],pos[1],pos[2])

        TubeSideLongGAr_pla = geom.structure.Placement('TubeSideLongGAr_pla',
                                                volume=TubeSideLongGAr_lv,
                                                pos=TubeSideLongGAr_pos)

        TubeSideLong_lv.placements.append(TubeSideLongGAr_pla.name)

        # Place TubeSideLong Volume inside Feedthrough volume
        for i in range(2):
            pos = [Q('0cm'),-self.halfDimension['dy']+self.TubeSide_dz_long,(-1)**i*2*self.TubeSide_Offset]

            rot_x = Q('90.0deg')

            TubeSideLong_pos = geom.structure.Position('TubeSideLong_pos_'+str(i),
                                                    pos[0],pos[1],pos[2])

            TubeSideLong_rot = geom.structure.Rotation('TubeSideLong_rot_'+str(i),
                                                    rot_x)

            TubeSideLong_pla = geom.structure.Placement('TubeSideLong_pla_'+str(i),
                                                    volume=TubeSideLong_lv,
                                                    pos=TubeSideLong_pos,
                                                    rot=TubeSideLong_rot)

            main_lv.placements.append(TubeSideLong_pla.name)

        # Construct TubeSideShort Volume
        TubeSideShort_shape = geom.shapes.Tubs('TubeSideShort_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeSide_rmax,
                                        dz = self.TubeSide_dz_short)

        TubeSideShort_lv = geom.structure.Volume('volTubeSideShort',
                                        material=self.Tube_Material,
                                        shape=TubeSideShort_shape)

        # Construct TubeSideShortGAr Volume
        TubeSideShortGAr_shape = geom.shapes.Tubs('TubeSideShortGAr_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeSide_rmin,
                                        dz = self.TubeSide_dz_short)

        TubeSideShortGAr_lv = geom.structure.Volume('volTubeSideShortGAr',
                                        material=self.GAr_Material,
                                        shape=TubeSideShortGAr_shape)

        # Place TubeSideShortGAr Volume inside TubeSideShort volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        TubeSideShortGAr_pos = geom.structure.Position('TubeSideShortGAr_pos',
                                                pos[0],pos[1],pos[2])

        TubeSideShortGAr_pla = geom.structure.Placement('TubeSideShortGAr_pla',
                                                volume=TubeSideShortGAr_lv,
                                                pos=TubeSideShortGAr_pos)

        TubeSideShort_lv.placements.append(TubeSideShortGAr_pla.name)

        # Place TubeSideShort Volume inside Feedthrough volume
        for i in range(2):
            pos = [(-1)**i*2*self.TubeSide_Offset,-self.halfDimension['dy']+self.TubeSide_dz_short,Q('0cm')]

            rot_x = Q('90.0deg')

            TubeSideShort_pos = geom.structure.Position('TubeSideShort_pos_'+str(i),
                                                    pos[0],pos[1],pos[2])

            TubeSideShort_rot = geom.structure.Rotation('TubeSideShort_rot_'+str(i),
                                                    rot_x)

            TubeSideShort_pla = geom.structure.Placement('TubeSideShort_pla_'+str(i),
                                                    volume=TubeSideShort_lv,
                                                    pos=TubeSideShort_pos,
                                                    rot=TubeSideShort_rot)

            main_lv.placements.append(TubeSideShort_pla.name)

