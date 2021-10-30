import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class SandInnerVolumeBuilder(gegede.builder.Builder):
    def configure( self, halfDimension=None, Material=None, nBarrelModules=None, liqArThickness=None, **kwds):
        self.halfDimension = halfDimension
        self.Material =      Material
        self.kloeVesselRadius       = self.halfDimension['rmax']
        self.kloeVesselHalfDx       = self.halfDimension['dz']
        self.nBarrelModules         = nBarrelModules
        self.rotAngle               = 0.5 * Q('360deg') / self.nBarrelModules
        self.liqArThickness         = liqArThickness

    def construct(self,geom):
        sand_inner_volume_shape=geom.shapes.PolyhedraRegular("sand_inner_volume_shape",numsides=self.nBarrelModules, rmin=Q('0cm'), rmax=self.kloeVesselRadius , dz=self.kloeVesselHalfDx, sphi=self.rotAngle)
        main_lv = geom.structure.Volume('sand_inner_volume',   material=self.Material, shape=sand_inner_volume_shape)
        self.add_volume( main_lv )
        self.build_stt(main_lv, geom)
        self.build_grain(main_lv, geom)

    def build_stt(self, main_lv, geom):
        if "STT" not in self.builders:
            print("STT builder not found")
            return        
        
        
        stt_builder=self.get_builder("STT")
        stt_lv=stt_builder.get_volume()

        stt_position = geom.structure.Position(
                'stt_position', Q('0m'), Q('0m'), Q('0m'))

        stt_rotation = geom.structure.Rotation(
                'stt_rotation', Q('0deg'), Q('180deg'), Q('0deg'))

        stt_placement = geom.structure.Placement('stt_place',
                                                  volume=stt_lv,
                                                  pos=stt_position,
                                                  rot=stt_rotation)

        main_lv.placements.append(stt_placement.name) 

    def build_grain(self, main_lv, geom):
        if "GRAIN" not in self.builders:
            print("GRAIN builder not found")
            return        

        grain_builder=self.get_builder("GRAIN")
        grain_lv=grain_builder.get_volume()
        
        grain_position = geom.structure.Position("grain_position",
                                      self.kloeVesselRadius-0.5*self.liqArThickness,
                                      Q('0mm'),
                                      Q('0mm'))

        grain_rotation = geom.structure.Rotation(
                'grain_rotation', Q('0deg'), Q('0deg'), Q('0deg'))

        grain_placement = geom.structure.Placement('grain_place',
                                                  volume=grain_lv,
                                                  pos=grain_position,
                                                  rot=grain_rotation)
        main_lv.placements.append(grain_placement.name) 
        