gegede-cli ../duneggd/Config/ArgonCube/*.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_HalfTPC.cfg ../duneggd/Config/WORLDggd.cfg -w World -o HalfTPC.gdml
root -l 'materialDisplay.C("HalfTPC.gdml")'
