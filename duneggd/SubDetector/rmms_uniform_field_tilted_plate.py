#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q

class rmmsBuilder(gegede.builder.Builder):
        

    def configure(self, mat = None, thinbox1Dimension = None, thinbox2Dimension = None, magneticbox1Dimension = None, magneticbox2Dimension = None, gapPosition = None, BFieldUp = None, BFieldDown = None, **kwds):
        self.BFieldUp = BFieldUp
        self.BFieldDown = BFieldDown
        self.magneticbox1Dimension =  magneticbox1Dimension
        self.magneticbox2Dimension = magneticbox2Dimension
        self.mat=mat
        self.thinbox1Dimension=thinbox1Dimension
        self.thinbox2Dimension=thinbox2Dimension
        self.gapPosition=gapPosition
        
    #Rotation of Magnetic Field                                                                                                                                                                             
        
    def construct(self, geom):        
            
        #Make Boxes for rmms
         rmmsbox = geom.shapes.Box( 'rmmsbox',
                                   dx = 0.5*Q("7.04m"),
                                   dy = 0.5*Q("6.825m"),
                                   dz = 0.5*Q("6.94m"))
         #Make Boxes for Magnetic filed
         MagneticBox1 = geom.shapes.Box( 'Magneticbox1',
                                         dx = 0.5*self.magneticbox1Dimension[0],
                                         dy = 0.5*self.magneticbox1Dimension[1],
                                         dz = 0.5*self.magneticbox1Dimension[2])
         MagneticBox2 = geom.shapes.Box( 'Magneticbox2',
                                         dx = 0.5*self.magneticbox2Dimension[0],
                                         dy = 0.5*self.magneticbox2Dimension[1],
                                         dz = 0.5*self.magneticbox2Dimension[2])
         #Make Boxes for steel
         thinBox1 = geom.shapes.Box( 'box'+self.name,
                                    dx = 0.5*self.thinbox1Dimension[0],
                                    dy = 0.5*self.thinbox1Dimension[1],
                                    dz = 0.5*self.thinbox1Dimension[2])
         thinBox2 = geom.shapes.Box( 'box2'+self.name,
                                    dx = 0.5*self.thinbox2Dimension[0],
                                    dy = 0.5*self.thinbox2Dimension[1],
                                    dz = 0.5*self.thinbox2Dimension[2])

         thickBox1 = geom.shapes.Box( 'thickbox'+self.name,
                                     dx = 0.5*self.thinbox1Dimension[0],
                                     dy = 0.5*self.thinbox1Dimension[1],
                                     dz = 0.5*Q("0.040m"))
         thickBox2 = geom.shapes.Box( 'thickbox2'+self.name,
                                    dx = 0.5*self.thinbox2Dimension[0],
                                    dy = 0.5*self.thinbox2Dimension[1],
                                    dz = 0.5*Q("0.040m"))
         #innerBField="(0.5 T, 0.0 T, 0.0 T)"
         #B_fieldup_left_rot = ('-BFieldUp*math.sin(0.0523599)','BFieldUp*math.cos(0.0523599)','0'),
         #B_fieldup_ri_rot = ('Bfieldup*math.sin(0.0523599)','BFieldUp*math.cos(0.0523599)','0'),
         #B_fielddown_left_rot = ('-BFieldDown*math.sin(0.0523599)','-BFieldDown*math.cos(0.0523599)','0'),
         #B_fielddown_ri_rot = ('BFieldDown*math.sin(0.0523599)','-BFieldDown*math.cos(0.0523599)','0')

         B_fieldup_left_rot_x=-1.5*math.sin(0.052359)
         B_fieldup_left_rot_y=1.5*math.cos(0.052359)
         B_fieldup_ri_rot_x= 1.5*math.sin(0.0523599) 
         B_fieldup_ri_rot_y=1.5*math.cos(0.0523599)
         B_fielddown_left_rot_x=-1.5*math.sin(0.0523599) 
         B_fielddown_left_rot_y=-1.5*math.cos(0.0523599)
         B_fielddown_ri_rot_x=1.5*math.sin(0.0523599)
         B_fielddown_ri_rot_y= 1.5*math.cos(0.0523599)



         B_fieldup_left_rot="({} T,{} T,0 T)".format(B_fieldup_left_rot_x, B_fieldup_left_rot_y)
         B_fieldup_ri_rot="({} T,{} T,0 T)".format(B_fieldup_ri_rot_x,B_fieldup_ri_rot_y)
         B_fielddown_left_rot="({} T,{} T,0 T)".format(B_fielddown_left_rot_x,B_fielddown_left_rot_y)
         B_fielddown_ri_rot="({} T,{} T,0 T)".format( B_fielddown_ri_rot_x,B_fielddown_ri_rot_y)

         print(B_fieldup_left_rot,B_fieldup_ri_rot, B_fielddown_left_rot,B_fielddown_ri_rot)

        # Logical volumes for rmms
         rmms_lv = geom.structure.Volume( 'rmmsvol', material='NoGas', shape=rmmsbox )
         #Make box for Scint Bar                                                                                                                                                  
         scinBox = geom.shapes.Box( 'scinbox'+self.name,
                                    dx = 0.5*Q("0.04m"),
                                    dy = 0.5*Q("3.2m"),
                                    dz = 0.5*Q("0.01m"))
         

         #Logical volumes for ScinBox
         scinBoxup_lv = geom.structure.Volume( 'scinBoxuplv'+self.name, material='Scintillator', shape=scinBox )
         scinBoxdown_lv = geom.structure.Volume( 'scinBoxdownlv'+self.name, material='Scintillator', shape=scinBox )
         
         scinBoxup_lv.params.append(("SensDet", rmms_lv.name))
         scinBoxdown_lv.params.append(("SensDet", rmms_lv.name))

         scinBoxdown_lv.params.append(('BField',self.BFieldDown))
         scinBoxup_lv.params.append(('BField',self.BFieldUp))
         
         #Logical volumes for Magnetic Boxes

         MagneticBox1_lv = geom.structure.Volume( 'Maneticvol1'+self.name, material=self.mat, shape=MagneticBox1 )
         MagneticBox2_lv = geom.structure.Volume( 'Magneticvol2'+self.name, material=self.mat, shape=MagneticBox2 )

         MagneticBox1_lv.params.append(('BField',self.BFieldDown))
         MagneticBox2_lv.params.append(('BField',self.BFieldUp))
         # Logical volumes for steel Boxes

         thinBox1_lv = geom.structure.Volume( 'thinvol'+self.name, material=self.mat, shape=thinBox1 )
         thinBox2_lv = geom.structure.Volume( 'thinvol2'+self.name, material=self.mat, shape=thinBox2 )
         thickBox1_lv = geom.structure.Volume( 'thickvol'+self.name, material=self.mat, shape=thickBox1 )
         thickBox2_lv = geom.structure.Volume( 'thickvol2'+self.name, material=self.mat, shape=thickBox2 )                                                                                                 
         
         thinBox1_lv.params.append(('BField',self.BFieldDown))
         thickBox1_lv.params.append(('BField',self.BFieldDown))
         thinBox2_lv.params.append(('BField',self.BFieldUp))
         thickBox2_lv.params.append(('BField',self.BFieldUp))
         

         #Poition Magneticbox in rmms volumes                                                                                                                                                                                                                                                                                        
         lf_pos_Mag = geom.structure.Position( 'lfposMag'+self.name,
                                          0.5*(self.magneticbox1Dimension[0]+self.magneticbox2Dimension[0])+self.gapPosition[0],
                                          Q("1.8125m"),
                                          Q("0m"))

         rt_pos_Mag = geom.structure.Position( 'rtposMag'+self.name,
                                          -(0.5*(self.magneticbox1Dimension[0]+self.magneticbox2Dimension[0])+self.gapPosition[0]),
                                          Q("1.8125m"),
                                          Q("0m"))

         ctr_pos_Mag = geom.structure.Position( 'ctrposMag'+self.name,
                                           Q("0m"),
                                           Q("1.8125m"),
                                           Q("0m"))

         rt_pla_Mag = geom.structure.Placement( 'rtplaMag'+self.name, volume=MagneticBox1_lv, pos=rt_pos_Mag )
         lf_pla_Mag = geom.structure.Placement( 'lfplaMag'+self.name, volume=MagneticBox1_lv, pos=lf_pos_Mag )
         ctr_pla_Mag = geom.structure.Placement( 'ctrplaMag'+self.name, volume=MagneticBox2_lv, pos=ctr_pos_Mag )

         rmms_lv.placements.append(rt_pla_Mag.name)
         rmms_lv.placements.append(lf_pla_Mag.name)
         rmms_lv.placements.append(ctr_pla_Mag.name)
        
            
         #Adding steelBox in magnetic volumes1 (ThinsteelBox1)
         n_Boxes = 40
         thinBox1_pos = [geom.structure.Position('a')]*n_Boxes
         thinBox1_pla = [geom.structure.Placement('b',volume=thinBox1_lv, pos=thinBox1_pos[1])]*n_Boxes

         for iter in range(0,n_Boxes):
            x = Q("0m")
            y = Q("0m")
            zpos = -Q("3.4645m")+ iter * Q("0.055m")
            thinBox1_pos[iter] = geom.structure.Position( 'thinBox1position'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("0m"),
                                                           z = zpos)
           
            thinBox1_pla[iter] = geom.structure.Placement('thinBox1pla'+self.name+str(iter), volume = thinBox1_lv, pos = thinBox1_pos[iter]) 
            MagneticBox1_lv.placements.append(thinBox1_pla[iter].name)
           
        #ThickBox1 Placements in Magnetic Box1                                                                                                                                                                                       
         m_Boxes = 60
         thickBox1_pos = [geom.structure.Position('c')]*m_Boxes

         thick_Box1_pla = [geom.structure.Placement('d',volume = thickBox1_lv, pos = thickBox1_pos[1])]*m_Boxes

         for iter in range(0,m_Boxes):
             x = Q("0m")
             y = Q("0m")
             wpos = -Q("1.292m")+ iter * Q("0.08m")
             thickBox1_pos[iter] = geom.structure.Position( 'thickBox1position'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("0m"),
                                                           z = wpos)
             thick_Box1_pla[iter] = geom.structure.Placement( 'thickBox1pla'+self.name+str(iter), volume = thickBox1_lv, pos = thickBox1_pos[iter] )
             MagneticBox1_lv.placements.append(thick_Box1_pla[iter].name)


        #Adding steelBox in magnetic volumes2 (ThinsteelBox2)
         o_Boxes = 40
         thinBox2_pos = [geom.structure.Position('e')]*o_Boxes
         thinBox2_pla = [geom.structure.Placement('f',volume = thinBox2_lv, pos=thinBox2_pos[1])]*o_Boxes

         for iter in range(0,o_Boxes):
             x = Q("0m")
             y = Q("0m")
             zpos = -Q("3.4645m")+ iter * Q("0.055m")
             thinBox2_pos[iter] = geom.structure.Position( 'thinBox2position'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("0m"),
                                                           z = zpos)

             thinBox2_pla[iter] = geom.structure.Placement('thinBox2pla'+self.name+str(iter), volume = thinBox2_lv, pos= thinBox2_pos[iter])
             MagneticBox2_lv.placements.append(thinBox2_pla[iter].name)
        #ThickBox Placements in Magenetic volumes2(ThicksteelBox2)
         p_Boxes = 60
         thickBox2_pos = [geom.structure.Position('g')]*p_Boxes

         thick_Box2_pla = [geom.structure.Placement('h',volume = thickBox2_lv, pos=thickBox2_pos[1])]*p_Boxes

         for iter in range(0,p_Boxes):
             x = Q("0m")
             y = Q("0m")
             wpos = -Q("1.292m")+ iter * Q("0.08m")
             thickBox2_pos[iter] = geom.structure.Position( 'thickBox2position'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("0m"),
                                                           z = wpos)
             thick_Box2_pla[iter] = geom.structure.Placement( 'thickBox2pla'+self.name+str(iter), volume = thickBox2_lv, pos = thickBox2_pos[iter] )
             MagneticBox2_lv.placements.append(thick_Box2_pla[iter].name)
  
           
        

        #Place Bars into Modules                                                                                                                                                                            
         ModuleBox = geom.shapes.Box( 'ModuleBox',
                                     dx = 0.5*Q("0.04m")*42,
                                     dy = 0.5*Q("3.2m"),
                                     dz = 0.5*Q("0.01m"))
         ModuleBoxup_lv = geom.structure.Volume( 'ModuleBoxupvol', material='NoGas', shape=ModuleBox )
         ModuleBoxdown_lv = geom.structure.Volume( 'ModuleBoxdownvol', material='NoGas', shape=ModuleBox )

         #ModuleBoxup_lv.params.append(('BField',self.BFieldUp))
         #ModuleBoxdown_lv.params.append(('BField',self.BFieldUp))

         ModuleBoxup_lv.params.append(("BField",B_fieldup_left_rot)) 
         ModuleBoxup_lv.params.append(("BField",B_fieldup_ri_rot ))
         ModuleBoxdown_lv.params.append(("BField",B_fielddown_left_rot))
         ModuleBoxdown_lv.params.append(("BField",B_fielddown_ri_rot))  
         
         sci_bars = 42
         sci_Bar_pos = [geom.structure.Position('i')]*sci_bars

         sci_Barup_pla = [geom.structure.Placement('j',volume=scinBoxup_lv, pos=sci_Bar_pos[1])]*sci_bars
         sci_Bardown_pla = [geom.structure.Placement('s',volume=scinBoxdown_lv, pos=sci_Bar_pos[1])]*sci_bars
         for iter in range(0,sci_bars):
             z = Q("0m")
             y = Q("0m")
             xpos = -Q("0.820m")+ iter * Q("0.04m")
             sci_Bar_pos[iter] = geom.structure.Position( 'sci_barposition'+str(iter),
                                                           x = xpos,
                                                           y = Q("0m"),
                                                           z = Q("0m"))
             sci_Barup_pla[iter] = geom.structure.Placement( 'scibaruppla'+self.name+str(iter), volume=scinBoxup_lv, pos=sci_Bar_pos[iter] )
             sci_Bardown_pla[iter] = geom.structure.Placement( 'scibardownpla'+self.name+str(iter), volume=scinBoxdown_lv, pos=sci_Bar_pos[iter] )

             ModuleBoxup_lv.placements.append(sci_Barup_pla[iter].name)
             ModuleBoxdown_lv.placements.append(sci_Bardown_pla[iter].name)
         




        #placeModulBox into MagneticBox1 
         Module_boxes_thin = 39
         thin_Modbox_ri_rot = geom.structure.Rotation('thinModboxrirot', '0deg','0deg','3deg')
         thin_Modbox_left_rot= geom.structure.Rotation( 'thinModboxleftrot1', '0deg','0deg','-3deg')
         thinModbox_pos = [geom.structure.Position('k')]*Module_boxes_thin


         thin_Modbox_ri_pla = [geom.structure.Placement('l', volume = ModuleBoxdown_lv, pos=thinModbox_pos[1], rot = thin_Modbox_ri_rot)]*Module_boxes_thin
         thin_Modbox_left_pla = [geom.structure.Placement('u', volume = ModuleBoxdown_lv, pos=thinModbox_pos[1], rot = thin_Modbox_left_rot)]*Module_boxes_thin

         for iter in range(0,Module_boxes_thin):
             x = Q("0m")
             y = Q("0m")
             zpos = -Q("3.4645m")+Q("0.0275m") +iter * Q("0.055m")
             thinModbox_pos[iter] = geom.structure.Position( 'thinModboxposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("0m"),
                                                           z = zpos)
             if iter % 2 == 0:    
                thin_Modbox_ri_pla[iter] = geom.structure.Placement( 'thinModboxripla'+self.name+str(iter), volume = ModuleBoxdown_lv, pos=thinModbox_pos[iter], rot = thin_Modbox_ri_rot)
                MagneticBox1_lv.placements.append(thin_Modbox_ri_pla[iter].name)
             else:
                thin_Modbox_left_pla[iter] = geom.structure.Placement( 'thinModboxleftpla'+self.name+str(iter), volume = ModuleBoxdown_lv, pos=thinModbox_pos[iter], rot =  thin_Modbox_left_rot)          
                MagneticBox1_lv.placements.append(thin_Modbox_left_pla[iter].name)

         Module_boxes_thick = 59
         thick_Modbox_ri_rot = geom.structure.Rotation( 'thickModboxrirot', '0deg','0deg','3deg')
         thick_Modbox_left_rot = geom.structure.Rotation( 'thickModboxleftrot', '0deg','0deg','-3deg')

         thickModbox_pos = [geom.structure.Position('m')]*Module_boxes_thick

         thick_Modbox_ri_pla = [geom.structure.Placement('n',volume = ModuleBoxdown_lv, pos=thickModbox_pos[1], rot = thick_Modbox_ri_rot)]*Module_boxes_thick
         thick_Modbox_left_pla = [geom.structure.Placement('v',volume = ModuleBoxdown_lv, pos=thickModbox_pos[1], rot = thick_Modbox_left_rot)]*Module_boxes_thick


         for iter in range(0,Module_boxes_thick):
             x = Q("0m")
             y = Q("0m")
             zpos = -Q("1.292m")+ Q("0.040m")  +iter * Q("0.08m")

             thickModbox_pos[iter] = geom.structure.Position( 'thickModboxposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("0m"),
                                                           z = zpos)
             if iter % 2 == 0 :    
                 thick_Modbox_ri_pla[iter] = geom.structure.Placement( 'thickModboxripla'+self.name+str(iter), volume = ModuleBoxdown_lv, pos=thickModbox_pos[iter], rot = thick_Modbox_ri_rot)
                 MagneticBox1_lv.placements.append(thick_Modbox_ri_pla[iter].name)
             else:
                 thick_Modbox_left_pla[iter] = geom.structure.Placement( 'thickModboxleftpla'+self.name+str(iter), volume = ModuleBoxdown_lv, pos=thickModbox_pos[iter], rot = thick_Modbox_left_rot)
                 MagneticBox1_lv.placements.append(thick_Modbox_left_pla[iter].name)
            
                                            
        #Place Modules into scint layers                                                                                                                                                                    
         Module_layer = geom.shapes.Box( 'Modulelayerbox',
                                         dx = 0.5*Q("3.43m"),
                                         dy = 0.5*Q("3.2m"),
                                         dz = 0.5*Q("0.040m"))

         Module_layerup_lv = geom.structure.Volume( 'modulelayerupvol', material='NoGas', shape=Module_layer )
         

                 #Poition modules in layer volumes                                                                                                                                                                  
         Mod_ri_rot = geom.structure.Rotation( 'Modrirot', '0deg','0deg','3deg')
         Mod_left_rot = geom.structure.Rotation( 'Modleftrot', '0deg','0deg','-3deg')

         mod_pos2 = geom.structure.Position( 'modpos2'+self.name,
                                            -0.5*Q("0.04m")*42-Q("0.035m"),
                                            Q("0m"),
                                            Q("0m"))

         mod_pos3 = geom.structure.Position( 'modpos3'+self.name,
                                           +0.5*Q("0.04m")*42+Q("0.035m"),
                                           Q("0m"),
                                           Q("0m"))

         modup_ri_pla2 = geom.structure.Placement( 'modupri2pla'+self.name, volume=  ModuleBoxup_lv, pos=mod_pos2, rot = Mod_ri_rot )
         modup_left_pla2 = geom.structure.Placement( 'modupleft2pla'+self.name, volume=  ModuleBoxup_lv, pos=mod_pos2, rot = Mod_left_rot)
         modup_ri_pla3 = geom.structure.Placement( 'modupripla3'+self.name, volume=  ModuleBoxup_lv, pos=mod_pos3, rot = Mod_ri_rot)
         modup_left_pla3 = geom.structure.Placement( 'modupleft3pla'+self.name, volume=  ModuleBoxup_lv, pos=mod_pos3, rot = Mod_left_rot)

        
         Module_layerup_lv.placements.append(modup_ri_pla2.name)
         Module_layerup_lv.placements.append(modup_left_pla2.name)
         Module_layerup_lv.placements.append(modup_ri_pla3.name)
         Module_layerup_lv.placements.append(modup_left_pla3.name)

         
         #Module_layerup_lv.params.append(("BField",self.BFieldUp))
         Module_layerup_lv.params.append(("BField",B_fieldup_left_rot))
         Module_layerup_lv.params.append(("BField",B_fieldup_ri_rot))
         


         #Place Layers into MagneticBox2                                                                                                                                                                           
         Module_layers_thin = 39
         thinModlayer_pos = [geom.structure.Position('o')]*Module_layers_thin
         thin_Modlayer_pla = [geom.structure.Placement('p', volume=Module_layerup_lv, pos=thinModlayer_pos[1])]*Module_layers_thin

         for iter in range(0,Module_layers_thin):
             x = Q("0m")
             y = Q("0m")
             zpos = -Q("3.4645m")+Q("0.0275m") +iter * Q("0.055m")
             thinModlayer_pos[iter] = geom.structure.Position( 'thinModlayerposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("0m"),
                                                           z = zpos)
             thin_Modlayer_pla[iter] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(iter), volume=Module_layerup_lv, pos=thinModlayer_pos[iter] )
             MagneticBox2_lv.placements.append(thin_Modlayer_pla[iter].name)


        #Place Layers into RMS vol between thick layers                                                                                                                                                     
         Module_layers_thick = 59
         thickModlayer_pos = [geom.structure.Position('q')]*Module_layers_thick

         thick_Modlayer_pla = [geom.structure.Placement('r',volume=Module_layerup_lv,pos=thickModlayer_pos[1])]*Module_layers_thick

         for iter in range(0,Module_layers_thick):
             x = Q("0m")
             y = Q("0m")
             zpos = -Q("1.292m")+ Q("0.040m")  +iter * Q("0.08m")

             thickModlayer_pos[iter] = geom.structure.Position( 'thickModlayerposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("0m"),
                                                           z = zpos)
             thick_Modlayer_pla[iter] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(iter), volume=Module_layerup_lv, pos=thickModlayer_pos[iter] )
             MagneticBox2_lv.placements.append(thick_Modlayer_pla[iter].name) 
         self.add_volume(rmms_lv)
         return
        
