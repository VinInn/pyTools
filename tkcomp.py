from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os


eventsOri = Events("step3_ori.root")
eventsNew = Events("step3.root")

tracksOri = Handle("std::vector<reco::Track>")
tracksNew = Handle("std::vector<reco::Track>")
label = "generalTracks"
quality = "highPurity"


for i in range(0, eventsOri.size()):
  a= eventsOri.to(i)
  a= eventsNew.to(i)
#  print "Event", i 
  a=eventsOri.getByLabel(label, tracksOri)
  a=eventsNew.getByLabel(label, tracksNew)
  ntOri = tracksOri.product().size()
  ntNew	= tracksOri.product().size()
  if (ntOri != ntNew ) : print i, ntOri,ntNew


