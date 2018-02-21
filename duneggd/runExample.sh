# examples of running DUNENDGGD
#gegede-cli Config/LArTracker.cfg Config/MAINDETggd.cfg Config/DETENCLOSURE-maindet-only.cfg Config/WORLDggd.cfg Config/KLOE.cfg Config/KLOESTT.cfg Config/MuID_end.cfg -w World -o example0.gdml
#gegede-cli Config/WORLDggd.cfg Config/DETENCLOSURE_MuID_test.cfg Config/MuID_end.cfg -w World -o example.gdml

#v4 argoncube kloe stt
gegede-cli duneggd/Config/DETENCLOSURE_concept1_all.cfg duneggd/Config/KLOE.cfg duneggd/Config/KLOESTT.cfg duneggd/Config/ArgonCube/*.cfg duneggd/Config/WORLDggd.cfg -w World -o example.gdml

#v4 argoncube dipole gartpc
gegede-cli duneggd/Config/DETENCLOSURE_concept2_gar.cfg duneggd/Config/KLOE.cfg duneggd/Config/KLOESTT.cfg duneggd/Config/ArgonCube/*.cfg duneggd/Config/WORLDggd.cfg -w World -o example2.gdml
