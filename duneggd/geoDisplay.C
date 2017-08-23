void geoDisplay()
{
	//gSystem->Load("libGdml");
	gSystem->Load("libGeom");
	TGeoManager *geo = new TGeoManager();
	geo->Import("example0.gdml");
	geo->DefaultColors();


	geo->CheckOverlaps(1e-5,"d");
 	geo->PrintOverlaps();

	//geo->SetMaxVisNodes(70000);
	//geo->SetVisLevel(3);
	geo->SetVisLevel(7);
	//geo->ViewLeaves(true);

       	geo->GetTopVolume()->Draw("ogl");
}
