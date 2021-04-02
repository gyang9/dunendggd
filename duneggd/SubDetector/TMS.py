#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q
global Pos
class rmmsBuilder(gegede.builder.Builder):
    def configure(self, mat=None, thinbox1Dimension=None, thinbox2Dimension=None, gapPosition=None, BFieldUpLow = None, BFieldUpHigh = None, BFieldDownLow = None , BFieldDownHigh = None,  **kwds):
        self.BFieldUpLow = BFieldUpLow
        self.BFieldUpHigh = BFieldUpHigh
        self.BFieldDownLow = BFieldDownLow 
        self.BFieldDownHigh = BFieldDownHigh
        self.mat=mat
        self.thinbox1Dimension=thinbox1Dimension
        self.thinbox2Dimension=thinbox2Dimension
        self.gapPosition=gapPosition
        
        
    def construct(self, geom):        
            
        #Make Boxes for steel and logical volumes

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



        thin_layer = geom.shapes.Box( 'thinlayerbox',
                                      dx = 0.5*Q("7.036m"),
                                      dy = 0.5*Q("5.022m"),
                                      dz = 0.5*Q("0.015m"))
        thick_layer = geom.shapes.Box( 'thicklayerbox',
                                      dx = 0.5*Q("7.036m"),
                                      dy = 0.5*Q("5.022m"),
                                      dz = 0.5*Q("0.040m"))
        
        rmmsbox = geom.shapes.Box( 'rmmsbox',
                                   dx = 0.5*Q("7.036m"),
                                   dy = 0.5*Q("8.825m"),
                                   dz = 0.5*Q("7m"))
        
        
        thinBox1_lv = geom.structure.Volume( 'thinvol'+self.name, material=self.mat, shape=thinBox1 )
        thinBox2_lv = geom.structure.Volume( 'thinvol2'+self.name, material=self.mat, shape=thinBox2 )
        thickBox1_lv = geom.structure.Volume( 'thickvol'+self.name, material=self.mat, shape=thickBox1 )
        thickBox2_lv = geom.structure.Volume( 'thickvol2'+self.name, material=self.mat, shape=thickBox2 )
        thinBox1_lv.params.append(('BField',self.BFieldDownHigh))
        thinBox2_lv.params.append(('BField',self.BFieldUpHigh))
        thickBox1_lv.params.append(('BField',self.BFieldDownLow))
        thickBox2_lv.params.append(('BField',self.BFieldUpLow))

        #Adding different magnetic field for four different steel plates

        #thinBox1_lv.params.append(('BField',self.BFieldUpHigh))
        #thinBox2_lv.params.append(('BField',self.BFieldDownHigh))
        #thickBox1_lv.params.append(('BField',self.BFieldUpLow))
        #thickBox2_lv.params.append(('BField',self.BFieldDownLow))
            

        thin_layer_lv = geom.structure.Volume( 'thinlayervol', material='air', shape=thin_layer )
        thick_layer_lv = geom.structure.Volume( 'thicklayervol', material='air', shape=thick_layer )
        rmms_lv = geom.structure.Volume( 'vol'+self.name, material=self.mat, shape=rmmsbox )
            
        #Poition steel in layer volumes (Thin)
            
        lf_pos = geom.structure.Position( 'lfpos'+self.name,
                                          0.5*(self.thinbox1Dimension[0]+self.thinbox2Dimension[0])+self.gapPosition[0],
                                          Q("0m"),
                                          Q("0m"))
        
        rt_pos = geom.structure.Position( 'rtpos'+self.name,
                                          -(0.5*(self.thinbox1Dimension[0]+self.thinbox2Dimension[0])+self.gapPosition[0]),
                                          Q("0m"),
                                          Q("0m"))
            
        ctr_pos = geom.structure.Position( 'ctrpos'+self.name,
                                           Q("0m"),
                                           Q("0m"),
                                           Q("0m"))
        
        rt_pla = geom.structure.Placement( 'rtpla'+self.name, volume=thinBox1_lv, pos=rt_pos )
        lf_pla = geom.structure.Placement( 'lfpla'+self.name, volume=thinBox1_lv, pos=lf_pos )
        ctr_pla = geom.structure.Placement( 'ctrpla'+self.name, volume=thinBox2_lv, pos=ctr_pos )

        thin_layer_lv.placements.append(rt_pla.name)
        thin_layer_lv.placements.append(lf_pla.name)
        thin_layer_lv.placements.append(ctr_pla.name)



        #Poition steel in layer volumes (Thick)                                                                                                                       
        thick_rt_pla = geom.structure.Placement( 'thickrtpla'+self.name, volume=thickBox1_lv, pos=rt_pos )
        thick_lf_pla = geom.structure.Placement( 'thicklfpla'+self.name, volume=thickBox1_lv, pos=lf_pos )
        thick_ctr_pla = geom.structure.Placement( 'thickctrpla'+self.name, volume=thickBox2_lv, pos=ctr_pos )

        thick_layer_lv.placements.append(thick_rt_pla.name)
        thick_layer_lv.placements.append(thick_lf_pla.name)
        thick_layer_lv.placements.append(thick_ctr_pla.name)

        #Postion layers in RMMS (Will become a for loop)

        #Place thin layers loop
        n_layers = 39
        thinlayer_pos = [geom.structure.Position('a')]*n_layers
        
        
        thin_layer_pla = [geom.structure.Placement('b',volume=thin_layer_lv,pos=thinlayer_pos[1])]*n_layers
        #thin_layer_pla = [geom.structure.Placement('b')]*n_layers

        for iter in range(0,n_layers):
            x = Q("0m")
            y = Q("1.8125m")
            zpos = -Q("3.4645m")+ iter * Q("0.055m")                                                        
            thinlayer_pos[iter] = geom.structure.Position( 'thinlayerposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
                                                           z = zpos)
            thin_layer_pla[iter] = geom.structure.Placement( 'thinlayerpla'+self.name+str(iter), volume=thin_layer_lv, pos=thinlayer_pos[iter] )
            rmms_lv.placements.append(thin_layer_pla[iter].name)

        #Thick Layer Placement
        m_layers = 60
        thicklayer_pos = [geom.structure.Position('c')]*m_layers
        
        thick_layer_pla = [geom.structure.Placement('d',volume=thick_layer_lv, pos=thicklayer_pos[1])]*m_layers
        
        for iter in range(0,m_layers):
            x = Q("0m")
            y = Q("1.8125m")
            wpos = -Q("1.307m")+ iter * Q("0.08m") #subtrack 0.015 m from wpos = -Q("1.292m") 
            thicklayer_pos[iter] = geom.structure.Position( 'thicklayerposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
                                                           z = wpos)
            thick_layer_pla[iter] = geom.structure.Placement( 'thicklayerpla'+self.name+str(iter), volume=thick_layer_lv, pos=thicklayer_pos[iter] )
            rmms_lv.placements.append(thick_layer_pla[iter].name)
        

        #MAKE AND PLACE SCINTILATOR
        #Make Scint Bar
        scinBox = geom.shapes.Box( 'scinbox'+self.name,
                                    dx = 0.5*Q("0.03542m"),
                                    dy = 0.5*Q("3.096m"),
                                    dz = 0.5*Q("0.01m"))

        scinBox_lv = geom.structure.Volume( 'scinBoxlv'+self.name, material='Scintillator', shape=scinBox)
        scinBox_lv.params.append(("SensDet", rmms_lv.name))

        #Place Bars into Modules
        ModuleBox = geom.shapes.Box( 'ModuleBox',
                                     dx = 0.5*Q("0.03542m")*48, # 0.04*42
                                     dy = 0.5*Q("3.096m"),
                                     dz = 0.5*Q("0.01m"))
        ModuleBox_lv = geom.structure.Volume( 'ModuleBoxvol', material='air', shape=ModuleBox )
                                                                                                                                           
        sci_bars = 48
        sci_Bar_pos = [geom.structure.Position('e')]*sci_bars

        sci_Bar_pla = [geom.structure.Placement('f',volume=scinBox_lv, pos=sci_Bar_pos[1])]*m_layers

        for iter in range(0,sci_bars):
            z = Q("0m") 
            y = Q("0m")
            xpos = -Q("0.83237m")+ iter * Q("0.03542m")
            sci_Bar_pos[iter] = geom.structure.Position( 'sci_barposition'+str(iter),
                                                           x = xpos,
                                                           y = Q("0m"),
                                                           z = Q("0m"))
            sci_Bar_pla[iter] = geom.structure.Placement( 'scibarpla'+self.name+str(iter), volume=scinBox_lv, pos=sci_Bar_pos[iter] )
            ModuleBox_lv.placements.append(sci_Bar_pla[iter].name)

        #Place Modules into scint layers
        modules_in_layer = 4
        Module_layer = geom.shapes.Box( 'Modulelayerbox',
                                      dx = 0.5*Q("7.036m"), #7.04 
                                      dy = 0.5*Q("5.022m"),
                                      dz = 0.5*Q("0.040m"))        

        Module_layer_lv = geom.structure.Volume( 'modulelayervol', material='air', shape=Module_layer )

         #Poition modules in layer volumes                                                                                                                         
         
        Mod_ri_rot = geom.structure.Rotation( 'Modrirot', '0deg','0deg','3deg')
        Mod_left_rot = geom.structure.Rotation( 'Modleftrot', '0deg','0deg','-3deg')

        mod_pos1 = geom.structure.Position( 'modpos1'+self.name,
                                          -1.5*Q("0.03542m")*48-Q("0.015m"),
                                          Q("0m"),
                                          Q("0m"))

        mod_pos2 = geom.structure.Position( 'modpos2'+self.name,
                                            -0.5*Q("0.03542m")*48-Q("0.005m"),
                                            Q("0m"),
                                            Q("0m"))

        mod_pos3 = geom.structure.Position( 'modpos3'+self.name,
                                           +0.5*Q("0.03542m")*48+Q("0.005m"),
                                           Q("0m"),
                                           Q("0m"))

        mod_pos4 = geom.structure.Position( 'modpos4'+self.name,
                                            +1.5*Q("0.03542m")*48+Q("0.015m"),
                                            Q("0m"),
                                            Q("0m"))




        mod_ri_pla1 = geom.structure.Placement( 'modripla1'+self.name, volume=  ModuleBox_lv, pos=mod_pos1, rot = Mod_ri_rot)
        mod_le_pla1 = geom.structure.Placement( 'modlepla1'+self.name, volume=  ModuleBox_lv, pos=mod_pos1, rot = Mod_left_rot)

        #mod_pla1 = geom.structure.Placement( 'mod1pla'+self.name, volume=  ModuleBox_lv, pos=mod_pos1)
        mod_ri_pla2 = geom.structure.Placement( 'modripla2'+self.name, volume=  ModuleBox_lv, pos=mod_pos2, rot = Mod_ri_rot)
        mod_le_pla2 = geom.structure.Placement( 'modlepla2'+self.name, volume=  ModuleBox_lv, pos=mod_pos2, rot = Mod_left_rot)

        #mod_pla2 = geom.structure.Placement( 'mod2pla'+self.name, volume=  ModuleBox_lv, pos=mod_pos2)
        mod_ri_pla3 = geom.structure.Placement( 'modripla3'+self.name, volume=  ModuleBox_lv, pos=mod_pos3, rot = Mod_ri_rot)
        mod_le_pla3 = geom.structure.Placement( 'modlepla3'+self.name, volume=  ModuleBox_lv, pos=mod_pos3, rot = Mod_left_rot)

        mod_ri_pla4 = geom.structure.Placement( 'modripla4'+self.name, volume=  ModuleBox_lv, pos=mod_pos4, rot = Mod_ri_rot)
        mod_le_pla4 = geom.structure.Placement( 'modlepla4'+self.name, volume=  ModuleBox_lv, pos=mod_pos4, rot = Mod_left_rot)

        #mod_pla3 = geom.structure.Placement( 'mod3pla'+self.name, volume=  ModuleBox_lv, pos=mod_pos3)
        #mod_pla4 = geom.structure.Placement( 'mod4pla'+self.name, volume=  ModuleBox_lv, pos=mod_pos4)

        #Module_layer_lv.placements.append(mod_pla1.name)
        Module_layer_lv.placements.append(mod_ri_pla1.name)
        Module_layer_lv.placements.append(mod_le_pla1.name)

        Module_layer_lv.placements.append(mod_ri_pla2.name)
        Module_layer_lv.placements.append(mod_le_pla2.name)

        Module_layer_lv.placements.append(mod_ri_pla3.name)
        Module_layer_lv.placements.append(mod_le_pla3.name)

        Module_layer_lv.placements.append(mod_ri_pla4.name)
        Module_layer_lv.placements.append(mod_le_pla4.name)

        #Module_layer_lv.placements.append(mod_pla2.name)
        #Module_layer_lv.placements.append(mod_pla3.name)
        #Module_layer_lv.placements.append(mod_pla4.name)

        #Place Layers into RMS vol
        Module_layers_thin = 40
        thinModlayer_pos = [geom.structure.Position('g')]*Module_layers_thin

        thin_Modlayer_pla = [geom.structure.Placement('h',volume=Module_layer_lv,pos=thinModlayer_pos[1])]*Module_layers_thin
        #thin_layer_pla = [geom.structure.Placement('b')]*n_layers                                                 

        for iter in range(0,Module_layers_thin):
            x = Q("0m")
            y = Q("1.8125m")
            zpos = -Q("3.4645m") -Q("0.0275m") +iter * Q("0.055m")
            thinModlayer_pos[iter] = geom.structure.Position( 'thinModlayerposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
                                                           z = zpos)
            thin_Modlayer_pla[iter] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(iter), volume=Module_layer_lv, pos=thinModlayer_pos[iter] )
            rmms_lv.placements.append(thin_Modlayer_pla[iter].name)


        #Place Layers into RMS vol between thick layers                                                                                 
        Module_layers_thick = 59
        thickModlayer_pos = [geom.structure.Position('i')]*Module_layers_thick

        thick_Modlayer_pla = [geom.structure.Placement('j',volume=Module_layer_lv,pos=thickModlayer_pos[1])]*Module_layers_thick
            
        for iter in range(0,Module_layers_thick):
            x = Q("0m")
            y = Q("1.8125m")
            zpos = -Q("1.292m") + Q("0.025m")  +iter * Q("0.08m") # subtract 0.015m from zpos=-Q("1.292m")+Q("0.040m")

            thickModlayer_pos[iter] = geom.structure.Position( 'thickModlayerposition'+str(iter),
                                                           x = Q("0m"),
                                                           y = Q("1.8125m"),
                                                           z = zpos)
            thick_Modlayer_pla[iter] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(iter), volume=Module_layer_lv, pos=thickModlayer_pos[iter] )
            rmms_lv.placements.append(thick_Modlayer_pla[iter].name)







        #Add RMMS to self

        #self.add_volume(rmms_lv.name)
        self.add_volume(rmms_lv)    
        return 
        
        
