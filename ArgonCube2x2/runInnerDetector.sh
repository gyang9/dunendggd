gegede-cli ../duneggd/Config/ArgonCube2x2/ArgonCube2x2.cfg ../duneggd/Config/ArgonCube2x2/DETENCLOSURE_InnerDetector.cfg ../duneggd/Config/WORLDggd.cfg -w World -o InnerDetector.gdml
root -l 'materialDisplay.C("InnerDetector.gdml")'
