from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os


eventsRef = Events("SingleEleC_Run200091_Event656063159_lumi538_AOD.root")
eventsNew = Events("step2_inAOD_74.root")

tracks = Handle("std::vector<reco::Track>")
label = "generalTracks"
quality = "highPurity"

i=0
a= eventsRef.to(i)
print "Event", i
a=eventsRef.getByLabel(label, tracks)
for track in tracks.product():
   if (track.phi()>0) : continue
   if (track.eta()<0) : continue
   if (track.pt()<2) : continue
   if (track.quality(track.qualityByName(quality))) : 
     print "ori", track.phi(),track.eta(),track.pt(),track.ndof(),track.chi2(), track.algo()

i=1
a= eventsNew.to(i)
print "Event", i
a=eventsNew.getByLabel(label, tracks)
for track in tracks.product():
   if (track.phi()>0) : continue
   if (track.eta()<0) : continue
   if (track.pt()<2) : continue
   if (track.quality(track.qualityByName(quality))) :
     print "new", track.phi(),track.eta(),track.pt(),track.ndof(),track.chi2(), track.algo()






