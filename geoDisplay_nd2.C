//void geoDisplay_nd(TString test.gdml)
{
	//gSystem->Load("libGdml");
	gSystem->Load("libGeom");
	TGeoManager *geo = new TGeoManager();
	geo->Import("test.gdml");
	geo->DefaultColors();

	geo->SetTopVisible();

	//geo->GetVolume("DetEnclosure_lv")->SetLineColor(kRed);
	geo->GetVolume("DetEnclosure_lv")->SetVisibility(1);
	geo->GetVolume("DetEnclosure_lv")->SetTransparency(20);

	if ( geo->GetVolume("LArD_lv") != NULL )
	{
		geo->GetVolume("LArD_lv")->SetLineColor(kBlue);
		geo->GetVolume("LArD_lv")->SetVisibility(1);
		geo->GetVolume("LArD_lv")->SetTransparency(20);
	}

	if ( geo->GetVolume("Tracker_lv") != NULL )
	{
		geo->GetVolume("Tracker_lv")->SetLineColor(kRed);
		geo->GetVolume("Tracker_lv")->SetVisibility(1);
		geo->GetVolume("Tracker_lv")->SetTransparency(90);
		//geo->GetVolume("Tracker_lv")->SetTransparency(10);
	}
	if ( geo->GetVolume("ECal_lv") != NULL )
	{
		geo->GetVolume("ECal_lv")->SetLineColor(kMagenta);
		geo->GetVolume("ECal_lv")->SetVisibility(1);
		geo->GetVolume("ECal_lv")->SetTransparency(70);
		//geo->GetVolume("ECal_lv")->SetTransparency(10);
	}

	if ( geo->GetVolume("HCal_lv") != NULL )
	{
		geo->GetVolume("HCal_lv")->SetLineColor(kMagenta);
		geo->GetVolume("HCal_lv")->SetVisibility(1);
		geo->GetVolume("HCal_lv")->SetTransparency(70);
		//geo->GetVolume("HCal_lv")->SetTransparency(10);
	}
	if ( geo->GetVolume("ECalBarrel_lv") != NULL )
	{
		geo->GetVolume("ECalBarrel_lv")->SetLineColor(kPink);
		geo->GetVolume("ECalBarrel_lv")->SetVisibility(1);
		geo->GetVolume("ECalBarrel_lv")->SetTransparency(60);
		//geo->GetVolume("ECalBarrel_lv")->SetTransparency(10);
	}
	if ( geo->GetVolume("Magnet_lv") != NULL )
	{
		geo->GetVolume("Magnet_lv")->SetLineColor(kOrange);
		geo->GetVolume("Magnet_lv")->SetVisibility(1);
		geo->GetVolume("Magnet_lv")->SetTransparency(20);
	}
/*
	//geo->GetVolume("LArD_lv")->SetLineColor(kBlue);
	geo->GetVolume("LArD_lv")->SetVisibility(1);
	geo->GetVolume("LArD_lv")->SetTransparency(20);

	//geo->GetVolume("LArPlane_lv")->SetLineColor(kGray);
	geo->GetVolume("LArPlane_lv")->SetVisibility(1);
	geo->GetVolume("LArPlane_lv")->SetTransparency(20);

	//geo->GetVolume("idWire_lv")->SetLineColor(kGreen);
	geo->GetVolume("idWire_lv")->SetVisibility(1);
	geo->GetVolume("idWire_lv")->SetTransparency(20);
*/
	geo->CheckOverlaps(1e-5,"d");
 	geo->PrintOverlaps();

	geo->SetMaxVisNodes(70000);
	//geo->SetVisLevel(3);
	//geo->SetVisLevel(5);
	geo->ViewLeaves(true);

	geo->GetTopVolume()->Draw("ogl");
	//geo->FindVolumeFast("Tracker_lv")->Draw("ogl");
	//geo->FindVolumeFast("LArD_lv")->Draw("ogl");
	geo->GetTopVolume()->Draw("");
	//
	//
}
