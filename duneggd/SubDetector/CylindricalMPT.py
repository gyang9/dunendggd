#!/usr/bin/env python
'''
CylindricalMPTBuilder: Builds the multi purpose tracker
'''

import gegede.builder
from gegede import Quantity as Q

class CylindricalMPTBuilder(gegede.builder.Builder):
    '''
    Build a cylindrical multipurpose tracker. This class directly
    builds the magnet yoke and ECAL (for now) but calls a subbuilder 
    for the GArTPC.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, yokeMaterial = 'Iron',
                  yokeInnerR=Q("3.0m"), yokeInnerZ=Q("3.0m"),
                  yokeThicknessR=Q("0.5m"),yokeThicknessZ=Q("0.5m"),
                  yokeBufferToBoundaryR=Q("0.5m"),
                  yokeBufferToBoundaryZ=Q("0.5m"),
                  yokePhiCutout=Q("90deg"),
                  innerBField=None,
                  GArTPCPos=None, GArTPCRot=None,
                  buildGArTPC=False,**kwds):
        '''
        
        Arguments:
        yokeMaterial: what the yoke is made of
        yokePosition: location of the center of the yoke in the mother volume
        (usually 0,0,0)
        yokeInnerR: Inner radius of the cylindrical magnet yoke
        
        yokeInnerZ: Half length of the cylindrical magnet yoke
        measured to inner surface

        yokeThicknessR,Z: Thickness of the magnet yoke
        
        yokeBufferToBoundaryR,Z: buffer between the outer edge 
        of the magnet and the rectangular mother volume
        
        innerBField: the magnetic field inside of the magnet
        
        '''
        # magnet configuration
        self.yokeMaterial      = yokeMaterial
        self.yokeInnerR = yokeInnerR
        self.yokeInnerZ = yokeInnerZ
        self.yokeThicknessR=yokeThicknessR
        self.yokeThicknessZ=yokeThicknessZ
        self.yokeBufferToBoundaryR=yokeBufferToBoundaryR
        self.yokeBufferToBoundaryZ=yokeBufferToBoundaryZ
        self.yokePhiCutout=yokePhiCutout
        self.innerBField = innerBField
#        self.MagnetBldr   = self.get_builder('Magnet')

        # GArTPC configuration
        # only get a GArTPC builder if we want to build the GArTPC
        self.GArTPCBldr = None
        if buildGArTPC:
            self.GArTPCBldr=self.get_builder('GArTPC')
        self.GArTPCPos=GArTPCPos
        self.GArTPCRot=GArTPCRot
        self.buildGArTPC=buildGArTPC

        return
    
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        
        ############# build the top level lv ###################
        # it's just a box to hold everything else
        # the z axis of a cylinder is the symmetry axis, but definition
        # for this box it corresponds to x
        dx_main=self.yokeInnerZ+self.yokeThicknessZ+self.yokeBufferToBoundaryZ
        dy_main=self.yokeInnerR+self.yokeThicknessR+self.yokeBufferToBoundaryR
        dz_main=dy_main
        main_shape = geom.shapes.Box('CylindricalMPT',
                                     dx=dx_main, dy=dy_main, dz=dz_main)
        
        main_lv = geom.structure.Volume('vol'+self.name,
                                        material='Air', shape=main_shape)
        self.add_volume(main_lv)

        ######### magnet yoke ##################################
        ### build the magnet yoke and coils and place inside the main lv
        self.build_yoke(main_lv,geom)

        ######### build an outer ecal ##########################

        ######### build the cryostat  ##########################

        ######### build an inner ecal ##########################

        ######### build the TPC       ##########################
        # use GArTPCBuilder, but "disable" the cyrostat by tweaking
        # EndcapThickness, WallThickness, and ChamberMaterial
        return
        

    def build_yoke(self,main_lv,geom):

        #### build the barrel ####
        rmin=self.yokeInnerR
        rmax=rmin+self.yokeThicknessR
        dz=self.yokeInnerZ
        sphi=self.yokePhiCutout/2.0
        dphi=Q("360deg")-self.yokePhiCutout
        by_name="MPTYokeBarrel"
        by_shape = geom.shapes.Tubs(by_name,
                                    rmin=rmin,rmax=rmax,dz=dz,
                                    sphi=sphi,dphi=dphi)
        by_lv=geom.structure.Volume(by_name+"_lv",
                                    material=self.yokeMaterial,
                                    shape=by_shape)
        pos=[Q('0m'),Q('0m'),Q('0m')]
        by_pos=geom.structure.Position(by_name+"_pos",pos[0],pos[1],pos[2])
        rot=[Q("0deg"),Q("-90deg"),Q("0deg")]
        by_rot=geom.structure.Rotation(by_name+"_rot",rot[0],rot[1],rot[2])
        by_pla=geom.structure.Placement(by_name+"_pla",volume=by_lv,
                                        pos=by_pos, rot=by_rot)
        main_lv.placements.append(by_pla.name)

        ### build the endcaps ###
        part="A" # eventually may add a multipart endcap (A, B, C... like KLOE)
        for side in ["L","R"] :
            name="YokeEndcap"+part+side
            ec_shape=geom.shapes.Tubs(name,
                                      rmin=Q("0.5m"),
                                      rmax=self.yokeInnerR+self.yokeThicknessR,
                                      dz=self.yokeThicknessZ/2.0)
            ec_lv=geom.structure.Volume(name+"_vol",
                                        material=self.yokeMaterial,
                                        shape=ec_shape)
            pos=[Q('0m'),Q('0m'),Q('0m')]
            pos[0]=self.yokeInnerZ+self.yokeThicknessZ/2.0
            if side=="L":
                pos[0]=-pos[0]

            ec_pos=geom.structure.Position(name+"_pos",pos[0],pos[1],pos[2])
            rot=[Q("0deg"),Q("-90deg"),Q("0deg")]
            ec_rot=geom.structure.Rotation(name+"_rot",rot[0],rot[1],rot[2])
            ec_pla=geom.structure.Placement(name+"_pla",volume=ec_lv,
                                            pos=ec_pos, rot=ec_rot)
            main_lv.placements.append(ec_pla.name)
        
        return



    
