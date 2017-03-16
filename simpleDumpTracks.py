from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os


#ver ='81X'
#ver ='810'
#ver ='80X'
##ver ='807'
#ver ='767'
#ver ="ncl"
#ver ="HiM"
#eventsRef = Events("SingleMuon22events_reco_81X.root")
#eventsRef = Events('SingleMuon22events_reco_newcal2.root')
#eventsRef = Events('SingleMuon22events_reco_HM2.root')
#ver ='81X'
#eventsRef = Events('badEvent4fb_reco_81X.root')
#ver ="ncl"
#eventsRef = Events('badEvent4fb_reco_ncl.root')
#ver ="HiM"
#eventsRef = Events('badEvent4fb_reco_HM.root')
eventsRef = Events('/afs/cern.ch/user/l/lanyov/cmsonly/rereco_278509_856_1394197760.root')
#ver = "PROMPT"
ver = "REREC"

tracksRef = Handle("std::vector<reco::Track>")
label = "generalTracks"
#label = "globalMuons" 
quality = "highPurity"
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
    if (track.pt()<1) : continue
#    if (track.qoverpError()*track.p()>2) : continue
#    if (not track.quality(track.qualityByName(quality))) : continue
#    pattern = track.hitPattern()
#    if (pattern.numberOfValidHits() != (pattern.numberOfValidPixelHits()+pattern.numberOfValidStripHits())) :
#      print pattern.numberOfValidHits(),pattern.numberOfValidPixelHits(),pattern.numberOfValidStripHits(), pattern.numberOfValidPixelHits()+pattern.numberOfValidStripHits()
    trVal.append([i, ev, 10*int(100*track.eta())+track.phi(), ver, format(track.eta()), format(track.phi()), format(track.pt()), format(track.qoverpError()*track.p()),   
                  track.numberOfValidHits() , track.hitPattern().numberOfValidPixelHits(), 
                  track.numberOfLostHits(), format(track.validFraction()), track.ndof(),format(track.chi2()),track.algo()-4,track.originalAlgo()-4,track.quality(track.qualityByName("highPurity"))])

#  print tracksRef.product().size(), len(trVal)
  for tr in trVal :
     print tr


  
       
          
