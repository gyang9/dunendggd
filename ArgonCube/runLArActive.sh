gegede-cli ../duneggd/Config/ArgonCube/*.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_LArActive.cfg ../duneggd/Config/WORLDggd.cfg -w World -o LArActive.gdml
root -l 'materialDisplay.C("LArActive.gdml")'
