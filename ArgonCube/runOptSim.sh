gegede-cli ../duneggd/Config/ArgonCube/*.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_OptSim.cfg ../duneggd/Config/WORLDggd.cfg -w World -o optSim.gdml
root -l 'materialDisplay.C("optSim.gdml")'
