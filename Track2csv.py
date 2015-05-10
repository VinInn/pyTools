from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os
import csv

fname='step3'


csvfile = open(fname+'.csv','wb')
writer = csv.writer(csvfile)

writer.writerow(['ev','eta','phi','pt','nhits','npixels','3DLayers', 'dof','chi2','mva','algo','orialgo','hp','conf','mcfrac'])

eventsRef = Events(fname+'.root')

tracksRef = Handle("std::vector<reco::Track>")
label = "generalTracks"
quality = "highPurity"
#quality = "tight"
#quality = "loose"


mvaRef = Handle("edm::ValueMap<float>")
mcMatchRef = Handle("std::vector<float>")

for i in range(0, eventsRef.size()):
#for i in range(0, 200):
  a= eventsRef.to(i)
  print "Event", i 
  a=eventsRef.getByLabel(label, tracksRef)
  a=eventsRef.getByLabel(label, 'MVAVals',mvaRef)
  a=eventsRef.getByLabel("trackMCQuality",mcMatchRef)
  mcMatch = mcMatchRef.product()
  mva = mvaRef.product() 
  trVal = []
  k = -1
  for track in tracksRef.product():
   k+=1
#   if (track.phi()<0) : continue
#   if (abs(track.eta())>2.3) : continue
#   if (track.pt()<4) : continue
#   if (track.quality(track.qualityByName(quality))) :
   writer.writerow([i,track.eta(), track.phi(), track.pt(),  
                   track.numberOfValidHits(), track.hitPattern().numberOfValidPixelHits(),  
                   track.hitPattern().pixelLayersWithMeasurement()+track.hitPattern().numberOfValidStripLayersWithMonoAndStereo(), 
                   track.ndof(), track.chi2(), mva.get(k), 
#                   track.algo()-4,track.originalAlgo()-4,track.quality(track.qualityByName("highPurity")),track.quality(track.qualityByName("confirmed")),mcMatch[k] ])
                   track.algo()-4,track.algo()-4,track.quality(track.qualityByName("highPurity")),track.quality(track.qualityByName("confirmed")),mcMatch[k] ])
