void generalDisplay(TString filename)
{
  Int_t PriKolor[] = {kRed, kMagenta, kBlue, kCyan, kGreen, kYellow,
                  kPink, kViolet, kAzure, kTeal, kSpring, kOrange };
  Int_t SecKolor[] = { 28, 30, 38, 40, 41, 42, 46};
  Int_t PriIndex = 0;
  Int_t SecIndex = 0;

  TGeoManager *geo2 = new TGeoManager("geo2","test");
	geo2->Import(filename);
  TGeoVolume *volume = NULL;
  TObjArray *volumes = geo2->GetListOfVolumes();
  Int_t nvolumes = volumes->GetEntries();
  for ( int i = 0; i < nvolumes; i++ )
  {
    volume = (TGeoVolume*)volumes->At(i);
    //volume->SetVisibility(kTRUE);
    //volume->VisibleDaughters(kTRUE);
    volume->SetVisContainers(kTRUE);
    Int_t daughters = volume->GetNdaughters();
    switch ( daughters )
    {
      case 0: volume->SetTransparency(100);
              volume->SetLineColor(PriKolor[PriIndex]);
              PriIndex = PriIndex == sizeof(PriKolor) /sizeof(PriKolor[0]) ? 0 : PriIndex + 1;
      case 1: volume->SetTransparency(80);
              volume->SetLineColor(SecKolor[SecIndex]);
              SecIndex = SecIndex == sizeof(SecKolor) /sizeof(SecKolor[0]) ? 0 : SecIndex + 1;
      case 2: volume->SetTransparency(60);
      case 3: volume->SetTransparency(40);
      default: volume->SetTransparency(10);
    }
    if ( TString(volume->GetName()).Contains("DetEnclosure"))
    {
      //cout << volume->GetName() << endl;
      volume->SetVisibility(kFALSE);
    }
  }
	geo2->Export("geom-test.root");
  geo2->GetTopVolume()->Draw("ogl");
}
