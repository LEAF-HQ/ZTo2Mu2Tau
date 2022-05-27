#pragma once

#include <TString.h>
#include <TH1F.h>
#include <map>
#include <TTreeReader.h>
#include <TROOT.h>
#include "LEAF/ZTo2Mu2Tau/include/ZTo2Mu2TauEvent.h"
#include "LEAF/Analyzer/include/BaseHists.h"

using namespace std;

class ZTo2Mu2TauHists : public BaseHists{

public:
  // Constructors, destructor
  ZTo2Mu2TauHists(TString dir_);
  ZTo2Mu2TauHists(const ZTo2Mu2TauHists &) = default;
  ZTo2Mu2TauHists & operator = (const ZTo2Mu2TauHists &) = default;
  ~ZTo2Mu2TauHists() = default;

  // Main functions
  void fill(const ZTo2Mu2TauEvent & event);


protected:

  shared_ptr<TH1D> hmetpt, hmetphi, hsumweights;

};
