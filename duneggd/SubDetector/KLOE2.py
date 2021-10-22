#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q

class KLOEBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                  halfDimension=None,
                  Material=None,
                  BField=None,
                  CentralBField=Q("0.0T"),
                  BuildSTT=False,
                  BuildGAR=False,
                  Build3DST=False,
                  BuildSTTFULL=False,
                  Build3DSTwithSTT=False,
                  STTRotations=None,
                  **kwds):
        del BField
        self.halfDimension = halfDimension
        self.Material      = Material
        self.BuildSTT      = BuildSTT
        self.BuildGAR      = BuildGAR
        self.Build3DST     = Build3DST
        self.BuildSTTFULL  = BuildSTTFULL
        self.Build3DSTwithSTT = Build3DSTwithSTT
        # The overall logical volume
        self.LVHalfLength=Q("3.1m")
        self.LVRadius=Q("3.6m")
        self.LVMaterial="Air"
        # the CentralBField is really the only configurable parameter
        # since KLOE is already built
        self.CentralBField=CentralBField
        self.SolenoidCoilShellRmin=Q("2.59m")
        # barrel yoke
        self.BarrelHalfLength=Q("2.15m")
        self.BarrelRmax=Q("3.30m")
        self.BarrelRmin=Q("2.93m")
        self.BarrelMaterial="Iron"
        # endcap yoke
        ## endcap B field will be a function of radius...
        # part A is a TUBS  2.58<|x|<2.99m, rmin=.96m, rmax=3.07m
        self.EndcapAZStart=Q("2.58m")
        self.EndcapAZEnd=Q("2.99m")
        self.EndcapARmax=Q("3.07m")
        self.EndcapARmin=Q("0.96m")
        
        # part B is a TUBS, 2.15<|x|<2.58m, rmin=2.78m, rmax=3.30m
        self.EndcapBZStart=Q("2.15m")
        self.EndcapBZEnd=Q("2.58m")
        self.EndcapBRmax=Q("3.30m")
        self.EndcapBRmin=Q("2.78m")

        # part C is a TUBS, 2.15<|x|<2.58m, rmin=0.84m, rmax=1.34m
        self.EndcapCZStart=Q("2.15m")
        self.EndcapCZEnd=Q("2.58m")
        self.EndcapCRmax=Q("1.34m")
        self.EndcapCRmin=Q("0.84m")

        # part D is a TUBS, 1.96<|x|<2.15m, rmin=0.512m, rmax=1.73m
        self.EndcapDZStart=Q("1.96m")
        self.EndcapDZEnd=Q("2.15m")
        self.EndcapDRmax=Q("1.73m")
        self.EndcapDRmin=Q("0.51m")

        self.STTRotations=STTRotations
        
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        print( "KLOEBuilder::construct()")
        print( "main_lv = "+ main_lv.name)
        self.add_volume( main_lv )
        self.build_yoke(main_lv, geom)
        self.build_solenoid(main_lv, geom)
        self.build_ecal(main_lv,geom)
        #self.build_muon_system(main_lv,geom)
        
        if(self.BuildGAR is True) or (self.BuildSTT is True):
            self.build_tracker(main_lv, geom)
        if(self.BuildSTTFULL is True):
            self.build_sttfull(main_lv,geom)
        if(self.Build3DST is True):
            self.build_3DST(main_lv, geom)
        if(self.Build3DSTwithSTT is True):
            self.build_3DSTwithSTT(main_lv, geom)

        print("printing main_lv: " + str(main_lv))
            
            
#        TranspV = [0,0,1]
#        begingap = ltools.getBeginGap( self )

        # initial position, based on the dimension projected on transportation vector

#        pos = [Q('0m'),Q('0m'),-main_hDim[2]]
#        pos = [Q('0m'),Q('0m'),Q('0m')]
#        rot = [Q('0deg'),Q('90deg'),Q('0deg')]
#        main_lv = main_lv.get_Volume()
#        main_pos = gemo.structure.Poition( main_lv.name_pos, Pos[0], Pos[1], Pos[2] )
#        main_rot = geom.structure.Rotation( main_lv.name_rot, Rot[0], Rot[1], Rot[2] )
#        main_pla = geom.structure.Placement (main_lv.name_pla, volume=main_lv, pos=main_pos, rot=main_rot )
#        main_lv.placements.append( main_pla.name )

#        print( "KLOE subbuilders")
#        for i,sb in enumerate(self.get_builders()):
#            sb_lv = sb.get_volume()
#            print( "Working on ", i, sb_lv.name)
#            sb_dim = ltools.getShapeDimensions( sb_lv, geom )

#            pos[2] = pos[2] + sb_dim[2] + self.InsideGap[i]
            # defining position, placement, and finally insert into main logic volume.
#            pos_name=self.name+sb_lv.name+'_pos_'+str(i)
#            pla_name=self.name+sb_lv.name+'_pla_'+str(i)
#            print( "Position name", pos_name)
#            print( "Placement name", pla_name)
#            sb_pos = geom.structure.Position(pos_name,pos[0], pos[1], pos[2])
#            sb_pla = geom.structure.Placement(pla_name,volume=sb_lv, pos=sb_pos)
#            print( "Appending ",sb_pla.name," to main_lv=",main_lv.name)
#            main_lv.placements.append(sb_pla.name)
    
    def build_yoke(self,main_lv,geom):
        
        #build barrel
        barrel_shape=geom.shapes.Tubs('KLOEYokeBarrel', 
                                      rmin=self.BarrelRmin, 
                                      rmax=self.BarrelRmax, 
                                      dz=self.BarrelHalfLength)
        barrel_lv=geom.structure.Volume('KLOEYokeBarrel_volume', 
                                        material=self.BarrelMaterial, 
                                        shape=barrel_shape)
        ## set magnitude of BarrelBField based on conserved B.dA
        BarrelBField=self.CentralBField*self.SolenoidCoilShellRmin**2/(self.BarrelRmax**2 - self.BarrelRmin**2)
        
#        BField="(0.0 T, 0.0 T, %f T)"%(-BarrelBField/Q("1.0T"))
        BField="(%f T, 0.0 T, 0.0 T)"%(-BarrelBField/Q("1.0T"))
        print( "Setting KLOE Barrel Bfield to "+str(BField))
        barrel_lv.params.append(("BField",BField))


        pos = [Q('0m'),Q('0m'),Q('0m')]
        barrel_pos=geom.structure.Position("KLOEYokeBarrel_pos",
                                           pos[0],pos[1], pos[2])
        barrel_pla=geom.structure.Placement("KLOEYokeBarrel_pla",
                                            volume=barrel_lv,
                                            pos=barrel_pos)
        print( "appending "+barrel_pla.name)
        main_lv.placements.append(barrel_pla.name)
        
        # build endcap
        partv=['A','B','C','D']

        zstartv=[self.EndcapAZStart,self.EndcapBZStart,self.EndcapCZStart,self.EndcapDZStart]
        zendv=[self.EndcapAZEnd,self.EndcapBZEnd,self.EndcapCZEnd,self.EndcapDZEnd]
        rmaxv=[self.EndcapARmax,self.EndcapBRmax,self.EndcapCRmax,self.EndcapDRmax]
        rminv=[self.EndcapARmin,self.EndcapBRmin,self.EndcapCRmin,self.EndcapDRmin]
        for zstart,zend,rmax,rmin,part in zip(zstartv,zendv,rmaxv,rminv,partv):
            name='KLOEYokeEndcap'+part
            for side in ['L','R']:
                name='KLOEYokeEndcap'+part+side
                hl=(zend-zstart)/2.0
                ec_shape=geom.shapes.Tubs(name, 
                                          rmin=rmin, 
                                          rmax=rmax, 
                                          dz=hl)
                ec_lv=geom.structure.Volume(name+'_volume', 
                                            material=self.BarrelMaterial, 
                                            shape=ec_shape)
                pos = [Q('0m'),Q('0m'),Q('0m')]
                pos[2]=(zstart+zend)/2.0
                if side=='L':
                    pos[2]=-pos[2]
                ec_pos=geom.structure.Position(name+"_pos",
                                               pos[0],pos[1], pos[2])
                ec_pla=geom.structure.Placement(name+"_pla",
                                                volume=ec_lv,
                                                pos=ec_pos)
                print( "appending "+ec_pla.name)
                main_lv.placements.append(ec_pla.name)

        

    def build_solenoid(self,main_lv,geom):
        # K.D. Smith, et al., 
        # IEEE Transactions on Applied Superconductivity, v7, n2, June 1997
        # the solenoid has the following major parts
        # cryostat endcaps
        # outer cryostat wall
        # inner crostat wall
        # inner and outer radiation screens
        # coil shell
        # coil

        #self.SolenoidHalfLength=Q("2.15m")
        #self.SolenoidRmin=Q("2.44m") # cryostat inner wall
        #self.SolenoidRmax=Q("2.85m") # cryostat outer wall
        #self.SolenoidRcen=Q("2.60m") # location of the coil's center

        SolenoidHL=Q("2.15m") # halflength of solenoid to outer edge of cryostat        
        # cryostat endcaps
        # rmin=2.43m, rmax=2.88m, thickness=40mm, xcenter=2.15m-40mm/2
        SolenoidECRmin=Q("2.43m")
        SolenoidECRmax=Q("2.88m")
        SolenoidECDz=Q("40mm")
        SolenoidECZloc=SolenoidHL-SolenoidECDz/2.0
        SolenoidECMaterial='Aluminum'

        for side in ['L','R']:
            name='KLOESolenoidCryostatEndcap'+side
            ec_shape=geom.shapes.Tubs(name, 
                                      rmin=SolenoidECRmin, 
                                      rmax=SolenoidECRmax, 
                                      dz=SolenoidECDz/2.0)
            ec_lv=geom.structure.Volume(name+'_volume', 
                                        material=SolenoidECMaterial, 
                                        shape=ec_shape)
            pos = [Q('0m'),Q('0m'),Q('0m')]
            pos[2]=SolenoidECZloc
            if side=='L':
                pos[2]=-pos[2]
            ec_pos=geom.structure.Position(name+"_pos",
                                           pos[0],pos[1], pos[2])
            ec_pla=geom.structure.Placement(name+"_pla",
                                            volume=ec_lv,
                                            pos=ec_pos)        
            print( "appending "+ec_pla.name)
            main_lv.placements.append(ec_pla.name)

        # cryostat inner and outer walls
        SolenoidCryostatRmax=SolenoidECRmax
        SolenoidCryostatRmin=SolenoidECRmin
        SolenoidCryostatHL=SolenoidECZloc=SolenoidHL-SolenoidECDz
        SolenoidCryostatDz=Q("12mm")+Q("3mm") # include radiation screen in wall
        for wall in ['Inner','Outer']:
            name='KLOESolenoidCryostat'+wall+'Wall'
            
            rmax=SolenoidCryostatRmax
            rmin=rmax-SolenoidCryostatDz
            if wall=='Inner':
                rmin=SolenoidCryostatRmin
                rmax=rmin+SolenoidCryostatDz
            hl=SolenoidCryostatHL
            shape=geom.shapes.Tubs(name, 
                                      rmin=rmin, 
                                      rmax=rmax, 
                                      dz=hl)
            lv=geom.structure.Volume(name+'_volume', 
                                        material=SolenoidECMaterial, 
                                        shape=shape)
            pos = [Q('0m'),Q('0m'),Q('0m')]

            pos=geom.structure.Position(name+"_pos",
                                           pos[0],pos[1], pos[2])
            pla=geom.structure.Placement(name+"_pla",
                                            volume=lv,
                                            pos=pos)        
            print( "appending "+pla.name)
            main_lv.placements.append(pla.name)
            

        # coil shell
        
        SolenoidCoilShellRmin=self.SolenoidCoilShellRmin
        SolenoidCoilShellDz=Q("10mm")+Q("1mm") # 1mm Al layer between two coil layers included here
        name='KLOESolenoidCoilShell'

        rmin=SolenoidCoilShellRmin        
        rmax=rmin+SolenoidCoilShellDz

        hl=SolenoidCryostatHL-Q("1cm") # make it a little shorter than the cryostat, 1cm is a wild guess
        shape=geom.shapes.Tubs(name, 
                               rmin=rmin, 
                               rmax=rmax, 
                               dz=hl)
        lv=geom.structure.Volume(name+'_volume', 
                                material=SolenoidECMaterial, 
                                 shape=shape)
        pos = [Q('0m'),Q('0m'),Q('0m')]
        
        pos=geom.structure.Position(name+"_pos",
                                    pos[0],pos[1], pos[2])
        pla=geom.structure.Placement(name+"_pla",
                                     volume=lv,
                                     pos=pos)        
        print( "appending "+pla.name)
        main_lv.placements.append(pla.name)
        
        
        #the coil itself
        SolenoidCoilRmin=SolenoidCoilShellRmin+SolenoidCoilShellDz
        SolenoidCoilDz=Q("10mm") # 1mm Al layer between two coil layers included here
        SolenoidCoilMaterial='Copper' # of course it's some mix, maybe not even including copper. This is a placeholder.
        name='KLOESolenoidCoil'

        rmin=SolenoidCoilRmin        
        rmax=rmin+SolenoidCoilDz

        hl=SolenoidCryostatHL-Q("1cm") # make it a little shorter than the cryostat, 1cm is a wild guess
        shape=geom.shapes.Tubs(name, 
                               rmin=rmin, 
                               rmax=rmax, 
                               dz=hl)
        lv=geom.structure.Volume(name+'_volume', 
                                material=SolenoidCoilMaterial, 
                                 shape=shape)
        pos = [Q('0m'),Q('0m'),Q('0m')]
        
        pos=geom.structure.Position(name+"_pos",
                                    pos[0],pos[1], pos[2])
        pla=geom.structure.Placement(name+"_pla",
                                     volume=lv,
                                     pos=pos)        
        print( "appending "+pla.name)
        main_lv.placements.append(pla.name)
        
    def build_ecal(self, main_lv, geom):
        
        if (self.builders.has_key("KLOEEMCALO") is False):
            print "KLOEEMCALO builder not found"
            return            

        emcalo_builder=self.get_builder("KLOEEMCALO")
        emcalo_lv=emcalo_builder.get_volume()
        
        emcalo_position = geom.structure.Position(
                'emcalo_position', Q('0m'), Q('0m'), Q('0m'))

        emcalo_rotation = geom.structure.Rotation(
                'emcalo_rotation', Q('0deg'), Q('0deg'), Q('7.5deg'))

        emcalo_placement = geom.structure.Placement('emcalo_place',
                                                  volume=emcalo_lv,
                                                  pos=emcalo_position,
                                                  rot=emcalo_rotation)
        main_lv.placements.append(emcalo_placement.name)
        
    def build_3DST(self, main_lv, geom):
        if (self.builders.has_key("3DST") is False):
            print("3DST have not been requested.")
            print("Therefore we will not build 3DST.")
            return
        else:
            a3dst_builder = self.get_builder("3DST")
            if (a3dst_builder != None):
                pos = [Q('0m'), Q('0m'), Q('0m')]
                a3dst_lv = a3dst_builder.get_volume()
                print("Working on ", a3dst_lv.name)
                pos_name = self.name + a3dst_lv.name + '_pos'
                pla_name = self.name + a3dst_lv.name + '_pla'
                print("Position name", pos_name)
                print("Placement name", pla_name)
                sb_pos = geom.structure.Position(pos_name, pos[0], pos[1], pos[2])
                sb_pla = geom.structure.Placement(pla_name,volume=a3dst_lv,
					          pos=sb_pos)
                print("Appending ", sb_pla.name, " to main_lv=", main_lv.name)
                main_lv.placements.append(sb_pla.name)

    def build_sttfull(self, main_lv, geom):
        if (self.builders.has_key("STTFULL") is False):
            print("STTFULL have not been requested.")
            print("Therefore we will not build  STTFULL")
            return
        else:
            stt_builder = self.get_builder("STTFULL")
            if (stt_builder != None):
                stt_lv = stt_builder.get_volume()
                #                stt_rot= geom.structure.Rotation("rot_stttracker", self.STTRotations[0], self.STTRotations[1], self.STTRotations[2])
                stt_rot= geom.structure.Rotation("rot_stttracker", Q('0deg'), Q('0deg'), Q('7.5deg'))
                stt_pla = geom.structure.Placement("KLOESTTFULL_pla",
                                                   volume=stt_lv, rot=stt_rot)
                main_lv.placements.append(stt_pla.name)

    def build_3DSTwithSTT(self,main_lv, geom):
        if self.builders.has_key("3DST_STT")==False:
            print "3DST_STT doesnot exist, return"
            return
        threeDSTwithSTT_builder=self.get_builder("3DST_STT")
        threeDSTwithSTT_lv=threeDSTwithSTT_builder.get_volume()
        threeDSTwithSTT_pla = geom.structure.Placement('threeDSTwithSTT_pla',
                                                  volume=threeDSTwithSTT_lv)
        main_lv.placements.append(threeDSTwithSTT_pla.name)
        


    def build_tracker(self,main_lv,geom):
        # only build the tracker if we are
        # also building the STT or GArTPC
        # 3DST works differently
        if self.builders.has_key("KLOEGAR")==False and self.builders.has_key("KLOESTT")==False :
            print "KLOEGAR and KLOESTT have not been requested."
            print "Therefore we will not build the tracking region."
            return 

        
        # this is where we will use subbuilders
        name="KLOETrackingRegion"
        KLOETrackingRegionRmin=Q("0m")
        KLOETrackingRegionRmax=Q("2.0m")
        KLOETrackingRegionHL=Q("1.69m")

        # build tracking region logical volume        
        shape=geom.shapes.Tubs(name, 
                               rmin=KLOETrackingRegionRmin, 
                               rmax=KLOETrackingRegionRmax,
                               dz=KLOETrackingRegionHL)
        lv=geom.structure.Volume(name+'_volume', 
                                 material='Air', 
                                 shape=shape)


#        BField="(0.0 T, 0.0 T, %f T)"%(self.CentralBField/Q("1.0T"))
        BField="(%f T, 0.0 T, 0.0 T)"%(self.CentralBField/Q("1.0T"))
        print( "Setting KLOE Central Tracker Bfield to "+str(BField))
        lv.params.append(("BField",BField))
        
        
        # now build the STT inside
        if self.builders.has_key("KLOESTT"):
            print "we have a KLOESTT builder key"
            stt_builder=self.get_builder("KLOESTT")
            print "self.BuildSTT==",self.BuildSTT
            print "stt_builder: ",stt_builder
            if (stt_builder!=None):
                rot = [Q("0deg"),Q("90deg"),Q("0deg")]
                loc = [Q('0m'),Q('0m'),Q('0m')]
                stt_lv=stt_builder.get_volume()
                stt_pos=geom.structure.Position(name+"_KLOESTT_pos",
                                                loc[0],loc[1],loc[2])
                stt_rot=geom.structure.Rotation(name+"_KLOESTT_rot",
                                                rot[0],rot[1],rot[2])
                stt_pla=geom.structure.Placement(name+"_KLOESTT_pla",
                                                 volume=stt_lv,pos=stt_pos,
                                                 rot=stt_rot)
                lv.placements.append(stt_pla.name)
        
        # or, build the GArTPC
        if self.builders.has_key("KLOEGAR"):
            print "we have a KLOEGAR builder key"
            gar_builder=self.get_builder("KLOEGAR")
            print "self.BuildGAR==",self.BuildGAR
            print "gar_builder: ",gar_builder
            if (gar_builder!=None) and (self.BuildGAR==True):
                rot = [Q("0deg"),Q("0deg"),Q("0deg")]
                loc = [Q('0m'),Q('0m'),Q('0m')]
                gar_lv=gar_builder.get_volume()
                gar_pos=geom.structure.Position(name+"_KLOEGAR_pos",
                                                loc[0],loc[1],loc[2])
                gar_rot=geom.structure.Rotation(name+"_KLOEGAR_rot",
                                                rot[0],rot[1],rot[2])
                gar_pla=geom.structure.Placement(name+"_KLOEGAR_pla",
                                                 volume=gar_lv,pos=gar_pos,
                                                 rot=gar_rot)
                lv.placements.append(gar_pla.name)
        


        # now place the tracking volume
        pos = [Q('0m'),Q('0m'),Q('0m')]
        pos=geom.structure.Position(name+"_pos",
                                    pos[0],pos[1], pos[2])
        pla=geom.structure.Placement(name+"_pla",
                                     volume=lv,
                                     pos=pos)
        print( "appending "+pla.name)

        main_lv.placements.append(pla.name)


            
    #def build_muon_system(self,main_lv,geom):
    #    pass


