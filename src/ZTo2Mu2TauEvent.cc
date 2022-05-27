#include "LEAF/ZTo2Mu2Tau/include/ZTo2Mu2TauEvent.h"
#include "LEAF/Analyzer/include/constants.h"
#include <TH1D.h>
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

ZTo2Mu2TauEvent::ZTo2Mu2TauEvent(){
}

ZTo2Mu2TauEvent::~ZTo2Mu2TauEvent(){
}

void ZTo2Mu2TauEvent::clear(){
  RecoEvent::clear();
}

void ZTo2Mu2TauEvent::reset(){
  RecoEvent::reset();
}
