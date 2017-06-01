void geoDisplay(TString filename, Int_t VisLevel=3)
{
	TGeoManager *geo = new TGeoManager();
	geo->Import(filename);
	geo->DefaultColors();


	geo->CheckOverlaps(1e-5,"d");
 	geo->PrintOverlaps();

	geo->SetVisLevel(VisLevel);

	geo->GetTopVolume()->Draw("ogl");
}
