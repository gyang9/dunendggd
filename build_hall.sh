#! /bin/bash
#

gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/MPD_Concept.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/*.cfg \
	   -w World -o test.gdml
