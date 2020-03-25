gegede-cli ../duneggd/Config/ArgonCube2x2/*.cfg ../duneggd/Config/ArgonCube2x2/DETENCLOSURE_OptSim.cfg ../duneggd/Config/WORLDggd.cfg -w World -o optSim.gdml
root -l 'materialDisplay.C("optSim.gdml")'
