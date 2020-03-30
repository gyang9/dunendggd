gegede-cli ../duneggd/Config/ArgonCube2x2/ArgonCube2x2.cfg ../duneggd/Config/ArgonCube2x2/DETENCLOSURE_OpticalDet.cfg ../duneggd/Config/WORLDggd.cfg -w World -o OpticalDet.gdml
root -l 'materialDisplay.C("OpticalDet.gdml")'
