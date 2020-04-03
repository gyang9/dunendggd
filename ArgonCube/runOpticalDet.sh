gegede-cli ../duneggd/Config/ArgonCube/ArgonCube_2x2.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_OpticalDet.cfg ../duneggd/Config/WORLDggd.cfg -w World -o OpticalDet.gdml
root -l 'materialDisplay.C("OpticalDet.gdml")'
