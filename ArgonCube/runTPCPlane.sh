gegede-cli ../duneggd/Config/ArgonCube/*.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_TPCPlane.cfg ../duneggd/Config/WORLDggd.cfg -w World -o TPCPlane.gdml
root -l 'materialDisplay.C("TPCPlane.gdml")'
