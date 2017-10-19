"""
A basic builder for a gas TPC consisting of a cylindrical chamber 
with two back-to-back rectangular active volmes.

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class GArTPCBuilder(gegede.builder.Builder):
    """ Build the Gas TPC volume. """

    def configure(self,chamberDimension,tpcDimension,
                  halfDimension,Material,bfield=None,drift='z',**kwargs):

        # The vacuum chamber is a G4Tubs for now
        self.ChamberRadius = chamberDimension['r']
        self.ChamberLength = chamberDimension['dz']

        self.EndCapThickness = Q("1cm")
        self.WallThickness = Q("1cm")
        self.ChamberMaterial = "Steel"

        # Should be a 3D array Quantity objects
        # Will support dipole and solenoid type fields
        # Really should be set with a magnet builder but here for testing
        # Not currently used
        self.BField = bfield
        
        # The gas
        if type(Material)=='string':
            # Set from a pre-defined material
            self.Material = Material
            self.GasDensity = None
            self.Composition = None
        else:
            # Set from a dictionary of materials & mass fractions
            comp = []
            for k in Material.keys():
                comp.append( (k,Material[k]) )
            self.Composition = tuple(comp)
            self.Material = kwargs['MaterialName']
            self.GasDensity = kwargs['Density']
 
        self.halfDimension = halfDimension
        # The TPCs: Boxes at the center of the vacuum chamber
        self.tpcDimension = tpcDimension
        self.HalfX = tpcDimension['dx']/2 
        self.HalfY = tpcDimension['dy']/2
        self.HalfZ = tpcDimension['dz']/2
        self.Drift = drift



    def construct(self,geom):

        # If using a custom gas, define here
        if self.Composition is not None:
            geom.matter.Mixture(self.Material,density=self.GasDensity,components=self.Composition)

        main_lv, main_hDim = ltools.main_lv(self,geom,'Tubs')
        print('GasTPCBuilder::construct()')
        print('main_lv = ',main_lv.name)
        self.add_volume(main_lv)

        # Construct the chamber
        tpc_chamber_shape = geom.shapes.Tubs('TPCChamber',
                                       rmax = self.ChamberRadius,
                                       dz = self.ChamberLength*0.5)
        tpc_chamber_lv = geom.structure.Volume('TPCChamber_vol',
                                               material=self.ChamberMaterial,
                                               shape=tpc_chamber_shape)


        # Place into main LV
        pos = [Q('0m'),Q('0m'),Q('0m')]
        tpc_chamber_pos = geom.structure.Position('TPCChamber_pos',
                                                  pos[0],pos[1],pos[2])
        tpc_chamber_pla = geom.structure.Placement('TPCChamber_pla',
                                                   volume=tpc_chamber_lv,
                                                   pos=tpc_chamber_pos)
        main_lv.placements.append(tpc_chamber_pla.name)

  
        # Add in the gas volume
        tpc_gas_shape = geom.shapes.Tubs('TPCGas',
                             rmax=self.ChamberRadius-self.WallThickness,
                             dz=0.5*self.ChamberLength - self.EndCapThickness)

        tpc_gas_lv = geom.structure.Volume('TPCGas_vol',
                                           material='GAr',#self.Material,
                                           shape=tpc_gas_shape)

        # Place gas into the chamber
        pos = [Q('0m'),Q('0m'),Q('0m')]
        tpc_gas_pos = geom.structure.Position('TPCGas_pos',
                                              pos[0],pos[1],pos[2])
        tpc_gas_pla = geom.structure.Placement('TPCGas_pla',
                                               volume=tpc_gas_lv,
                                               pos=tpc_gas_pos)
        tpc_chamber_lv.placements.append(tpc_gas_pla.name)

        
        # Construct the TPCs
        self.construct_tpcs(geom,tpc_gas_lv)
        

    def construct_tpcs(self,geom,lv):
        gap = Q('2mm') # A bit of space for the central electrode

        # TPC1
        tpc1_shape = geom.shapes.Box('TPC1',self.HalfX,self.HalfY,self.HalfZ)
        tpc1_lv = geom.structure.Volume('TPC1_vol',material = self.Material,
                                        shape=tpc1_shape)
        tpc2_shape = geom.shapes.Box('TPC2',self.HalfX,self.HalfY,self.HalfZ)
        tpc2_lv = geom.structure.Volume('TPC2_vol',material = self.Material,
                                        shape=tpc2_shape)

        tpc1_lv.params.append(('SensDet','TPC1'))
        tpc2_lv.params.append(('SensDet','TPC2'))

        tpc1_pos = None 
        tpc2_pos = None
        rot1 = []
        rot2 = []
        rot0 = [Q('0deg'),Q('0deg'),Q('0deg')]
        
        if self.Drift == 'y':

            tpc1_pos = geom.structure.Position('TPC1_pos',Q('0mm'),
                                               self.HalfZ+gap,Q('0mm'))
            tpc2_pos = geom.structure.Position('TPC2_pos',Q('0mm'),
                                               -self.HalfZ-gap,Q('0mm'))
            
            rot1 = [Q('270deg'),Q('0deg'),Q('0deg')]
            rot2 = [Q('90deg'),Q('0deg'),Q('0deg')]

        elif self.Drift == 'x':
            tpc1_pos = geom.structure.Position('TPC1_pos',self.HalfZ+gap,
                                               Q('0mm'),Q('0mm'))
            tpc2_pos = geom.structure.Position('TPC2_pos',-self.HalfZ-gap,
                                               Q('0mm'),Q('0mm'))

            rot1 = [Q('0deg'),Q('90deg'),Q('0deg')]
            rot2 = [Q('0deg'),Q('270deg'),Q('0deg')]

        else:
            tpc1_pos = geom.structure.Position('TPC1_pos',Q('0mm'),Q('0mm'),-self.HalfZ-gap)
            tpc2_pos = geom.structure.Position('TPC2_pos',Q('0mm'),Q('0mm'),self.HalfZ+gap)
            rot1 = [Q('0deg'),Q('0deg'),Q('0deg')]
            rot2 = [Q('180deg'),Q('0deg'),Q('0deg')]

        tpc1_rot = geom.structure.Rotation('TPC1_rot',rot1[0],rot1[1],rot1[2])
        tpc2_rot = geom.structure.Rotation('TPC2_rot',rot2[0],rot2[1],rot2[2])

        tpc1_pla = geom.structure.Placement('TPC1_pla',
                                            volume=tpc1_lv,
                                            pos=tpc1_pos,
                                            rot=tpc1_rot
                                           )

        tpc2_pla = geom.structure.Placement('TPC2_pla',
                                            volume=tpc2_lv,
                                            pos=tpc2_pos,
                                            rot=tpc2_rot
                                           )
        lv.placements.append(tpc1_pla.name)
        lv.placements.append(tpc2_pla.name)
