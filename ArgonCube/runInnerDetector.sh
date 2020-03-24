gegede-cli ../duneggd/Config/ArgonCube/*.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_InnerDetector.cfg ../duneggd/Config/WORLDggd.cfg -w World -o InnerDetector.gdml
root -l 'materialDisplay.C("InnerDetector.gdml")'
