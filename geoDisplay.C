void geoDisplay(TString filename)
{
	TGeoManager *geo = new TGeoManager();
	geo->Import(filename);
	geo->DefaultColors();


	geo->CheckOverlaps(1e-5,"d");
 	geo->PrintOverlaps();

	geo->SetVisLevel(5);

	geo->GetTopVolume()->Draw("ogl");
}
