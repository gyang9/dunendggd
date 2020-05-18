gegede-cli ../duneggd/Config/ArgonCube/OptSim.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_OpticalDetL.cfg ../duneggd/Config/WORLDggd.cfg -w World -o OpticalDetL.gdml
root -l 'materialDisplay.C("OpticalDetL.gdml")'
