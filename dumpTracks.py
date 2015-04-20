from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os


eventsRef = Events("arizzi_53XRECO_step3.root")
eventsNew = Events("step3all-samesim.root")

tracksRef = Handle("std::vector<reco::Track>")
tracksNew = Handle("std::vector<reco::Track>")
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
   if (track.pt()<5) : continue
   if (track.quality(track.qualityByName(quality))) :
      trVal.append([10*int(100*track.eta())+track.phi(), "ori", track.eta(), track.phi(), track.pt(),  track.numberOfValidHits() , track.hitPattern().numberOfValidPixelHits(), track.ndof(),track.chi2(), track.algo()-4,track.quality(track.qualityByName("highPurity"))])
  ori = len(trVal)
  a= eventsNew.to(i)
  a=eventsNew.getByLabel(label, tracksNew)
  for track in tracksNew.product():
      #   if (track.phi()<0) : continue
      #   if (track.eta()<0) : continue
      if (track.pt()<5) : continue
      if (track.quality(track.qualityByName(quality))) :
          trVal.append([10*int(100*track.eta())+track.phi(), "new", track.eta(), track.phi(), track.pt(),  track.numberOfValidHits(),  track.hitPattern().numberOfValidPixelHits(),track.ndof(),track.chi2(), track.algo()-4,track.quality(track.qualityByName("highPurity"))])
  a = trVal.sort(key=lambda tr: tr[0])
  print len(trVal)
#  if (len(trVal) != 2*ori) :
#      for tr in trVal :
#          print tr

  for i in range(0, len(trVal)-1):
    if ( abs(trVal[i][0]-trVal[i+1][0])<0.01 and (trVal[i][1] != trVal[i+1][1]) and abs(trVal[i][5]-trVal[i+1][5])<2  ) :
          trVal[i][1] = "del"
          trVal[i+1][1] = "del"
          

  for tr in trVal :
     if (tr[1]!="del") : print tr
  
       
          
