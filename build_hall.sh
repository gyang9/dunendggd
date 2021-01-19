#! /bin/bash

# use the first argument to indicate what we should build
# if no argument build everything
option=$1
if [ -z $option ];
then
  option="all"
fi

# build the full hall
if [ $option = "all" -o $option = "full" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeActiveModule.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeModule.cfg \
	   duneggd/Config/ArgonCube/BottomStructure.cfg \
	   duneggd/Config/ArgonCube/FrontStructure.cfg \
	   duneggd/Config/ArgonCube/SideStructure.cfg \
	   -w World -o nd_hall_with_dets.gdml
fi

if [ $option = "all" -o $option = "3DST_STT" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/KLOE_with_3DST_STT.cfg \
           duneggd/Config/KLOEEMCALO.cfg \
           duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/ArgonCube/ArgonCubeActiveModule.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           duneggd/Config/ArgonCube/ArgonCubeModule.cfg \
           duneggd/Config/ArgonCube/BottomStructure.cfg \
           duneggd/Config/ArgonCube/FrontStructure.cfg \
           duneggd/Config/ArgonCube/SideStructure.cfg \
           -w World -o nd_hall_with_3DST_STT.gdml
fi

# build a hall with no detectors
if [ $option = "all" -o $option = "empty" ];
then

gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_NoDets.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   -w World -o nd_hall_no_dets.gdml
fi

if [ $option = "all" -o $option = "lar" ];
then
# build a hall with only LAr
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_LAr.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeActiveModule.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeModule.cfg \
	   duneggd/Config/ArgonCube/BottomStructure.cfg \
	   duneggd/Config/ArgonCube/FrontStructure.cfg \
	   duneggd/Config/ArgonCube/SideStructure.cfg \
	   -w World -o nd_hall_only_lar.gdml
fi
# anti-fiducial LAr
if [ $option = "all" -o $option = "lar_antifid" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_LAr.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeActiveModule.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeModuleNoActive.cfg \
	   duneggd/Config/ArgonCube/BottomStructure.cfg \
	   duneggd/Config/ArgonCube/FrontStructure.cfg \
	   duneggd/Config/ArgonCube/SideStructure.cfg \
	   -w World -o nd_hall_lar_antifid.gdml
fi

# MPD only
if [ $option = "all" -o $option = "mpd" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_MPD.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeActiveModule.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeModule.cfg \
	   duneggd/Config/ArgonCube/BottomStructure.cfg \
	   duneggd/Config/ArgonCube/FrontStructure.cfg \
	   duneggd/Config/ArgonCube/SideStructure.cfg \
	   -w World -o nd_hall_only_mpd.gdml
fi

# MPD anti-fiducial
if [ $option = "all" -o $option = "mpd_antifid" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_MPD.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID_noTPC.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeActiveModule.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeModule.cfg \
	   duneggd/Config/ArgonCube/BottomStructure.cfg \
	   duneggd/Config/ArgonCube/FrontStructure.cfg \
	   duneggd/Config/ArgonCube/SideStructure.cfg \
	   -w World -o nd_hall_only_mpd_antifid.gdml
fi


# KLOE only
if [ $option = "all" -o $option = "kloe" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_KLOE.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeActiveModule.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeModule.cfg \
	   duneggd/Config/ArgonCube/BottomStructure.cfg \
	   duneggd/Config/ArgonCube/FrontStructure.cfg \
	   duneggd/Config/ArgonCube/SideStructure.cfg \
	   -w World -o nd_hall_only_kloe.gdml
fi

# KLOE filled with STT
if [ $option = "all" -o $option = "kloe_sttonly" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume_Only_KLOE.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/KLOE_STTFULL.cfg \
           duneggd/Config/KLOEEMCALO.cfg \
           duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/ArgonCube/ArgonCubeActiveModule.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           duneggd/Config/ArgonCube/ArgonCubeModule.cfg \
           duneggd/Config/ArgonCube/BottomStructure.cfg \
           duneggd/Config/ArgonCube/FrontStructure.cfg \
           duneggd/Config/ArgonCube/SideStructure.cfg \
           -w World -o nd_hall_kloe_sttonly.gdml
fi

# KLOE anti-fiducial
if [ $option = "all" -o $option = "kloe_antifid" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_KLOE.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_No_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeActiveModule.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeModule.cfg \
	   duneggd/Config/ArgonCube/BottomStructure.cfg \
	   duneggd/Config/ArgonCube/FrontStructure.cfg \
	   duneggd/Config/ArgonCube/SideStructure.cfg \
	   -w World -o nd_hall_only_kloe_antifid.gdml
fi

# LAr and MPD (No KLOE)
if [ $option = "all" -o $option = "lar_mpd" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_No_KLOE.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeActiveModule.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeModule.cfg \
	   duneggd/Config/ArgonCube/BottomStructure.cfg \
	   duneggd/Config/ArgonCube/FrontStructure.cfg \
	   duneggd/Config/ArgonCube/SideStructure.cfg \
	   -w World -o nd_hall_lar_mpd.gdml
fi

# LAr and MPD anti-fiducial (for MPD)
if [ $option = "all" -o $option = "lar_mpd_antifid" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_No_KLOE.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID_noTPC.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeActiveModule.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeModule.cfg \
	   duneggd/Config/ArgonCube/BottomStructure.cfg \
	   duneggd/Config/ArgonCube/FrontStructure.cfg \
	   duneggd/Config/ArgonCube/SideStructure.cfg \
	   -w World -o nd_hall_lar_mpd_antifid.gdml
fi
