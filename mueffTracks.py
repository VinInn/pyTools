from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os


eventsRef = Events("step3.root")

tracksRef = Handle("std::vector<reco::Track>")
label = "generalTracks"
quality = "highPurity"
#quality = "tight"
#quality = "loose"

mcMatchRef = Handle("std::vector<float>")

nmu=0
nmuOnly=0
nmuNotConf=0
for i in range(0, eventsRef.size()):
#for i in range(0, 200):
  a= eventsRef.to(i)
  print "Event", i 
  a=eventsRef.getByLabel(label, tracksRef)
  a=eventsRef.getByLabel("trackMCQuality",mcMatchRef)
  mcMatch = mcMatchRef.product() 
  trVal = []
  k = -1
  for track in tracksRef.product():
   k+=1
#   if (track.phi()<0) : continue
   if (abs(track.eta())>2.3) : continue
   if (track.pt()<4) : continue
#   if (track.quality(track.qualityByName(quality))) :
   trVal.append([10*int(100*track.eta())+track.phi(), "ori", track.eta(), track.phi(), track.pt(),  
                   track.numberOfValidHits(), track.hitPattern().numberOfValidPixelHits(), track.ndof(), track.chi2(), 
#                   track.algo()-4,track.originalAlgo()-4,track.quality(track.qualityByName("highPurity")),track.quality(track.qualityByName("confirmed")),mcMatch[k] ])
                   track.algo()-4,track.algo()-4,track.quality(track.qualityByName("highPurity")),track.quality(track.qualityByName("confirmed")),mcMatch[k] ])

  for tr in trVal :
     if(tr[9]==9 or tr[9]==10) :
       nmu+=1
       if(tr[10]==9 or tr[10]==10) : 
          nmuOnly+=1
       if(not tr[12]) : nmuNotConf+=1       
       if (tr[13]<0.5) : print tr

print nmu,nmuOnly,nmuNotConf
          
