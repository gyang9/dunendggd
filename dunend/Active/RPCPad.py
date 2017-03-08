#!/usr/bin/env python
'''
Subbuilder of RPCTray*Builder
'''

import gegede.builder
from gegede import Quantity as Q

class RPCModBuilder(gegede.builder.Builder):
    '''
    Build the RPC modules, the effective unit of the MuID, 
    constituting an X and Y plane of RPC strips 
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  rpcModDim    = None, 
                  resiplateDim = None, 
                  stripxDim    = None,
                  stripyDim    = None,
                  gas_gap      = None,
                  rpcModMat=None, resiplateMat=None, 
                  gasMat=None, rpcReadoutMat=None, **kwds):
         self.rpcModMat     = rpcModMat
         self.rpcReadoutMat = rpcReadoutMat
         self.resiplateMat  = resiplateMat
         self.gasMat        = gasMat
         self.rpcModDim     = rpcModDim
         self.resiplateDim  = resiplateDim
         self.stripxDim      = stripxDim
         self.stripyDim      = stripyDim
         self.gas_gap       = gas_gap


    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # define box and volume for whole RPCMod,
        # to be retrieved by RPCTray*Builder
        rpcMod = geom.shapes.Box( self.name,
                                  dx = 0.5*self.rpcModDim[0],
                                  dy = 0.5*self.rpcModDim[1],
                                  dz = 0.5*self.rpcModDim[2])
        rpcMod_lv = geom.structure.Volume('vol'+self.name, material=self.rpcModMat, shape=rpcMod)
        # define box and volume for RPC strip
        rpcStripx = geom.shapes.Box( 'RPCStripx',
                                    dx = 0.5*self.stripxDim[0],
                                    dy = 0.5*self.stripxDim[1],
                                    dz = 0.5*self.stripxDim[2])
        rpcStripx_lv = geom.structure.Volume('volRPCStripx', material=self.rpcReadoutMat, shape=rpcStripx)
        rpcStripy = geom.shapes.Box( 'RPCStripy',
                                    dx = 0.5*self.stripyDim[0],
                                    dy = 0.5*self.stripyDim[1],
                                    dz = 0.5*self.stripyDim[2])
        rpcStripy_lv = geom.structure.Volume('volRPCStripy', material=self.rpcReadoutMat, shape=rpcStripy)
        # define box and volume for resistive plate (maybe the same volume for anode and cathode?)
        resiplate = geom.shapes.Box( 'ResistivePlate',
                                     dx = 0.5*self.resiplateDim[0],
                                     dy = 0.5*self.resiplateDim[1],
                                     dz = 0.5*self.resiplateDim[2])
        resiplate_lv = geom.structure.Volume('volResistivePlate', material=self.resiplateMat, shape=resiplate)
        # define box and volume for gas in rpc
        rpcGas = geom.shapes.Box( 'RPCGas',
                                  dx = 0.5*self.resiplateDim[0],
                                  dy = 0.5*self.resiplateDim[1],
                                  dz = 0.5*self.gas_gap)
        rpcGas_lv = geom.structure.Volume('volRPCGas', material=self.gasMat, shape=rpcGas)

        # position and place resistive plates in RPCMod
        #pRP_in_Module = geom.structure.Placement( 'placeRP_in_'+self.name, volume = resiplate_lv )
        pG_in_Module  = geom.structure.Placement( 'placeG_in_'+self.name, volume = rpcGas_lv )
        #rpcMod_lv.placements.append( pRP_in_Module.name )
        rpcMod_lv.placements.append( pG_in_Module.name )
        self.add_volume(rpcMod_lv)