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
        # A bit of space for the central electrode
        self.TPCGap = Q('2mm') 


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


        pos1 = []
        pos2 = []
        rot1 = []
        rot2 = []
        
        if self.Drift == 'y':

            pos1 = [0,1,0]
            pos2 = [0,-1,0]
            rot1 = [Q('270deg'),Q('0deg'),Q('0deg')]
            rot2 = [Q('90deg'),Q('0deg'),Q('0deg')]

        elif self.Drift == 'x':

            pos1 = [1,0,0]
            pos2 = [-1,0,0]
            rot1 = [Q('0deg'),Q('90deg'),Q('0deg')]
            rot2 = [Q('0deg'),Q('270deg'),Q('0deg')]

        else:
            pos1 = [0,0,-1]
            pos2 = [0,0,1]
            rot1 = [Q('0deg'),Q('0deg'),Q('0deg')]
            rot2 = [Q('180deg'),Q('0deg'),Q('0deg')]


        self.construct_tpc(geom,"TPC1",pos1,rot1,lv)
        self.construct_tpc(geom,"TPC2",pos2,rot2,lv)


    def construct_tpc(self,geom,name,pos_vec,rot,lv):

        # First, set up the main rotation and position to be used for the TPC
        tpc_rot = geom.structure.Rotation(name+'_rot',rot[0],rot[1],rot[2])
        pos = [ x*(self.HalfZ + self.TPCGap) for x in pos_vec]
        tpc_pos = geom.structure.Position(name+'_pos',pos[0],pos[1],pos[2])
 
        # Create the shape and logical volume
        tpc_shape = geom.shapes.Box(name+'_shape',self.HalfX,self.HalfY,self.HalfZ)
        tpc_lv = geom.structure.Volume(name+'_vol',material = self.Material,
                                       shape=tpc_shape)

        # Create a placement
        tpc_pla = geom.structure.Placement(name+'_pla',
                                            volume=tpc_lv,
                                            pos=tpc_pos,
                                            rot=tpc_rot
                                           )

        # The gas volumes are sensitive detectors
        tpc_lv.params.append(('SensDet',name))

        # Place in the main gas volume
        lv.placements.append(tpc_pla.name)

       
