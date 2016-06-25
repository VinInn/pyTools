from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os


ver ='81X'
#ver ='810'
#ver ='80X'
##ver ='807'
#ver ='767'
#ver ="ncl"
#ver ="HiM"
eventsRef = Events("SingleMuon22events_reco_81X.root")
#eventsRef = Events('SingleMuon22events_reco_newcal.root')
#eventsRef = Events('SingleMuon22events_reco_HM.root')

tracksRef = Handle("std::vector<reco::Track>")
label = "generalTracks"
#quality = "highPurity"
#quality = "tight"
#quality = "loose"

def format(x) :
  return '{:.2f}'.format(x)


for i in range(0, eventsRef.size()):
#for i in range(0, 200):
  a= eventsRef.to(i)
  ev = eventsRef.eventAuxiliary().event()
#  print "Event", i 
  a=eventsRef.getByLabel(label, tracksRef)
  trVal = []
  for track in tracksRef.product():
#   if (track.phi()<0) : continue
#   if (track.eta()<0) : continue
    if (track.pt()<50) : continue
#   if (track.quality(track.qualityByName(quality))) :
#    pattern = track.hitPattern()
#    if (pattern.numberOfValidHits() != (pattern.numberOfValidPixelHits()+pattern.numberOfValidStripHits())) :
#      print pattern.numberOfValidHits(),pattern.numberOfValidPixelHits(),pattern.numberOfValidStripHits(), pattern.numberOfValidPixelHits()+pattern.numberOfValidStripHits()
    trVal.append([i, ev, 10*int(100*track.eta())+track.phi(), ver, format(track.eta()), format(track.phi()), format(track.pt()),  track.numberOfValidHits() , track.hitPattern().numberOfValidPixelHits(), 
                  track.numberOfLostHits(), format(track.validFraction()), track.ndof(),format(track.chi2()),track.algo()-4,track.originalAlgo()-4,track.quality(track.qualityByName("highPurity"))])

#  print tracksRef.product().size(), len(trVal)
  for tr in trVal :
     print tr


  
       
          
