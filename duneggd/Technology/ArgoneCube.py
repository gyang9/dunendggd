#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class ArgoneCubeBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfActDimension=None, IsolationThickness=Q('60cm'),
                        StructureThickness=Q('40cm'), Sensitive=None,
                        Material=None, **kwds ):

        self.halfActDimension = halfActDimension
        self.halfVolDimension = {   'dx':halfActDimension['dx'],
                                    'dy':halfActDimension['dy']*100/90,
                                    'dz':halfActDimension['dz'] }
        self.halfModDimension = {   'dx':halfVolDimension['dx'],
                                    'dy':halfVolDimension['dy']*100/75,
                                    'dz':halfVolDimension['dz'] }
        self.halfTopDimension = {   'dx':halfModDimension['dx'],
                                    'dy':halfModDimension['dy']*15/100,
                                    'dz':halfModDimension['dz'] }
        self.halfBotDimension = {   'dx':halfModDimension['dx'],
                                    'dy':halfModDimension['dy']*10/100,
                                    'dz':halfModDimension['dz'] }
        self.StructureThickness = StructureThickness
        self.Sensitive = Sensitive
        self.Sensitive, self.Material = Sensitive, Material

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
