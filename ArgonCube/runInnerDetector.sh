gegede-cli ../duneggd/Config/ArgonCube/ArgonCube_2x2.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_InnerDetector.cfg ../duneggd/Config/WORLDggd.cfg -w World -o InnerDetector.gdml
root -l 'materialDisplay.C("InnerDetector.gdml")'
