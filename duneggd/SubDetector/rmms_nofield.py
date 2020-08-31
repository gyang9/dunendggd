#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q
global Pos
class rmmsBuilder(gegede.builder.Builder):
    
    def configure(self, mat = None, thinbox1Dimension = None, thinbox2Dimension = None, magneticbox1Dimension = None, magneticbox2Dimension = None, gapPosition = None, BFieldUp = None, BFieldDown = None,  **kwds):
        self.BFieldUp = BFieldUp
        self.BFieldDown = BFieldDown
        self.magneticbox1Dimension =  magneticbox1Dimension
        self.magneticbox2Dimension = magneticbox2Dimension
        self.mat=mat
        self.thinbox1Dimension=thinbox1Dimension
        self.thinbox2Dimension=thinbox2Dimension
        self.gapPosition=gapPosition
    
        
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

         #scinBoxdown_lv.params.append(('BField',self.BFieldDown))
         #scinBoxup_lv.params.append(('BField',self.BFieldUp))

         
         #Logical volumes for Magnetic Boxes

         MagneticBox1_lv = geom.structure.Volume( 'Maneticvol1'+self.name, material=self.mat, shape=MagneticBox1 )
         MagneticBox2_lv = geom.structure.Volume( 'Magneticvol2'+self.name, material=self.mat, shape=MagneticBox2 )

         #MagneticBox1_lv.params.append(('BField',self.BFieldDown))
         #MagneticBox2_lv.params.append(('BField',self.BFieldUp))
         # Logical volumes for steel Boxes

         thinBox1_lv = geom.structure.Volume( 'thinvol'+self.name, material=self.mat, shape=thinBox1 )
         thinBox2_lv = geom.structure.Volume( 'thinvol2'+self.name, material=self.mat, shape=thinBox2 )
         thickBox1_lv = geom.structure.Volume( 'thickvol'+self.name, material=self.mat, shape=thickBox1 )
         thickBox2_lv = geom.structure.Volume( 'thickvol2'+self.name, material=self.mat, shape=thickBox2 )                                                                                                 
         
         #thinBox1_lv.params.append(('BField',self.BFieldDown))
         #thickBox1_lv.params.append(('BField',self.BFieldDown))
         #thinBox2_lv.params.append(('BField',self.BFieldUp))
         #thickBox2_lv.params.append(('BField',self.BFieldUp))
         

         #Poition Magneticbox in rmms volumes                                                                                                                                                                                                                                                                                        
         lf_pos_Mag = geom.structure.Position( 'lfposMag'+self.name,
                                          0.5*(self.magneticbox1Dimension[0]+self.magneticbox2Dimension[0])+self.gapPosition[0],
                                          Q("0m"),
                                          Q("0m"))

         rt_pos_Mag = geom.structure.Position( 'rtposMag'+self.name,
                                          -(0.5*(self.magneticbox1Dimension[0]+self.magneticbox2Dimension[0])+self.gapPosition[0]),
                                          Q("0m"),
                                          Q("0m"))

         ctr_pos_Mag = geom.structure.Position( 'ctrposMag'+self.name,
                                           Q("0m"),
                                           Q("0m"),
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
            y = Q("1.8125m")
            zpos = -Q("3.4645m")+ iter * Q("0.055m")
            thinBox1_pos[iter] = geom.structure.Position( 'thinBox1position'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
                                                           z = zpos)
           
            thinBox1_pla[iter] = geom.structure.Placement('thinBox1pla'+self.name+str(iter), volume = thinBox1_lv, pos = thinBox1_pos[iter]) 
            MagneticBox1_lv.placements.append(thinBox1_pla[iter].name)
           
        #ThickBox1 Placements in Magnetic Box1                                                                                                                                                                                       
         m_Boxes = 60
         thickBox1_pos = [geom.structure.Position('c')]*m_Boxes

         thick_Box1_pla = [geom.structure.Placement('d',volume = thickBox1_lv, pos = thickBox1_pos[1])]*m_Boxes

         for iter in range(0,m_Boxes):
             x = Q("0m")
             y = Q("1.8125m")
             wpos = -Q("1.292m")+ iter * Q("0.08m")
             thickBox1_pos[iter] = geom.structure.Position( 'thickBox1position'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
                                                           z = wpos)
             thick_Box1_pla[iter] = geom.structure.Placement( 'thickBox1pla'+self.name+str(iter), volume = thickBox1_lv, pos = thickBox1_pos[iter] )
             MagneticBox1_lv.placements.append(thick_Box1_pla[iter].name)


        #Adding steelBox in magnetic volumes2 (ThinsteelBox2)
         o_Boxes = 40
         thinBox2_pos = [geom.structure.Position('e')]*o_Boxes
         thinBox2_pla = [geom.structure.Placement('f',volume = thinBox2_lv, pos=thinBox2_pos[1])]*o_Boxes

         for iter in range(0,o_Boxes):
             x = Q("0m")
             y = Q("1.8125m")
             zpos = -Q("3.4645m")+ iter * Q("0.055m")
             thinBox2_pos[iter] = geom.structure.Position( 'thinBox2position'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
                                                           z = zpos)

             thinBox2_pla[iter] = geom.structure.Placement('thinBox2pla'+self.name+str(iter), volume = thinBox2_lv, pos= thinBox2_pos[iter])
             MagneticBox2_lv.placements.append(thinBox2_pla[iter].name)
        #ThickBox Placements in Magenetic volumes2(ThicksteelBox2)
         p_Boxes = 60
         thickBox2_pos = [geom.structure.Position('g')]*p_Boxes

         thick_Box2_pla = [geom.structure.Placement('h',volume = thickBox2_lv, pos=thickBox2_pos[1])]*p_Boxes

         for iter in range(0,p_Boxes):
             x = Q("0m")
             y = Q("1.8125m")
             wpos = -Q("1.292m")+ iter * Q("0.08m")
             thickBox2_pos[iter] = geom.structure.Position( 'thickBox2position'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
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
         thinModbox_pos = [geom.structure.Position('k')]*Module_boxes_thin
         thin_Modbox_pla = [geom.structure.Placement('l', volume = ModuleBoxdown_lv, pos=thinModbox_pos[1])]*Module_boxes_thin

         for iter in range(0,Module_boxes_thin):
             x = Q("0m")
             y = Q("1.8125m")
             zpos = -Q("3.4645m")+Q("0.0275m") +iter * Q("0.055m")
             thinModbox_pos[iter] = geom.structure.Position( 'thinModboxposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
                                                           z = zpos)
             thin_Modbox_pla[iter] = geom.structure.Placement( 'thinModboxpla'+self.name+str(iter), volume = ModuleBoxdown_lv, pos=thinModbox_pos[iter] )
             MagneticBox1_lv.placements.append(thin_Modbox_pla[iter].name)

         Module_boxes_thick = 59
         thickModbox_pos = [geom.structure.Position('m')]*Module_boxes_thick

         thick_Modbox_pla = [geom.structure.Placement('n',volume = ModuleBoxdown_lv, pos=thickModbox_pos[1])]*Module_boxes_thick

         for iter in range(0,Module_boxes_thick):
             x = Q("0m")
             y = Q("1.8125m")
             zpos = -Q("1.292m")+ Q("0.040m")  +iter * Q("0.08m")

             thickModbox_pos[iter] = geom.structure.Position( 'thickModboxposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
                                                           z = zpos)
             thick_Modbox_pla[iter] = geom.structure.Placement( 'thickModboxpla'+self.name+str(iter), volume = ModuleBoxdown_lv, pos=thickModbox_pos[iter] )
             MagneticBox1_lv.placements.append(thick_Modbox_pla[iter].name)
            
                                            
        #Place Modules into scint layers                                                                                                                                                                    
         Module_layer = geom.shapes.Box( 'Modulelayerbox',
                                         dx = 0.5*Q("3.43m"),
                                         dy = 0.5*Q("3.2m"),
                                         dz = 0.5*Q("0.040m"))

         Module_layerup_lv = geom.structure.Volume( 'modulelayerupvol', material='NoGas', shape=Module_layer )
         

                 #Poition modules in layer volumes                                                                                                                                                                  

         mod_pos2 = geom.structure.Position( 'modpos2'+self.name,
                                            -0.5*Q("0.04m")*42-Q("0.035m"),
                                            Q("0m"),
                                            Q("0m"))

         mod_pos3 = geom.structure.Position( 'modpos3'+self.name,
                                           +0.5*Q("0.04m")*42+Q("0.035m"),
                                           Q("0m"),
                                           Q("0m"))

         modup_pla2 = geom.structure.Placement( 'modup2pla'+self.name, volume=  ModuleBoxup_lv, pos=mod_pos2)
         modup_pla3 = geom.structure.Placement( 'modup3pla'+self.name, volume=  ModuleBoxup_lv, pos=mod_pos3)

        
         Module_layerup_lv.placements.append(modup_pla2.name)
         Module_layerup_lv.placements.append(modup_pla3.name)
         
         #Module_layerup_lv.params.append(('BField',self.BFieldUp))
         


         #Place Layers into MagneticBox2                                                                                                                                                                           
         Module_layers_thin = 39
         thinModlayer_pos = [geom.structure.Position('o')]*Module_layers_thin
         thin_Modlayer_pla = [geom.structure.Placement('p', volume=Module_layerup_lv, pos=thinModlayer_pos[1])]*Module_layers_thin

         for iter in range(0,Module_layers_thin):
             x = Q("0m")
             y = Q("1.8125m")
             zpos = -Q("3.4645m")+Q("0.0275m") +iter * Q("0.055m")
             thinModlayer_pos[iter] = geom.structure.Position( 'thinModlayerposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
                                                           z = zpos)
             thin_Modlayer_pla[iter] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(iter), volume=Module_layerup_lv, pos=thinModlayer_pos[iter] )
             MagneticBox2_lv.placements.append(thin_Modlayer_pla[iter].name)


        #Place Layers into RMS vol between thick layers                                                                                                                                                     
         Module_layers_thick = 59
         thickModlayer_pos = [geom.structure.Position('q')]*Module_layers_thick

         thick_Modlayer_pla = [geom.structure.Placement('r',volume=Module_layerup_lv,pos=thickModlayer_pos[1])]*Module_layers_thick

         for iter in range(0,Module_layers_thick):
             x = Q("0m")
             y = Q("1.8125m")
             zpos = -Q("1.292m")+ Q("0.040m")  +iter * Q("0.08m")

             thickModlayer_pos[iter] = geom.structure.Position( 'thickModlayerposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
                                                           z = zpos)
             thick_Modlayer_pla[iter] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(iter), volume=Module_layerup_lv, pos=thickModlayer_pos[iter] )
             MagneticBox2_lv.placements.append(thick_Modlayer_pla[iter].name) 
         self.add_volume(rmms_lv)
         return
        
