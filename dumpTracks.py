from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os


eventsRef = Events("step3.root")

tracksRef = Handle("std::vector<reco::Track>")
label = "generalTracks"
quality = "highPurity"
#quality = "tight"
#quality = "loose"



for i in range(0, eventsRef.size()):
#for i in range(0, 200):
  a= eventsRef.to(i)
  print "Event", i 
  a=eventsRef.getByLabel(label, tracksRef)
  trVal = []
  for track in tracksRef.product():
#   if (track.phi()<0) : continue
#   if (track.eta()<0) : continue
#   if (track.pt()<5) : continue
   if (track.quality(track.qualityByName(quality))) :
      trVal.append([10*int(100*track.eta())+track.phi(), "ori", track.eta(), track.phi(), track.pt(),  track.numberOfValidHits() , track.hitPattern().numberOfValidPixelHits(), track.ndof(),track.chi2(), track.algo()-4,track.originalAlgo()-4,track.quality(track.qualityByName("highPurity"))])

  for tr in trVal :
     if (tr[1]!="del") : print tr
  
       
          
