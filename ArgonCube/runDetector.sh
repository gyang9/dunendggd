gegede-cli ../duneggd/Config/ArgonCube/ArgonCube_2x2.cfg ../duneggd/Config/ArgonCube/DETENCLOSURE_Detector.cfg ../duneggd/Config/WORLDggd.cfg -w World -o Detector.gdml
root -l 'materialDisplay.C("Detector.gdml")'
