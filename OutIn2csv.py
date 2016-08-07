from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os
import csv

def format(x) :
  return '{:.2f}'.format(x)

ver = 'ori'
fname= 'chi2_'+ver
#'inefficientMuons'
# fname= 'run251561New3'

csvfile = open(fname+'.csv','wb')
writer = csv.writer(csvfile)

writer.writerow(['ev','eta','phi','pt','nhits','npixels','pixLayers', 'firstBPix', 'firstFPix', 'Layers','3DLayers', 'missingLayers','dof','chi2','mva','algo','orialgo','algoMask','hp','conf','mcfrac'])

eventsRef = Events('step3_'+ver+'.root')

tracksRef = Handle("std::vector<reco::Track>")
label = "generalTracks"
quality = "highPurity"
#quality = "tight"
#quality = "loose"


mvaRef = Handle("std::vector<float>")
mcMatchRef = Handle("std::vector<float>")

for i in range(0, eventsRef.size()):
#for i in range(0, 200):
  a= eventsRef.to(i)
  id = eventsRef.object().id()
  evid = '{:d}:{:d}:{:d}'.format(int(id.run()),int(id.luminosityBlock()), int(id.event()))
  print "Event", i , evid
  a=eventsRef.getByLabel(label, tracksRef)
#  a=eventsRef.getByLabel(label, 'MVAValues',mvaRef)
  a=eventsRef.getByLabel("trackMCQuality",mcMatchRef)
#  mcMatch = mcMatchRef.product()
#  mva = mvaRef.product() 
  trVal = []
  k = -1
  for track in tracksRef.product():
   k+=1
#   if (track.phi()<0) : continue
#   if (abs(track.eta())>2.3) : continue
#   if (track.pt()<4) : continue
#   if (track.quality(track.qualityByName(quality))) :
#   if (track.algoMask().test(14)):
   writer.writerow([evid,format(track.eta()), format(track.phi()), format(track.pt()),  
                   track.numberOfValidHits(), track.hitPattern().numberOfValidPixelHits(),  track.hitPattern().pixelLayersWithMeasurement(), 
                   track.hitPattern().hasValidHitInPixelLayer(1,1),track.hitPattern().hasValidHitInPixelLayer(2,1),
                   track.hitPattern().trackerLayersWithMeasurement(),
                   track.hitPattern().pixelLayersWithMeasurement()+track.hitPattern().numberOfValidStripLayersWithMonoAndStereo(),
                   track.hitPattern().trackerLayersWithoutMeasurement(0),
                   track.ndof(), format(track.chi2()), 1., # mva[k], 
                   track.algo()-4,track.originalAlgo()-4, track.algoMask().to_ullong()>>4,
                   track.quality(track.qualityByName("highPurity")),track.quality(track.qualityByName("confirmed")),1 ])
#                   track.algo()-4,track.algo()-4,track.quality(track.qualityByName("highPurity")),track.quality(track.qualityByName("confirmed")),mcMatch[k] ])
