#include "LEAF/ZTo2Mu2Tau/include/ZTo2Mu2TauHists.h"
#include "LEAF/Analyzer/include/constants.h"
#include "LEAF/Analyzer/include/useful_functions.h"
#include <TH1F.h>
#include <TFile.h>
#include <TGraphAsymmErrors.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TLine.h>
#include <TStyle.h>
#include <TKey.h>
#include <TTree.h>
#include <TLatex.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <iostream>
#include <sys/stat.h>

using namespace std;

ZTo2Mu2TauHists::ZTo2Mu2TauHists(TString dir_) : BaseHists(dir_){

  hmetpt = book<TH1D>("metpt", ";p_{T}^{miss} [GeV]; Events / bin", 150, 0, 3000);
  hmetphi = book<TH1D>("metphi", ";#phi(p_{T}^{miss}); Events / bin", 70, -3.5, 3.5);
  hsumweights = book<TH1D>("sumweights", ";;Sum of event weights", 1, 0.5, 1.5);

}

void ZTo2Mu2TauHists::fill(const ZTo2Mu2TauEvent & event){
  double weight = event.weight;

  hmetpt->Fill(event.met->pt(), weight);
  hmetphi->Fill(event.met->phi(), weight);
  hsumweights->Fill(1, weight);
}
