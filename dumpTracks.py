from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os


eventsRef = Events("step3.root")

tracksRef = Handle("std::vector<reco::Track>")
label = "generalTracks"
quality = "highPurity"
#quality = "tight"
#quality = "loose"


n4=0
n4c=0
n4n=0
n4cn=0
n4h=0
n4ch=0

nhp=0
nhpc=0

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
#   if (track.quality(track.qualityByName(quality))) :
#    pattern = track.hitPattern()
#    if (pattern.numberOfValidHits() != (pattern.numberOfValidPixelHits()+pattern.numberOfValidStripHits())) :
#      print pattern.numberOfValidHits(),pattern.numberOfValidPixelHits(),pattern.numberOfValidStripHits(), pattern.numberOfValidPixelHits()+pattern.numberOfValidStripHits()
    trVal.append([10*int(100*track.eta())+track.phi(), "ori", track.eta(), track.phi(), track.pt(),  track.numberOfValidHits() , track.hitPattern().numberOfValidPixelHits(), track.ndof(),track.chi2(), 
                    track.algo()-4,track.originalAlgo()-4,track.algoMask().to_string(),    track.algoMask(), track.quality(track.qualityByName("highPurity"))])

  print tracksRef.product().size(), len(trVal)
  for tr in trVal :
     if (tr[12].count()<1) : print tr
     if (tr[13]) :
       nhp+=1
       if (tr[12].count()>1) :
        nhpc+=1
     # if(tr[9]!=tr[10]) : 
     #if(tr[12]>1) :
     if (tr[12].test(4+4)) :
        n4+=1
        if (tr[12].count()>1)	:
       	  n4c+=1
        if (not tr[13]) :
          n4n+=1
          if (tr[12].count()>1) :
            n4cn+=1
        else :
          n4h+=1
          if (tr[12].count()>1) :
            n4ch+=1


print nhp,nhpc
print n4,n4c,n4n,n4cn,n4h,n4ch


  
       
          
