#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time as tm

class STTLARBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, **kwds ):
        sqrt3                    = 1.7320508
        self.halfDimension, self.Material = ( halfDimension, Material )
        
        # ST
        self.strawRadius         = Q('2.5mm')
        self.coatThickness       = Q("70nm")
        self.mylarThickness      = Q("20um")
        self.strawWireWThickness = Q('20um')
        self.strawWireGThickness = Q('20nm')
        
        # XY STT planes
        self.planeXXThickness    = self.strawRadius * (2 + sqrt3) #=9.33mm half of XXYY plane thickness
        
        # STT MODULE 
        self.nfoil               = 119
        self.foilThickness       = Q("18um")
        self.foilGap             = Q("117um")
        self.totFoilsThickness   = self.nfoil * self.foilThickness + (self.nfoil-1)*self.foilGap
        self.slabThickness       = Q("5.0mm")
        self.graphiteThickness   = Q("4mm") 
        
        # STT
        self.kloeVesselHalfDx    = Q('1.69m')
        self.kloeVesselRadius    = Q('2m')
        self.extLateralgap       = Q("0cm")
        self.extRadialgap        = Q("0cm")
        self.kloeTrkRegRadius    = self.kloeVesselRadius - self.extRadialgap
        self.kloeTrkRegHalfDx    = self.kloeVesselHalfDx - self.extLateralgap
        self.C3H6ModThickness    = self.planeXXThickness * 2 + self.totFoilsThickness + self.slabThickness # complete thickness
        self.CModThickness       = self.planeXXThickness * 2 + self.graphiteThickness  #9,33cm*2 + 0,4 = 3.7 cm complete thickness
        
        self.TrModLatGap         = Q('4.67mm') ##introduced
        self.TrModThickness      = self.planeXXThickness * 3 + self.TrModLatGap * 2 #=37.33 mm complete thickness
        
        # LAr target
        self.BoxThickness        = Q("12mm")
        
        self.ExternalVesselX     = Q("297mm") #minor semiaxis of external vessel
        self.ExternalVesselY     = Q("788.5mm") #major semiaxis of external vessel
        self.ExternalVesselZ     = Q("740mm") #half lenght of external vessel
        
        self.VesselRelativeZPos  = Q("50mm")
        
        self.InternalVesselX     = Q("237.5mm")#minor semiaxis of internal vessel
        self.InternalVesselY     = Q("728mm") #major semiaxis of internal vessel
        self.InternalVesselZ     = Q("500mm") #half lenght of internal vessel
        
        self.VacuumThickness     = Q("200mm") #thickness of empty between the two vessels
        self.UpstreamVesselGap   = Q("8cm") #margin between kloe vessel and the LAr target
        self.MinDistExtVesTrMod  = Q("15cm") #margin between LAr target and upstream traking module
        self.InterVesselHalfGap  = Q('30mm')
        
        self.DownstreamTrMod     = Q("20cm")
        self.DownNTrMod          = 4
        self.NC3H6Packet         = 12
        self.NCPacket            = 1
        pass

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct STT 
    def construct(self,geom):
        start_time=tm.time()
                
        main_lv, main_hDim = ltools.main_lv(self, geom, "Tubs")
        print( "KLOESTTFULL::construct()")
        print( "  main_lv = "+ main_lv.name)
        self.add_volume( main_lv )
       
#------ Building 2 LAr targets in the upstram part of kloe ad distance self.UpstreamVesselGap from the barrels

        self.construct_LAr_Target(geom, main_lv)

#------ Counting number of modules to be built

        # upstream: at the certer of kloe there is a carbon module and after the cryostat, at least 15 cm away from it, 1 traking module
        
        up_avail_space = self.kloeTrkRegRadius - self.ExternalVesselX*2 - self.MinDistExtVesTrMod - self.UpstreamVesselGap - 0.5 * self.CModThickness - self.TrModThickness

        packet_Thickness = self.CModThickness * self.NCPacket + self.C3H6ModThickness * self.NC3H6Packet 
        packet_Thickness.ito(up_avail_space.units) 
        
        up_n_packets = int((up_avail_space/packet_Thickness).magnitude)
        
        up_remain_space = up_avail_space - up_n_packets * packet_Thickness
        up_remain_space.ito(self.C3H6ModThickness.units) 
        
        up_nC3H6Mod = int((up_remain_space/self.C3H6ModThickness).magnitude) # first modules of C3H6 after the upstream traking module
        
        start_Xpos = - (up_n_packets * packet_Thickness + up_nC3H6Mod * self.C3H6ModThickness + 0.5 * self.CModThickness + self.TrModThickness)

        #downstream: the last C3H6 module far from the wall at least 20 cm and after it 4 traking modules
        
        dw_avail_space = self.kloeTrkRegRadius - self.DownstreamTrMod - 0.5 * self.CModThickness
        packet_Thickness.ito(dw_avail_space.units) 
        
        dw_n_packets = int((dw_avail_space/packet_Thickness).magnitude)
        
        dw_remain_space = dw_avail_space - dw_n_packets * packet_Thickness
        dw_remain_space.ito(self.C3H6ModThickness.units) 
        
        dw_nC3H6Mod = int((dw_remain_space/self.C3H6ModThickness).magnitude)

        n_packets = up_n_packets + dw_n_packets
        
#        print("dw_avail_space :"+str(dw_avail_space)+", packet_Thickness :"+str(packet_Thickness))
#        print("upstream modules: "+str(up_nC3H6Mod)+", downstram modules: "+str(dw_nC3H6Mod))

#------ Building STT modules
        
        module_types = {'TrMod': {'constructor': self.construct_tracking_module, 'thickness':self.TrModThickness},
                        'C3H6Mod': {'constructor': self.construct_C3H6_Module, 'thickness':self.C3H6ModThickness},
                        'CMod': {'constructor': self.construct_C_Module, 'thickness':self.CModThickness}} 

        # 1 Traking module upstream
        
        Tr_count = 0
        mod_name = "_TrMod_" + str(Tr_count)
        Xpos = self.construct_STT(geom, mod_name, start_Xpos, module_types['TrMod'], main_lv)
        
        # first C3H6 modules after the traking modules:
        
        for i in range(up_nC3H6Mod):
            
            Tr_count += 1
            mod_name = "_C3H6Mod_" + str(Tr_count)
            Xpos = self.construct_STT(geom, mod_name, Xpos, module_types['C3H6Mod'], main_lv)
        
        Tr_count += 1
        mod_name = "_CMod_" + str(Tr_count)
        Xpos = self.construct_STT(geom, mod_name, Xpos, module_types['CMod'], main_lv)
        
        # set of 12 C3H6 + 1 C
        
        for i in range(n_packets):
        
            for n in range(self.NC3H6Packet):
            
                Tr_count += 1
                mod_name = "_C3H6Mod_" + str(Tr_count)
                Xpos = self.construct_STT(geom, mod_name, Xpos, module_types['C3H6Mod'], main_lv)
                 
            for n in range(self.NCPacket):

                Tr_count += 1
                mod_name = "_CMod_" + str(Tr_count)
                Xpos = self.construct_STT(geom, mod_name, Xpos, module_types['CMod'], main_lv)
            
        # end C3H6 modules
        
        for i in range(dw_nC3H6Mod):
            
            Tr_count += 1
            mod_name = "_C3H6Mod_" + str(Tr_count)
            Xpos = self.construct_STT(geom, mod_name, Xpos, module_types['C3H6Mod'], main_lv)
        
        #  downstream traking modules
        
        for i in range(self.DownNTrMod):
        
            Tr_count += 1
            mod_name = "_TrMod_" + str(Tr_count)
            Xpos = self.construct_STT(geom, mod_name, Xpos, module_types['TrMod'], main_lv) 

        print('Xpos: ' + str(Xpos)) 
        
#---------------------------------------------------------------------------------------------------------------------------------------

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct_STT(self, geom, name, X, module_type, volume): 
    
        thickness = module_type['thickness']

        if X < Q('0mm'):
        
            cos = X / self.kloeTrkRegRadius
        
        else:
        
            cos = (X + thickness) / self.kloeTrkRegRadius
        
        module_halfHeight = self.kloeTrkRegRadius*math.sqrt(1 - cos*cos)
        module_halfDimension = {'dx' : 0.5*thickness, 'dy' : module_halfHeight, 'dz' : self.kloeTrkRegHalfDx}
        module_lv = module_type['constructor'](geom, name, module_halfDimension)
        
        module_pos = geom.structure.Position(name + "_pos", X + 0.5*thickness, Q('0mm'), Q('0mm'))
        module_pla = geom.structure.Placement(name + "_pla", volume = module_lv, pos = module_pos)
        volume.placements.append(module_pla.name)

        return X + thickness
    
    # construct LAr Vessel
    def construct_LAr_Vessel(self, geom):
        #building the outermost layer of either aluminium or carbon fiber
        
        Gr_ext_shape = geom.shapes.EllipticalTube("Gr_ext_shape", 
                                         dx=self.ExternalVesselX, 
                                         dy=self.ExternalVesselY, 
                                         dz=self.ExternalVesselZ)

        Gr_ext_lv = geom.structure.Volume("Gr_ext_lv", 
                                          material="Carbon_fiber", 
                                          shape=Gr_ext_shape)

        #building the layer of empty (for the moment there is air in there)                                       
        Empty_tgt_shape = geom.shapes.EllipticalTube("Empty_tgt_shape", 
                                         dx=self.ExternalVesselX-self.BoxThickness, 
                                         dy=self.ExternalVesselY-self.BoxThickness, 
                                         dz=self.ExternalVesselZ-self.BoxThickness - Q("4mm")) #endcap thickness of the external vessel is 16 mm

        Empty_tgt_lv = geom.structure.Volume("Empty_tgt_lv", 
                                           material="Vacuum_cryo", #to be change with empty
                                           shape=Empty_tgt_shape)
        
        Empty_tgt_pla = geom.structure.Placement("Empty_tgt_pla", 
                                                 volume=Empty_tgt_lv)

        Gr_ext_lv.placements.append(Empty_tgt_pla.name)
        
        #building the internal vessel
        
        Al_int_shape = geom.shapes.EllipticalTube("Al_int_shape", 
                                         dx=self.InternalVesselX, 
                                         dy=self.InternalVesselY, 
                                         dz=self.InternalVesselZ) #self.ExternalVesselZ-self.BoxThickness-self.VacuumThickness) 
       
        Al_int_lv = geom.structure.Volume("Al_int_lv", 
                                          material="Aluminum", 
                                          shape=Al_int_shape)
                                          
        relative_pos = geom.structure.Position("relative_pos",
                                      Q('0mm'),
                                      Q('0mm'),
                                      self.VesselRelativeZPos)
        
        Al_int_pla = geom.structure.Placement("Al_int_pla", 
                                              volume=Al_int_lv,
                                              pos=relative_pos)
        
        Empty_tgt_lv.placements.append(Al_int_pla.name)
        
        #building the bulk of the target made by liquid argon
        Lar_bulk_shape = geom.shapes.EllipticalTube("Lar_bulk_shape", 
                                         dx=self.InternalVesselX-self.BoxThickness, 
                                         dy=self.InternalVesselY-self.BoxThickness, 
                                         dz=self.InternalVesselZ-self.BoxThickness - Q("4mm"))
        
        Lar_bulk_lv = geom.structure.Volume("Lar_bulk_lv", 
                                            material="LAr", 
                                            shape=Lar_bulk_shape)
        
        Lar_bulk_lv.params.append(("SensDet", 'LArHit'))
        
        Lar_bulk_pla = geom.structure.Placement("Lar_bulk_pla", 
                                                 volume=Lar_bulk_lv)
                                                 
        Al_int_lv.placements.append(Lar_bulk_pla.name)
        
        return Gr_ext_lv

        
    # construct LAr target
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct_LAr_Target(self, geom, main_lv):
        
        LAr_tgt_lv = self.construct_LAr_Vessel(geom)
        
        pos1 = geom.structure.Position("Lar_target_position1",
                                      -self.kloeVesselRadius + self.ExternalVesselX + self.UpstreamVesselGap,
                                      Q('0mm'),
                                      self.InterVesselHalfGap+self.ExternalVesselZ)
                                      
        LAr_tgt_pla1 = geom.structure.Placement("LAr_tgt_pla1",
                                               volume=LAr_tgt_lv,
                                               pos=pos1,
                                               rot= "r180aboutY")
                                               
        main_lv.placements.append(LAr_tgt_pla1.name)
                  
        pos2 = geom.structure.Position("Lar_target_position2",
                                      -self.kloeVesselRadius + self.ExternalVesselX + self.UpstreamVesselGap,
                                      Q('0mm'),
                                      -(self.InterVesselHalfGap+self.ExternalVesselZ))
        
        LAr_tgt_pla2 = geom.structure.Placement("LAr_tgt_pla2",
                                               volume=LAr_tgt_lv,
                                               pos=pos2)
        
        main_lv.placements.append(LAr_tgt_pla2.name)

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct traking modules made of 1 XY strawplane + 1 additional X strawplane to be placed upstream (1 module) and downstream (4 modules)
    def construct_tracking_module(self, geom, name, halfDimension): 
        
        main_shape = geom.shapes.Box(name + "_shape", 
                                     dx=halfDimension['dx'], # 37.33 mm/2
                                     dy=halfDimension['dy'], 
                                     dz=halfDimension['dz'])

        main_lv = geom.structure.Volume(name + "_vol", 
                                        material="Air35C", 
                                        shape=main_shape)

        print( "STTModuleFULL::construct()")
        print( "  main_lv = "+ main_lv.name)

        pos_hh_in_TrMod=geom.structure.Position(name + "pos_hh_in_TrMod",+self.planeXXThickness, Q('0mm'),Q('0mm'))
#        pos_vv_in_TrMod=geom.structure.Position(name + "pos_vv_in_TrMod", Q('0mm'), Q('0mm'),Q('0mm'))
        pos_hh2_in_TrMod=geom.structure.Position(name + "pos_hh2_in_TrMod", -self.planeXXThickness, Q('0mm'),Q('0mm'))
        
        hh_lv=self.construct_STPlane(geom, 
                                     name+"_hor",
                                     halfDimension['dy'],
                                     halfDimension['dz'], 
                                     "stGas_Xe19")
        vv_lv=self.construct_STPlane(geom, 
                                     name+"_ver",
                                     halfDimension['dz'],
                                     halfDimension['dy'],
                                     "stGas_Xe19")
        hh2_lv=self.construct_STPlane(geom, 
                                     name+"_hor2",
                                     halfDimension['dy'],
                                     halfDimension['dz'], 
                                     "stGas_Xe19")
        
        
        hh_pla=geom.structure.Placement("pla_"+name+"_hh", 
                                        volume=hh_lv, 
                                        pos=pos_hh_in_TrMod)
        vv_pla=geom.structure.Placement("pla_"+name+"_vv", 
                                        volume=vv_lv,   
                                        #pos=pos_vv_in_TrMod,
                                        rot= "r90aboutX")
        hh2_pla=geom.structure.Placement("pla_"+name+"_hh2", 
                                        volume=hh2_lv, 
                                        pos=pos_hh2_in_TrMod)
        
        main_lv.placements.append(hh_pla.name)
        main_lv.placements.append(vv_pla.name)
        main_lv.placements.append(hh2_pla.name)
        return main_lv

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct straw tube regular module: C3H6 target + radiator foils + straw tube XY plane
    def construct_C3H6_Module(self,geom, name, halfDimension):

        main_shape = geom.shapes.Box(name + "_shape", 
                                     dx=halfDimension['dx'], 
                                     dy=halfDimension['dy'], 
                                     dz=halfDimension['dz'])

        main_lv = geom.structure.Volume(name + "_vol", 
                                        material="Air35C", 
                                        shape=main_shape)

        print( "STTModuleFULL::construct()")
        print( "  main_lv = "+ main_lv.name)

        slab_shape = geom.shapes.Box(name + "_slab_shape", 
                                     dx=self.slabThickness/2.0, 
                                     dy=halfDimension['dy'], 
                                     dz=halfDimension['dz'])

        slab_lv = geom.structure.Volume(name + "_slab_vol", 
                                        material="C3H6", 
                                        shape=slab_shape)
        
        slab_pos = geom.structure.Position(name + "_pos_slab_in_C3H6_Mod", 
                                           -self.C3H6ModThickness/2.0 + self.slabThickness/2.0, 
                                           Q('0cm'),
                                           Q('0cm'))

        slab_pla=geom.structure.Placement(name + "_slab_pla", 
                                          volume=slab_lv, 
                                          pos=slab_pos)

        main_lv.placements.append(slab_pla.name)
        
        foil_lv = self.construct_Foils(geom, 
                                      name + "_foils", 
                                      halfDimension['dy'], 
                                      halfDimension['dz'])
        
        foil_pos = geom.structure.Position(name + "_pos_foilchunk_in_C3H6_Mod",
                                           -self.C3H6ModThickness/2.0 + self.slabThickness + self.totFoilsThickness/2.0,
                                           Q('0cm'),
                                           Q('0cm'))

        foil_pla=geom.structure.Placement(name + "_foils_pla", 
                                          volume=foil_lv, 
                                          pos=foil_pos)

        main_lv.placements.append(foil_pla.name)
            
        strawplane_lv=self.construct_XYSTPlane(geom,
                                               name + "_ST",
                                               halfDimension['dy'],
                                               halfDimension['dz'],
                                               "stGas_Xe19")
        
        strawplane_pos = geom.structure.Position(name + "_pos_ST_in_C3H6_Mod", 
                                                 self.C3H6ModThickness/2.0 - self.planeXXThickness,
                                                 Q('0cm'),
                                                 Q('0cm'))
                                           
        strawplane_pla=geom.structure.Placement(name + "_ST_pla", 
                                                volume=strawplane_lv, 
                                                pos=strawplane_pos)

        main_lv.placements.append(strawplane_pla.name)
        return main_lv

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct straw tube module (with graphite target): graphite target + straw tube XY plane
    def construct_C_Module(self,geom, name, halfDimension):

        main_shape = geom.shapes.Box(name + "_shape", 
                                     dx=halfDimension['dx'], 
                                     dy=halfDimension['dy'], 
                                     dz=halfDimension['dz'])

        main_lv = geom.structure.Volume(name + "_vol", 
                                        material="Air35C", 
                                        shape=main_shape)
        
        print( "STTModuleFULL::construct()")
        print( "  main_lv = "+ main_lv.name)

        graphite_shape = geom.shapes.Box(name+"_graph_shape", 
                                         dx=self.graphiteThickness/2.0, 
                                         dy=halfDimension['dy'], 
                                         dz=halfDimension['dz'])

        graphite_lv = geom.structure.Volume(name+"_graph_vol", 
                                            material="Graphite", 
                                            shape=graphite_shape)
        
        graphite_pos = geom.structure.Position(name + "_pos_graphite_in_C_Mod", 
                                               -self.CModThickness/2.0+self.graphiteThickness/2.0, 
                                               Q('0cm'),
                                               Q('0cm'))
        
        graphite_pla=geom.structure.Placement(name+"_graph_pla", 
                                              volume=graphite_lv, 
                                              pos=graphite_pos)

        main_lv.placements.append(graphite_pla.name)

        strawplane_lv=self.construct_XYSTPlane(geom,
                                               name+"_ST", 
                                               halfDimension['dy'],
                                               halfDimension['dz'],
                                               "stGas_Ar19")
        
        strawplane_pos = geom.structure.Position(name + "_pos_ST_in_C_Mod",
                                                 self.CModThickness/2.0 - self.planeXXThickness,
                                                 Q('0cm'),
                                                 Q('0cm'))

        strawplane_pla=geom.structure.Placement("pla_"+name+"_ST", 
                                                volume=strawplane_lv, 
                                                pos=strawplane_pos)

        main_lv.placements.append(strawplane_pla.name)
        return main_lv

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct radiator foils
    def construct_Foils(self,geom, name, halfheight, halflength):
        main_shape = geom.shapes.Box(name, 
                                     dx=self.totFoilsThickness/2.0, 
                                     dy=halfheight, 
                                     dz=halflength)

        main_lv = geom.structure.Volume("vol"+name, 
                                        material="Air35C", 
                                        shape=main_shape)

        print( "STTModuleFULL::construct()")
        print( "  main_lv = "+ main_lv.name)
        
        foil_shape = geom.shapes.Box(name + "_foil_shape", 
                                     dx=self.foilThickness/2.0, 
                                     dy=halfheight, 
                                     dz=halflength)

        foil_lv = geom.structure.Volume(name + "_foil_vol", 
                                        material="C3H6", 
                                        shape=foil_shape)
        
        for i in range(self.nfoil):
            foil_pos = geom.structure.Position(name + "_pos_foil_"+str(i), 
                                          -self.totFoilsThickness/2.0 + self.foilThickness/2.0 + i*(self.foilThickness+self.foilGap), 
                                          Q('0m'), 
                                          Q('0m'))

            foil_pla = geom.structure.Placement("pla_"+name + "_foil_"+str(i), 
                                              volume=foil_lv, 
                                              pos=foil_pos)
            main_lv.placements.append(foil_pla.name)
        return main_lv

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct XY straw tube plane
    def construct_XYSTPlane(self,geom, name, halfheight, halflength, gasMaterial):
        main_shape = geom.shapes.Box(name, 
                                     dx=self.planeXXThickness, 
                                     dy=halfheight, 
                                     dz=halflength)
        main_lv = geom.structure.Volume("vol"+name, 
                                        material="Air35C", 
                                        shape=main_shape)
        
        pos_hh_in_ST=geom.structure.Position(name + "pos_hh_in_ST", -self.planeXXThickness/2.0, Q('0cm'),Q('0cm'))
        pos_vv_in_ST=geom.structure.Position(name + "pos_vv_in_ST", self.planeXXThickness/2.0 , Q('0cm'),Q('0cm'))
        
        hh_lv=self.construct_STPlane(geom, 
                                     name+"_hor",
                                     halfheight,
                                     halflength, 
                                     gasMaterial)
        vv_lv=self.construct_STPlane(geom, 
                                     name+"_ver",
                                     halflength,
                                     halfheight,
                                     gasMaterial)
        
        hh_pla=geom.structure.Placement("pla_"+name+"_hh", 
                                        volume=hh_lv, 
                                        pos=pos_hh_in_ST)
        vv_pla=geom.structure.Placement("pla_"+name+"_vv", 
                                        volume=vv_lv,   
                                        pos=pos_vv_in_ST,
                                        rot= "r90aboutX")
        
        main_lv.placements.append(hh_pla.name)
        main_lv.placements.append(vv_pla.name)
        return main_lv  

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct straw tube plane. Straw tubes are staggered
    def construct_STPlane(self,geom, name, halfheight, halflength, gasMaterial):
        main_shape = geom.shapes.Box(name + "_shape", 
                                     dx=self.planeXXThickness/2.0, 
                                     dy=halfheight, 
                                     dz=halflength)
        main_lv = geom.structure.Volume(name + "_vol", 
                                        material="Air35C", 
                                        shape=main_shape )
        straw_lv=self.construct_ST(geom,
                                   name + "_ST_" + gasMaterial , 
                                   halflength=halflength, 
                                   gasMaterial=gasMaterial)
            
        Nstraw=int(0.5*(2.*halfheight/self.strawRadius-1.))
        
        for i in range(Nstraw):
            pos1=[-self.planeXXThickness/2.0 + self.strawRadius, 
                  halfheight - (2*i+1)*self.strawRadius, 
                  Q('0m')]
            straw_pos1=geom.structure.Position("pos_"+name+"_"+str(i),
                                               pos1[0],pos1[1],pos1[2])
            straw_pla1=geom.structure.Placement("pla_"+name+"_"+str(i), 
                                                volume=straw_lv, 
                                                pos=straw_pos1)
            main_lv.placements.append(straw_pla1.name)

            pos2=[self.planeXXThickness/2.0 - self.strawRadius,  
                  halfheight -(2*i+2)*self.strawRadius, 
                  Q('0m')]
            straw_pos2=geom.structure.Position("pos_"+name+"_"+str(i+Nstraw), 
                                               pos2[0],pos2[1],pos2[2])
            straw_pla2=geom.structure.Placement("pla_"+name+"_"+str(i+Nstraw), 
                                                volume=straw_lv, 
                                                pos=straw_pos2)
            main_lv.placements.append(straw_pla2.name)    
        return main_lv  

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct straw tube        
    def construct_ST( self, geom, name, halflength, gasMaterial ):
        main_shape = geom.shapes.Tubs(name + "_shape", 
                                      rmin=Q("0m"), 
                                      rmax=self.strawRadius, 
                                      dz=halflength)
        main_lv = geom.structure.Volume(name + "_vol", 
                                        material = "Air35C", 
                                        shape = main_shape )

        coat_shape = geom.shapes.Tubs(name + "_coat", 
                                      rmin = self.strawRadius- self.coatThickness , 
                                      rmax = self.strawRadius, 
                                      dz = halflength)
        coat_lv = geom.structure.Volume(name + "_coat_lv", 
                                        material = "Aluminum", 
                                        shape = coat_shape)
        
        mylar_shape = geom.shapes.Tubs(name + "_mylar", 
                                       rmin = self.strawRadius- self.coatThickness - self.mylarThickness , 
                                       rmax = self.strawRadius- self.coatThickness, 
                                       dz = halflength)
        mylar_lv   = geom.structure.Volume(name + "_mylar_lv", 
                                           material = "Mylar", 
                                           shape = mylar_shape)

        
        air_shape=geom.shapes.Tubs(name+"_air", 
                                   rmin = self.strawWireWThickness + self.strawWireGThickness,
                                   rmax = self.strawRadius- self.coatThickness - self.mylarThickness, 
                                   dz = halflength)
        air_lv   = geom.structure.Volume(name+"_air_lv", 
                                         material = gasMaterial, 
                                         shape = air_shape)
        air_lv.params.append(("SensDet","Straw"))

        wireW_shape = geom.shapes.Tubs(name + "_wireW", 
                                       rmin = Q("0um"), 
                                       rmax = self.strawWireWThickness, 
                                       dz = halflength)
        wireW_lv    = geom.structure.Volume(name + "_wireW_lv", 
                                            material = "Tungsten", 
                                            shape = wireW_shape)

        wireG_shape = geom.shapes.Tubs(name + "_wireG", 
                                       rmin = self.strawWireWThickness, 
                                       rmax = self.strawWireWThickness + self.strawWireGThickness, 
                                       dz = halflength)
        wireG_lv    = geom.structure.Volume(name + "_wireG_lv", 
                                            material = "Gold", 
                                            shape = wireG_shape)
        
        coat_pla  = geom.structure.Placement( "pla_"+name+"_coat" , volume = coat_lv )
        mylar_pla = geom.structure.Placement( "pla_"+name+"_mylar", volume = mylar_lv )
        air_pla   = geom.structure.Placement( "pla_"+name+"_air"  , volume = air_lv )
        wireW_pla = geom.structure.Placement( "pla_"+name+"_wireW", volume = wireW_lv )
        wireG_pla = geom.structure.Placement( "pla_"+name+"_wireG", volume = wireG_lv )
        
        main_lv.placements.append( coat_pla.name )
        main_lv.placements.append( mylar_pla.name )
        main_lv.placements.append( air_pla.name )
        main_lv.placements.append( wireW_pla.name )
        main_lv.placements.append( wireG_pla.name )
        return main_lv        
        
