gegede-cli ../duneggd/Config/ArgonCube/DUNE_ND.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_Detector.cfg ../duneggd/Config/WORLDggd.cfg -w World -o ND.gdml
root -l 'materialDisplay.C("ND.gdml")'
