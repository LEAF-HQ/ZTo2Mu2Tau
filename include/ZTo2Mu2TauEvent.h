#pragma once

#include <TString.h>
#include <TH1F.h>
#include <map>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>

#include "LEAF/Analyzer/include/RecoEvent.h"

using namespace std;

// Container class for all quantities
class ZTo2Mu2TauEvent : public RecoEvent{

public:
  // Constructors, destructor
  ZTo2Mu2TauEvent();
  ~ZTo2Mu2TauEvent();

  void clear();
  void reset();

};
