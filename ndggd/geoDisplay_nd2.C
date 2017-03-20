//void geoDisplay_nd(TString test.gdml)
{
	//gSystem->Load("libGdml");
	gSystem->Load("libGeom");
	TGeoManager *geo = new TGeoManager();
	geo->Import("test.gdml");
	geo->DefaultColors();

	geo->SetTopVisible();

	//geo->GetVolume("volMagnetInner")->SetLineColor(kRed);
	geo->GetVolume("volSecondary")->SetVisibility(1);
	geo->GetVolume("volSecondary")->SetTransparency(20);
/*
	if ( geo->GetVolume("volMuIDBarrel") != NULL )
	{
		geo->GetVolume("volMuIDBarrel")->SetLineColor(kBlue);
		geo->GetVolume("volMuIDBarrel")->SetVisibility(1);
		geo->GetVolume("volMuIDBarrel")->SetTransparency(20);
	}

	if ( geo->GetVolume("volMuIDUpstream") != NULL )
	{
		geo->GetVolume("volMuIDUpstream")->SetLineColor(kRed);
		geo->GetVolume("volMuIDUpstream")->SetVisibility(1);
		geo->GetVolume("volMuIDUpstream")->SetTransparency(90);
		//geo->GetVolume("volMuIDUpstream")->SetTransparency(10);
	}
	if ( geo->GetVolume("volMuIDDownstream") != NULL )
	{
		geo->GetVolume("volMuIDDownstream")->SetLineColor(kRed);
		geo->GetVolume("volMuIDDownstream")->SetVisibility(1);
		geo->GetVolume("volMuIDDownstream")->SetTransparency(70);
		//geo->GetVolume("volMuIDDownstream")->SetTransparency(10);
	}
*/
/*
	if ( geo->GetVolume("volECALBarrel") != NULL )
	{
		geo->GetVolume("volECALBarrel")->SetLineColor(kGreen);
		geo->GetVolume("volECALBarrel")->SetVisibility(1);
		geo->GetVolume("volECALBarrel")->SetTransparency(70);
		//geo->GetVolume("muidBar_lv")->SetTransparency(10);
	}
	if ( geo->GetVolume("volECALDownstream") != NULL )
	{
		geo->GetVolume("volECALDownstream")->SetLineColor(kPink);
		geo->GetVolume("volECALDownstream")->SetVisibility(1);
		geo->GetVolume("volECALDownstream")->SetTransparency(60);
		//geo->GetVolume("volECALDownstream")->SetTransparency(10);
	}
*/
/*
	if ( geo->GetVolume("volMagnet") != NULL )
	{
		geo->GetVolume("volMagnet")->SetLineColor(kOrange);
		geo->GetVolume("volMagnet")->SetVisibility(1);
		geo->GetVolume("volMagnet")->SetTransparency(20);
	}
*/
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
