gegede-cli ../duneggd/Config/ArgonCube/ArgonCube_2x2.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_TPC.cfg ../duneggd/Config/WORLDggd.cfg -w World -o TPC.gdml
root -l 'materialDisplay.C("TPC.gdml")'
