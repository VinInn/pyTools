from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os


#ver ='81X'
#ver ='810'
ver ='80X'
##ver ='807'
#ver ='767'
eventsRef = Events("reco"+ver+".root")

tracksRef = Handle("std::vector<reco::Track>")
label = "ctfWithMaterialTracksP5"
#quality = "highPurity"
#quality = "tight"
#quality = "loose"



#for i in range(0, eventsRef.size()):
for i in range(0, 200):
  a= eventsRef.to(i)
  ev = eventsRef.eventAuxiliary().event()
#  print "Event", i 
  a=eventsRef.getByLabel(label, tracksRef)
  trVal = []
  for track in tracksRef.product():
#   if (track.phi()<0) : continue
#   if (track.eta()<0) : continue
#   if (track.pt()<5) : continue
#   if (track.quality(track.qualityByName(quality))) :
#    pattern = track.hitPattern()
#    if (pattern.numberOfValidHits() != (pattern.numberOfValidPixelHits()+pattern.numberOfValidStripHits())) :
#      print pattern.numberOfValidHits(),pattern.numberOfValidPixelHits(),pattern.numberOfValidStripHits(), pattern.numberOfValidPixelHits()+pattern.numberOfValidStripHits()
    trVal.append([ev, ver, 10*int(100*track.eta())+track.phi(), track.eta(), track.phi(), track.pt(),  track.numberOfValidHits() , track.hitPattern().numberOfValidPixelHits(), 
                  track.numberOfLostHits(), track.validFraction(), track.ndof(),track.chi2()])

#  print tracksRef.product().size(), len(trVal)
  for tr in trVal :
     print tr


  
       
          
