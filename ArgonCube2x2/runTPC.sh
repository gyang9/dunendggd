gegede-cli ../duneggd/Config/ArgonCube2x2/ArgonCube2x2.cfg ../duneggd/Config/ArgonCube2x2/DETENCLOSURE_TPC.cfg ../duneggd/Config/WORLDggd.cfg -w World -o TPC.gdml
root -l 'materialDisplay.C("TPC.gdml")'
