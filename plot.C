#include "CMS_lumi.C"


void xAxisname(string histname, string& xname, string& xunit, string& reg);

void setTCanvasNicev1(TCanvas *can0){
  can0->SetFillColor(0);
  can0->SetBorderMode(0);
  can0->SetBorderSize(2);
  can0->SetTickx(1);
  can0->SetTicky(1);
  /*can0->SetLeftMargin(0.15);
  can0->SetRightMargin(0.05);
  can0->SetTopMargin(0.05);
  can0->SetBottomMargin(0.13);
  */
  can0->SetFrameFillStyle(0);
  can0->SetFrameBorderMode(0);
  can0->SetFrameFillStyle(0);
  can0->SetFrameBorderMode(0);
  return;
}


void plot(){

  bool plotLog = false;
  //bool plotLog = true;

  bool scaleTo1 = true;
  //bool scaleTo1 = false;

  bool scaleTodata = true;

  if(scaleTodata)
    scaleTo1 = false;


  TFile *f;

  string fdname = "histoData_runBCD.root";
  
  TFile *fdata = TFile::Open(fdname.c_str());
  f   = TFile::Open("histoMC_runBCD.root");


  TIter next(fdata->GetListOfKeys());

  TKey *key;


  while ((key = (TKey*)next())) {

    
    TClass *cl = gROOT->GetClass(key->GetClassName());
    if (cl->InheritsFrom("TDirectory")) {
      continue;
    }
  
    
    if (!cl->InheritsFrom("TH1F")) continue;
    

   
    TH1 *hdata = (TH1*)key->ReadObj();
    hdata->SetMarkerColor(1);
    hdata->SetLineColor(1);
    hdata->SetMarkerStyle(20);
    hdata->SetMarkerSize(1.5);
    

    string var = hdata->GetName();
    cout<<"Var name is "<<var<<endl;


    int nbins = hdata->GetNbinsX();
    double xlow = hdata->GetXaxis()->GetXmin();
    double xhigh = hdata->GetXaxis()->GetXmax();
    
    TH1F *hgjtot = new TH1F("hgjtot","",nbins,xlow,xhigh);

    int histLineColor = kOrange-2;
    int histFillColor = kOrange-2;

    TH1F *hmc;
    
    hmc = (TH1F*)f->Get(var.c_str());

    hmc->SetFillColor(histFillColor);
    hmc->SetLineColor(histLineColor);
      
    
    TH1F *hcdata = (TH1F*)hdata->Clone();
    TH1F *hcmc = (TH1F*)hmc->Clone();

    double scale_data = 1;
    double scale_mc = 1;
      
    if(hmc->Integral()!=0)
      scale_mc = hdata->Integral()/hmc->Integral();
    else 
      scale_mc = 0;
      
    hmc->Scale(scale_mc);

    


    int W = 800;
    int H = 600;
    
    int H_ref = 600; 
    int W_ref = 800; 
    
    // references for T, B, L, R
    float T = 0.08*H_ref;
    float B = 0.12*H_ref; 
    float L = 0.12*W_ref;
    float R = 0.04*W_ref;


    
    TCanvas* c = new TCanvas("c","c",50,50,W,H);
    
    c->SetLeftMargin( L/W );
    c->SetRightMargin( R/W );
    c->SetTopMargin( T/H );
    c->SetBottomMargin( B/H );
    
    gStyle->SetOptStat(0);
    
    
    gStyle->SetTitleFont(62);
    gStyle->SetLabelFont(62);
    
    setTCanvasNicev1(c);
    
    TPad *pad1 = new TPad("pad1", "The pad 80% of the height",0.0,0.2,1.0,1.0,21);
    TPad *pad2 = new TPad("pad2", "The pad 20% of the height",0.0,0.001,1.0,0.25,22);
    
    pad1->SetFillColor(0);
    pad2->SetFillColor(0);

    pad2->SetTopMargin(0.02619172);
    pad2->SetBottomMargin(0.3102846);
    
    pad1->Draw();
    pad2->Draw();
    
    pad1->cd();
    if(plotLog) pad1->SetLogy();
    
    char *binw = new char[100];
  
    string fname = var;

    ///get the xaxis name and the y axis unit
    string xname = "";
    string xunit = "";
    string reg = "";
    xAxisname(var,xname, xunit, reg);

    cout<<"REG is "<<reg<<endl;

    //bin widths
    sprintf(binw,"Events / %2.1f %s", float(hdata->GetBinWidth(1)), xunit.c_str());

    if(float(hdata->GetBinWidth(1)) < 10e-2)
    sprintf(binw,"Events / %2.2f %s", float(hdata->GetBinWidth(1)), xunit.c_str());

    if(float(hdata->GetBinWidth(1)) < 10e-3)
      sprintf(binw,"Events / %2.3f %s", float(hdata->GetBinWidth(1)), xunit.c_str());

    if(float(hdata->GetBinWidth(1)) < 10e-4)
      sprintf(binw,"Events / %2.4f %s", float(hdata->GetBinWidth(1)), xunit.c_str());

    if(float(hdata->GetBinWidth(1)) < 10e-5)
      sprintf(binw,"Events / %2.5f %s", float(hdata->GetBinWidth(1)), xunit.c_str());

    string xtitle = xname;
     
    float max = TMath::Max(hmc->GetMaximum(),hdata->GetMaximum());
    
    double dmax = 1.5;
    double dmin = 0.1;
    
    if(plotLog) dmax = 70.0;
    hdata->SetMaximum(max*dmax);
    hdata->SetMinimum(dmin);
    if(!scaleTodata)
      hdata->SetMinimum(0.00005);
    
    hmc->SetMaximum(max*dmax);
    hmc->SetMinimum(dmin);
    if(!scaleTodata)
      hmc->SetMinimum(0.000005);
    

    hmc->GetXaxis()->SetTitleSize(0.05);  
    hmc->GetYaxis()->SetTitleSize(0.05);  
    
    hmc->GetXaxis()->SetLabelOffset(999);
    hmc->GetXaxis()->SetLabelSize(0);
    hmc->GetYaxis()->SetTitle(binw);
    
    
    
    hmc->GetXaxis()->SetLabelFont(42);
    hmc->GetXaxis()->SetLabelSize(0.035);
    hmc->GetXaxis()->SetTitleSize(0.035);
    hmc->GetXaxis()->SetTitleFont(62);
    hmc->GetYaxis()->SetLabelFont(62);
    hmc->GetYaxis()->SetLabelSize(0.035);
    hmc->GetYaxis()->SetTitleSize(0.035);
    hmc->GetYaxis()->SetTitleFont(62);
    hmc->GetZaxis()->SetLabelFont(62);
    hmc->GetZaxis()->SetLabelSize(0.035);
    hmc->GetZaxis()->SetTitleSize(0.035);
    hmc->GetZaxis()->SetTitleFont(62);
  
    hmc->Draw("LF2BAR");
    hdata->Draw("PE1sames");
    
    TLegend *leg = new TLegend(0.6080402,0.7125436,0.8994975,0.8954704,NULL,"brNDC");
    leg->SetBorderSize(0);
    leg->SetTextFont(62);
    leg->SetLineColor(1);
    leg->SetLineStyle(1);
    leg->SetLineWidth(1);
    leg->SetFillColor(0);
    leg->SetFillStyle(1001);
    
    leg->AddEntry(hdata,"Data","P");
    leg->AddEntry(hmc, "Z#rightarrow ee (MC)","f");
  
    leg->Draw();
    c->Update();
    
    pad1->cd();
    int iPeriod = 2;
    int iPos = 11;
    CMS_lumi( c, iPeriod, iPos );
    pad1->Modified();
    
    pad1->cd();
    
    TLatex *tex = new TLatex(0.4,0.8,reg.c_str());
    tex->SetNDC();
    tex->SetLineWidth(2);
    tex->Draw();
    pad1->Modified();
    
    
    c->Modified();
    c->cd();
    c->SetSelected(c);
    
    /////ratio plots
    pad2->cd();
    
    TH1F *hctot = new TH1F("hctot","",nbins, xlow, xhigh);
    TH1F *htot = new TH1F("htot","",nbins, xlow, xhigh);
    TH1F *hratio = new TH1F("hratio","",nbins, xlow, xhigh); 

    hratio->SetMarkerStyle(20);
    hratio->SetLineColor(1);
    hctot->Add(hcmc);
    htot->Add(hmc);
    //htot->Add(hcqcdtot);
    for( int i=1; i<=nbins; i++){
      
      double ratio = 2;
      double err = 0;
      double mc = htot->GetBinContent(i);
      double data =  hdata->GetBinContent(i);
      
      double cmc = hctot->GetBinContent(i);
      double cdata =  hcdata->GetBinContent(i);
      
      if(htot->GetBinContent(i)==0){
	
	mc = 0.01;
	
	cmc = 0.01;
      }
      
      if( htot->GetBinContent(i)==0 && data == 0)
	{
	  data = 0;
	  cdata = 0;
	}
      
      ratio = (data)/mc;
      cout<<"scale_data : scale_mc : "<<scale_data <<":"<< scale_mc <<endl;
      err = (data/mc)*sqrt( pow(scale_data/sqrt(cdata),2) + pow(scale_mc/sqrt(cmc),2) );
      
      if(data==0){
	
	err = 0;
	ratio = 0;
	
      }
      

      
    
      hratio->SetBinContent(i,ratio);
      hratio->SetBinError(i,err);
      cout<<"data : mc : ratio +/- err : "<<data <<":"<< mc << ":"<< ratio<<"+/-"<<err<<endl;
    }
    
    hratio->GetXaxis()->SetLabelSize(0.11);
    hratio->GetYaxis()->SetLabelSize(0.11);
    hratio->GetYaxis()->SetTitleSize(0.09);
    
    hratio->GetXaxis()->SetLabelFont(42);
    hratio->GetXaxis()->SetLabelSize(0.11);
    hratio->GetXaxis()->SetTitleSize(0.035);
    hratio->GetXaxis()->SetTitleFont(62);
    hratio->GetYaxis()->SetTitle("#frac{Data}{MC}");
    hratio->GetYaxis()->SetLabelFont(62);
    hratio->GetYaxis()->SetLabelSize(0.11);
    hratio->GetYaxis()->SetTitleSize(0.13);
    hratio->GetYaxis()->SetTitleOffset(0.3);
    hratio->GetZaxis()->SetLabelFont(62);
    hratio->GetZaxis()->SetLabelSize(0.035);
    hratio->GetZaxis()->SetTitleSize(0.035);
    hratio->GetZaxis()->SetTitleFont(62);
    
    hratio->GetYaxis()->SetNdivisions(205);
    //hratio->GetYaxis()->SetTickLength(0.01);
    
    hratio->GetXaxis()->SetTitleSize(0.08);  
    hratio->GetXaxis()->SetTitle(xtitle.c_str());
    
    
   hratio->GetXaxis()->SetLabelSize(0.13);
   hratio->GetXaxis()->SetTitleSize(0.13);
   hratio->GetYaxis()->SetLabelSize(0.12);
   hratio->GetYaxis()->SetTitleSize(0.13);
   //hratio->GetYaxis()->SetTickLength(0.01);
   hratio->GetYaxis()->SetTitleFont(62);
   hratio->GetZaxis()->SetLabelFont(62);
   hratio->GetZaxis()->SetLabelSize(0.035);
   hratio->GetZaxis()->SetTitleSize(0.035);
   hratio->GetZaxis()->SetTitleFont(62);

   hratio->GetYaxis()->SetTitleOffset(0.3);
   hratio->GetYaxis()->SetTitle("#frac{Data}{MC}");
   
  //hratio->GetYaxis()->SetTitle("Data/SM");


  //hratio->Draw("PE");
   hratio->SetMaximum(2);
   hratio->SetMinimum(0);
   //hratio->SetMinimum(-3);
   
   hratio->Draw("E1");
   TLine *l = new TLine(xlow,1.,xhigh,1.);
   l->SetLineColor(2);
   l->SetLineStyle(2);
   l->SetLineWidth(2);
   l->Draw("sames");
   
   c->Modified();
   c->Update();
   
   char *filename = new char[100];
   
   char dirName[100] = "plots";
   
   sprintf(filename,"%s/%s.png",dirName,var.c_str());
   c->Print(filename);
   
  }//while ((key = (TKey*)next()))
}


void xAxisname(string histname, string& xname, string& xunit, string& reg){

  ////variable naming
  int fstr = histname.find("chIso",0);
  if(fstr!=string::npos)
    {
      xname = "PF Charged Isolation [GeV]";
      xunit = "GeV";
    }

  fstr = histname.find("neIso",0);
  if(fstr!=string::npos)
    {
      xname = "PF Neutral Hadron Isolation [GeV]";
      xunit = "GeV";
    }

  fstr = histname.find("pfIso",0);
  if(fstr!=string::npos)
    {
      xname = "PF Photon Isolation [GeV]";
      xunit = "GeV";
    }



  fstr = histname.find("ecalIso",0);
  if(fstr!=string::npos)
    {
      xname = "ECAL Isolation [GeV]";
      xunit = "GeV";
    }

  fstr = histname.find("hcalIso",0);
  if(fstr!=string::npos)
    {
      xname = "HCAL Isolation [GeV]";
      xunit = "GeV";
    }

  fstr = histname.find("hcalIso1",0);
  if(fstr!=string::npos)
    {
      xname = "HCAL depth1 Isolation [GeV]";
      xunit = "GeV";
    }

  fstr = histname.find("hcalIso2",0);
  if(fstr!=string::npos)
    {
      xname = "HCAL depth2 Isolation [GeV]";
      xunit = "GeV";
    }

  fstr = histname.find("trkIso",0);
  if(fstr!=string::npos)
    {
      xname = "Tracker Isolation [GeV]";
      xunit = "GeV";
    }




  fstr = histname.find("e1x3",0);
  if(fstr!=string::npos)
    {
      xname = "E_{1x3}/E_{5x5}";
      xunit = "";
    }



  fstr = histname.find("e1x3raw",0);
  if(fstr!=string::npos)
    {
      xname = "E_{1x3}";
      xunit = "GeV";
    }

  
  fstr = histname.find("e1x3raw",0);
  if(fstr!=string::npos)
    {
      xname = "E_{1x3}";
      xunit = "GeV";
    }

  fstr = histname.find("e2x2",0);
  if(fstr!=string::npos)
    {
      xname = "E_{2x2}/E_{5x5}";
      xunit = "";
    }


  fstr = histname.find("e2x2raw",0);
  if(fstr!=string::npos)
    {
      xname = "E_{2x2}";
      xunit = "GeV";
    }


  fstr = histname.find("e2x5",0);
  if(fstr!=string::npos)
    {
      xname = "E_{2x5}/E_{5x5}";
      xunit = "";
    }


  fstr = histname.find("e2x5raw",0);
  if(fstr!=string::npos)
    {
      xname = "E_{2x5}";
      xunit = "GeV";
    }


  fstr = histname.find("e5x5raw",0);
  if(fstr!=string::npos)
    {
      xname = "E_{5x5}";
      xunit = "GeV";
    }

  fstr = histname.find("eleVeto",0);
  if(fstr!=string::npos)
    {
      xname = "CSV";
      xunit = "";
    }

  fstr = histname.find("esEn",0);
  if(fstr!=string::npos)
    {
      xname = "E_{ES}";
      xunit = "GeV";
    }

  fstr = histname.find("esEnTorawEn",0);
  if(fstr!=string::npos)
    {
      xname = "E_{ES}/E_{SC}^{Raw}";
      xunit = "";
    }


  fstr = histname.find("esSRR",0);
  if(fstr!=string::npos)
    {
      xname = "#sigma_{E}^{ES}";
      xunit = "GeV";
    }

  fstr = histname.find("eta",0);
  if(fstr!=string::npos)
    {
      xname = "#eta_{#gamma}";
      xunit = "";
    }

  fstr = histname.find("hOe",0);
  if(fstr!=string::npos)
    {
      xname = "H/E";
      xunit = "";
    }

  fstr = histname.find("muu",0);
  if(fstr!=string::npos)
    {
      xname = "M_{#mu#mu} [GeV]";
      xunit = "GeV";
    }

  fstr = histname.find("muug",0);
  if(fstr!=string::npos)
    {
      xname = "M_{#mu#mu#gamma} [GeV]";
      xunit = "GeV";
    }

  fstr = histname.find("muuPlusmuug",0);
  if(fstr!=string::npos)
    {
      xname = "(M_{#mu#mu#gamma} + M_{#mu#mu})[GeV]";
      xunit = "GeV";
    }

  fstr = histname.find("mva",0);
  if(fstr!=string::npos)
    {
      xname = "MVA";
      xunit = "";
    }


  fstr = histname.find("nvtx",0);
  if(fstr!=string::npos)
    {
      xname = "Nvtx";
      xunit = "";
    }

  fstr = histname.find("pt",0);
  if(fstr!=string::npos)
    {
      xname = "P_{T}^{#gamma} [GeV]";
      xunit = "GeV";
    }

  fstr = histname.find("r9",0);
  if(fstr!=string::npos)
    {
      xname = "R_{9}";
      xunit = "";
    }


  fstr = histname.find("scBrem",0);
  if(fstr!=string::npos)
    {
      xname = "SC brem";
      xunit = "";
    }

  fstr = histname.find("scEn",0);
  if(fstr!=string::npos)
    {
      xname = "SC Energy [GeV]";
      xunit = "[GeV]";
    }

  fstr = histname.find("scEta",0);
  if(fstr!=string::npos)
    {
      xname = "#eta^{SC}";
      xunit = "";
    }

  fstr = histname.find("scPhi",0);
  if(fstr!=string::npos)
    {
      xname = "#phi^{SC}";
      xunit = "";
    }


  fstr = histname.find("scEtaw",0);
  if(fstr!=string::npos)
    {
      xname = "#eta^{SC} width";
      xunit = "";
    }

  fstr = histname.find("scPhiw",0);
  if(fstr!=string::npos)
    {
      xname = "#phi^{SC} width";
      xunit = "";
    }

  fstr = histname.find("scRawEn",0);
  if(fstr!=string::npos)
    {
      xname = "E_{SC}^{Raw} [GeV]";
      xunit = "GeV";
    }

  fstr = histname.find("sie",0);
  if(fstr!=string::npos)
    {
      //xname = "#sigma_{i#etai#eta}";
      xname = "#sigma_{#eta#eta}";
      xunit = "";
    }

  fstr = histname.find("sietaiphi",0);
  if(fstr!=string::npos)
    {
      xname = "#sigma_{i#etai#phi}";
      xunit = "";
    }

  fstr = histname.find("siphi",0);
  if(fstr!=string::npos)
    {
      xname = "#sigma_{i#phii#phi}";
      xunit = "";
    }

  fstr = histname.find("EB",0);
  if(fstr!=string::npos)
    {
      reg = "Barrel";
    }

  fstr = histname.find("EE",0);
  if(fstr!=string::npos)
    {
      reg = "Endcap";
    }

  /*
  fstr = histname.find("2012",0);
  if(fstr!=string::npos)
    {
      xname += "[5x5]";
      xunit = "";
    }
  */

  fstr = histname.find("EB",0);
  if(fstr!=string::npos)
    {
      xname += " [EB]";
      xunit = "";
    }


  fstr = histname.find("EE",0);
  if(fstr!=string::npos)
    {
      xname += " [EE]";
      xunit = "";
    }
  

}
