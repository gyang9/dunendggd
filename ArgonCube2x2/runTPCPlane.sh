gegede-cli ../duneggd/Config/ArgonCube2x2/ArgonCube2x2.cfg ../duneggd/Config/ArgonCube2x2/DETENCLOSURE_TPCPlane.cfg ../duneggd/Config/WORLDggd.cfg -w World -o TPCPlane.gdml
root -l 'materialDisplay.C("TPCPlane.gdml")'
