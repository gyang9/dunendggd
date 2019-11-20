gegede-cli ../duneggd/Config/ArgonCube/*.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_PhotonSim.cfg ../duneggd/Config/WORLDggd.cfg -w World -o PhotonSim.gdml
root -l 'materialDisplay.C("PhotonSim.gdml")'
