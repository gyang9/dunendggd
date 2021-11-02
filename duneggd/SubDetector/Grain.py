import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class GrainBuilder(gegede.builder.Builder):
    def configure( self, configuration=None, **kwds):

        self.configuration       = configuration
        
        if self.configuration == "option_1":

            ######################################### EXTERNAL VESSEL (endcap steel 12 mm)
            #               Carbon_fiber 12 mm                                  
            ######################################### END EXTERNAL VESSEL
            #               vacuum gap                                          
            ######################################### INTERNAL VESSEL (endcap aluminum 12 mm)
            #               Aluminum 12 mm 
            ######################################### END IINTERNAL VESSEL

            self.Carbon_fiberThickness   = Q("12mm") #two layers of 6 mm for a total of 12
            self.AluminumThickness   = Q("12mm")
            self.EndcapThickness     = Q("16mm")
        
            self.ExternalVesselX     = Q("297.5mm") + self.Carbon_fiberThickness #minor semiaxis of external vessel
            self.ExternalVesselY     = Q("788mm") + self.Carbon_fiberThickness #major semiaxis of external vessel
            self.ExternalVesselZ     = Q("816mm") + self.EndcapThickness #half lenght of external vessel
        
            self.InternalVesselX     = Q("237.5mm") + self.AluminumThickness #minor semiaxis of internal vessel
            self.InternalVesselY     = Q("728mm") + self.AluminumThickness #major semiaxis of internal vessel
            self.InternalVesselZ     = Q("600mm") + self.EndcapThickness #half lenght of internal vessel
        
            self.UpstreamVesselGap   = Q("30mm") #margin between kloe vessel and the LAr target
            #self.MinDistExtVesTrMod  = Q("50mm") #margin between LAr target and upstream traking module
            self.InterVesselHalfGap  = Q('30mm')


        elif self.configuration == "option_2":

            #########################################  EXTERNAL VESSEL (endcap steel 12 mm)
            #              Carbon_fiber 6 mm                                     
            #########################################
            #              honeycomb (vacuum) 50 mm     -----------> shal we put honeycomb? It is in the tool file
            #########################################
            #              Carbon_fiber 6 mm
            #########################################  END EXTERNAL VESSEL
            #              vacuum gap 
            #########################################  INTERNAL VESSEL (endcap aluminum 12 mm)
            #              aluminum 12 mm
            #########################################
            #                  LAr     
            #########################################  END INTERNAL VESSEL

            self.HoneycombThickness  = Q("50mm")
            self.Carbon_fiberThickness   = Q("6mm") #two layers of 6 mm for a total of 12
            self.AluminumThickness   = Q("12mm")
            self.EndcapThickness     = Q("16mm")
        
            self.ExternalVesselX     = Q("365mm") + self.HoneycombThickness + self.Carbon_fiberThickness*2 #minor semiaxis of external vessel
            self.ExternalVesselY     = Q("900mm") + self.HoneycombThickness + self.Carbon_fiberThickness*2 #major semiaxis of external vessel
            self.ExternalVesselZ     = Q("950mm") + self.EndcapThickness #half lenght of external vessel
        
            self.InternalVesselX     = Q("237.5mm") + self.AluminumThickness #minor semiaxis of internal vessel
            self.InternalVesselY     = Q("728mm") + self.AluminumThickness #major semiaxis of internal vessel
            self.InternalVesselZ     = Q("650mm") + self.EndcapThickness #half lenght of internal vessel
        
            self.UpstreamVesselGap   = Q("30mm") #margin between kloe vessel and the LAr target
            #self.MinDistExtVesTrMod  = Q("50mm") #margin between LAr target and upstream traking module
            #self.InterVesselHalfGap  = Q('30mm')
            

    #def construct(self,geom):
        # whole_shape=geom.shapes.PolyhedraRegular("whole_shape_for_grain",numsides=self.nBarrelModules, rmin=Q('0cm'), rmax=self.kloeVesselRadius , dz=self.kloeVesselHalfDx, sphi=self.rotAngle)
        # upstream_shape=geom.shapes.Box("upstream_shape_for_grain", dx=0.5*self.liqArThickness, dy=self.kloeVesselRadius, dz=self.kloeVesselHalfDx )
        # upstream_shape_pos = geom.structure.Position("upstream_shape_pos_for_grain", 0.5*self.liqArThickness, Q('0m'), Q('0m'))
        # grain_shape = geom.shapes.Boolean("grain_shape",
        #                                  type='intersection',
        #                                  first=whole_shape,
        #                                  second=upstream_shape,
        #                                  rot='r180aboutY',
        #                                  pos=upstream_shape_pos)

        # main_lv = geom.structure.Volume('Grain_envelope',   material=self.Material, shape=grain_shape)
        #self.construct_GRAIN(geom, main_lv)
    def construct(self, geom):
        if self.configuration == "option_1":
            main_lv = self.construct_GRAIN_option1(geom)
        elif self.configuration == "option_2":
            main_lv = self.construct_GRAIN_option2(geom)

        #main_lv = self.construct_GRAIN(geom)
        print( "  main_lv = "+ main_lv.name)
        #print('building GRAIN')
        self.add_volume( main_lv )

#############################################################         GRAIN   1      ###################################################################

    def construct_GRAIN_option1(self, geom):
        
        print("-------------------------------------------")
        print("BUILDING GRAIN OPTION 1")
        print("-------------------------------------------")

        # build the external vessel envelop
        
        Ext_vessel_shape = geom.shapes.EllipticalTube("Ext_vessel_shape", 
                                                      dx = self.ExternalVesselX, 
                                                      dy = self.ExternalVesselY, 
                                                      dz = self.ExternalVesselZ)

        Ext_vessel_lv = geom.structure.Volume("Ext_vessel_lv", 
                                              material = "Carbon_fiber", 
                                              shape = Ext_vessel_shape)


        # build the layer of vacuum between the two vessels

        vacuum_gap_between_vessels_shape  = geom.shapes.EllipticalTube("vacuum_gap_between_vessels_shape", 
                                                                       dx = self.ExternalVesselX - self.Carbon_fiberThickness, 
                                                                       dy = self.ExternalVesselY - self.Carbon_fiberThickness, 
                                                                       dz = self.ExternalVesselZ - self.EndcapThickness) # self.EndcapThickness needed?
                                                            
                                                            
        vacuum_gap_between_vessels_lv = geom.structure.Volume("vacuum_gap_between_vessels_lv", 
                                                              material = "Vacuum_cryo", 
                                                              shape = vacuum_gap_between_vessels_shape)
                                                                    
        
        vacuum_gap_between_vessels_pla = geom.structure.Placement("vacuum_gap_between_vessels_pla",
                                                                  volume = vacuum_gap_between_vessels_lv)
        
        
        Ext_vessel_lv.placements.append(vacuum_gap_between_vessels_pla.name)  

        
        # build the layer of aluminum of the inner vessel
        
        Int_vessel_shape = geom.shapes.EllipticalTube("Int_vessel_shape", 
                                                      dx = self.InternalVesselX, 
                                                      dy = self.InternalVesselY, 
                                                      dz = self.InternalVesselZ)

        Int_vessel_lv = geom.structure.Volume("Int_vessel_lv", 
                                              material = "Aluminum", 
                                              shape = Int_vessel_shape)

        
        Int_vessel_pla = geom.structure.Placement("Int_vessel_pla",
                                                  volume = Int_vessel_lv)
                                               
        vacuum_gap_between_vessels_lv.placements.append(Int_vessel_pla.name)

        
        # build the inner volume of LAr
        
        LAr_volume_shape = geom.shapes.EllipticalTube("LAr_volume_shape", 
                                                      dx = self.InternalVesselX - self.AluminumThickness, 
                                                      dy = self.InternalVesselY - self.AluminumThickness, 
                                                      dz = self.InternalVesselZ - self.EndcapThickness)

        LAr_volume_lv = geom.structure.Volume("LAr_volume_lv", 
                                              material = "LAr", 
                                              shape = LAr_volume_shape)
                                              
        LAr_volume_lv.params.append(("SensDet", 'LArHit'))
                                                                    
        
        LAr_volume_pla = geom.structure.Placement("LAr_volume_pla",
                                                  volume = LAr_volume_lv)
                                               
        Int_vessel_lv.placements.append(LAr_volume_pla.name)


        # build external vessel endcaps
        
        EndCap_ExtVessel_shape = geom.shapes.EllipticalTube("EndCap_ExtVessel_shape", 
                                                            dx = self.ExternalVesselX, 
                                                            dy = self.ExternalVesselY, 
                                                            dz = self.EndcapThickness/2)
                                         
        EndCap1_ExtVessel_lv = geom.structure.Volume("EndCap1_ExtVessel_lv", 
                                                      material = "Steel", 
                                                      shape = EndCap_ExtVessel_shape)
                                          
        EndCap1_ExtVessel_pos = geom.structure.Position("EndCap1_ExtVessel_pos",
                                                        Q("0mm"),#- self.kloeVesselRadius + self.UpstreamVesselGap + self.ExternalVesselX,
                                                        Q("0mm"),
                                                        - self.ExternalVesselZ +  self.EndcapThickness/2)
                                      
        EndCap1_ExtVessel_pla = geom.structure.Placement("EndCap1_ExtVessel_pla",
                                                          volume = EndCap1_ExtVessel_lv,
                                                          pos = EndCap1_ExtVessel_pos)
        
        Ext_vessel_lv.placements.append(EndCap1_ExtVessel_pla.name)
        
        
        EndCap2_ExtVessel_lv = geom.structure.Volume("EndCap2_ExtVessel_lv", 
                                                      material = "Steel", 
                                                      shape = EndCap_ExtVessel_shape)
        
        EndCap2_ExtVessel_pos = geom.structure.Position("EndCap2_ExtVessel_pos",
                                                        Q("0mm"),#- self.kloeVesselRadius + self.UpstreamVesselGap + self.ExternalVesselX,
                                                        Q("0mm"),
                                                        + self.ExternalVesselZ - self.EndcapThickness/2)
                                      
        EndCap2_ExtVessel_pla = geom.structure.Placement("EndCap2_ExtVessel_pla",
                                                         volume = EndCap2_ExtVessel_lv,
                                                         pos = EndCap2_ExtVessel_pos)        
        
        Ext_vessel_lv.placements.append(EndCap2_ExtVessel_pla.name)


        return Ext_vessel_lv


        #return self.construct_GRAIN_option2(geom)

##############################################################        END GRAIN    1     ################################################################        


##############################################################         GRAIN   2      ###################################################################
    
    
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    #def construct_GRAIN(self, geom, main_lv):
    def construct_GRAIN_option2(self, geom):

        print("-------------------------------------------")
        print("BUILDING GRAIN OPTION 2")
        print("-------------------------------------------")

    
        # build the external vessel envelop
        
        Ext_vessel_outern_Carbon_fiber_layer_shape = geom.shapes.EllipticalTube("Ext_vessel_outern_Carbon_fiber_layer_shape", 
                                                                            dx = self.ExternalVesselX, 
                                                                            dy = self.ExternalVesselY, 
                                                                            dz = self.ExternalVesselZ)

        Ext_vessel_outern_Carbon_fiber_layer_lv = geom.structure.Volume("Ext_vessel_outern_Carbon_fiber_layer_lv", 
                                                                    material = "Carbon_fiber", 
                                                                    shape = Ext_vessel_outern_Carbon_fiber_layer_shape)
                                                                    
        # pos = geom.structure.Position("GRAI_position",
        #                               -self.kloeVesselRadius + self.ExternalVesselX + self.UpstreamVesselGap,
        #                               Q('0mm'),
        #                               Q('0mm'))
        
        # Ext_vessel_outern_Carbon_fiber_layer_pla = geom.structure.Placement("Ext_vessel_outern_Carbon_fiber_layer_pla",
        #                                                                 volume = Ext_vessel_outern_Carbon_fiber_layer_lv,
        #                                                                 pos = pos)
                                               
        #main_lv.placements.append(Ext_vessel_outern_Carbon_fiber_layer_pla.name)
        
        # build the layer of vacuum (in the real geometry honeycomb)
        
        Honeycomb_empty_layer_shape  = geom.shapes.EllipticalTube("Honeycomb_empty_layer_shape", 
                                                                  dx = self.ExternalVesselX - self.Carbon_fiberThickness, 
                                                                  dy = self.ExternalVesselY - self.Carbon_fiberThickness, 
                                                                  dz = self.ExternalVesselZ - self.EndcapThickness) # self.EndcapThickness needed?
                                                            
                                                            
        Honeycomb_empty_layer_lv = geom.structure.Volume("Honeycomb_empty_layer_lv", 
                                                          material = "Vacuum_cryo", 
                                                          shape = Honeycomb_empty_layer_shape)
                                                                    
        
        Honeycomb_empty_layer_pla = geom.structure.Placement("Honeycomb_empty_layer_pla",
                                                                volume = Honeycomb_empty_layer_lv)
        
        
        Ext_vessel_outern_Carbon_fiber_layer_lv.placements.append(Honeycomb_empty_layer_pla.name)
        
        
        # build the inner layer of Carbon_fiber of the external vessel
        
        Ext_vessel_inner_Carbon_fiber_layer_shape = geom.shapes.EllipticalTube("Ext_vessel_inner_Carbon_fiber_layer_shape", 
                                                                            dx = self.ExternalVesselX - self.Carbon_fiberThickness - self.HoneycombThickness, 
                                                                            dy = self.ExternalVesselY - self.Carbon_fiberThickness - self.HoneycombThickness, 
                                                                            dz = self.ExternalVesselZ - self.EndcapThickness)

        Ext_vessel_inner_Carbon_fiber_layer_lv = geom.structure.Volume("Ext_vessel_inner_Carbon_fiber_layer_lv", 
                                                                    material = "Carbon_fiber", 
                                                                    shape = Ext_vessel_inner_Carbon_fiber_layer_shape)
                                                                    
                                                                    
        Ext_vessel_inner_Carbon_fiber_layer_pla = geom.structure.Placement("Ext_vessel_inner_Carbon_fiber_layer_pla",
                                                                       volume = Ext_vessel_inner_Carbon_fiber_layer_lv)
                                               
        
        Honeycomb_empty_layer_lv.placements.append(Ext_vessel_inner_Carbon_fiber_layer_pla.name)
        
        
        # build the layer of vacuum between the two vessels
        
        vacuum_gap_between_vessels_shape  = geom.shapes.EllipticalTube("vacuum_gap_between_vessels_shape", 
                                                                       dx = self.ExternalVesselX - self.Carbon_fiberThickness*2 - self.HoneycombThickness, 
                                                                       dy = self.ExternalVesselY - self.Carbon_fiberThickness*2 - self.HoneycombThickness, 
                                                                       dz = self.ExternalVesselZ - self.EndcapThickness) # self.EndcapThickness needed?
                                                            
                                                            
        vacuum_gap_between_vessels_lv = geom.structure.Volume("vacuum_gap_between_vessels_lv", 
                                                              material = "Vacuum_cryo", 
                                                              shape = vacuum_gap_between_vessels_shape)
                                                                    
        
        vacuum_gap_between_vessels_pla = geom.structure.Placement("vacuum_gap_between_vessels_pla",
                                                                  volume = vacuum_gap_between_vessels_lv)
        
        
        Ext_vessel_inner_Carbon_fiber_layer_lv.placements.append(vacuum_gap_between_vessels_pla.name)
        
        
        # build the layer of aluminum of the inner vessel
        
        Aluminum_layer_inner_vessel_shape = geom.shapes.EllipticalTube("Aluminum_layer_inner_vessel_shape", 
                                                                       dx = self.InternalVesselX, 
                                                                       dy = self.InternalVesselY, 
                                                                       dz = self.InternalVesselZ)

        Aluminum_layer_inner_vessel_lv = geom.structure.Volume("Aluminum_layer_inner_vessel_lv", 
                                                                material = "Aluminum", 
                                                                shape = Aluminum_layer_inner_vessel_shape)

        
        Aluminum_layer_inner_vessel_pla = geom.structure.Placement("Aluminum_layer_inner_vessel_pla",
                                                                   volume = Aluminum_layer_inner_vessel_lv)
                                               
        vacuum_gap_between_vessels_lv.placements.append(Aluminum_layer_inner_vessel_pla.name)
        
        
        # build the inner volume of LAr
        
        LAr_volume_shape = geom.shapes.EllipticalTube("LAr_volume_shape", 
                                                      dx = self.InternalVesselX - self.AluminumThickness, 
                                                      dy = self.InternalVesselY - self.AluminumThickness, 
                                                      dz = self.InternalVesselZ - self.EndcapThickness)

        LAr_volume_lv = geom.structure.Volume("LAr_volume_lv", 
                                              material = "LAr", 
                                              shape = LAr_volume_shape)
                                              
        LAr_volume_lv.params.append(("SensDet", 'LArHit'))
                                                                    
        
        LAr_volume_pla = geom.structure.Placement("LAr_volume_pla",
                                                  volume = LAr_volume_lv)
                                               
        Aluminum_layer_inner_vessel_lv.placements.append(LAr_volume_pla.name)
        
       
        # build external vessel endcaps
        
        EndCap_ExtVessel_shape = geom.shapes.EllipticalTube("EndCap_ExtVessel_shape", 
                                                            dx = self.ExternalVesselX, 
                                                            dy = self.ExternalVesselY, 
                                                            dz = self.EndcapThickness/2)
                                         
        EndCap1_ExtVessel_lv = geom.structure.Volume("EndCap1_ExtVessel_lv", 
                                                      material = "Steel", 
                                                      shape = EndCap_ExtVessel_shape)
                                          
        EndCap1_ExtVessel_pos = geom.structure.Position("EndCap1_ExtVessel_pos",
                                                        Q("0mm"),#- self.kloeVesselRadius + self.UpstreamVesselGap + self.ExternalVesselX,
                                                        Q("0mm"),
                                                        - self.ExternalVesselZ +  self.EndcapThickness/2)
                                      
        EndCap1_ExtVessel_pla = geom.structure.Placement("EndCap1_ExtVessel_pla",
                                                          volume = EndCap1_ExtVessel_lv,
                                                          pos = EndCap1_ExtVessel_pos)
        
        Ext_vessel_outern_Carbon_fiber_layer_lv.placements.append(EndCap1_ExtVessel_pla.name)
        
        
        EndCap2_ExtVessel_lv = geom.structure.Volume("EndCap2_ExtVessel_lv", 
                                                      material = "Steel", 
                                                      shape = EndCap_ExtVessel_shape)
        
        EndCap2_ExtVessel_pos = geom.structure.Position("EndCap2_ExtVessel_pos",
                                                        Q("0mm"),#- self.kloeVesselRadius + self.UpstreamVesselGap + self.ExternalVesselX,
                                                        Q("0mm"),
                                                        + self.ExternalVesselZ - self.EndcapThickness/2)
                                      
        EndCap2_ExtVessel_pla = geom.structure.Placement("EndCap2_ExtVessel_pla",
                                                         volume = EndCap2_ExtVessel_lv,
                                                         pos = EndCap2_ExtVessel_pos)        
        
        Ext_vessel_outern_Carbon_fiber_layer_lv.placements.append(EndCap2_ExtVessel_pla.name)
        
        
        return Ext_vessel_outern_Carbon_fiber_layer_lv
        
        
    
##############################################################        END GRAIN    2     ################################################################
