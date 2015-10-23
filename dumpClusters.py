from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os


eventsRef = Events("run258425_reco.root")
# "run259721_reco.root") 
#"step3.root")


clusRef = Handle("edmNew::DetSetVector<SiStripCluster>")
label =  "siStripClusters" 

vRef = Handle("vector<reco::Vertex>")
vl   = "offlinePrimaryVertices" 

clusHIP = [0,0,0,0,0,0,0,0,0]
nv=0
for i in range(0, eventsRef.size()):
#for i in range(0, 20):
  if (i%100 == 0) : print i
  a= eventsRef.to(i)
#  print "Event", i 
  a=eventsRef.getByLabel(label, clusRef)
  a=eventsRef.getByLabel(vl,vRef)
  nvtx = vRef.product().size()
  if (nvtx<2) : continue;
  nv+=nvtx
  clusters = clusRef.product().data()
  for ids in clusRef.product().ids() :
    for k  in range(0,ids.size):
      clus = clusters[ids.offset+k]
      if (clus.amplitudes().size()>6 and clus.charge()/clus.amplitudes().size()>250) : 
         clusHIP[(ids.id >>25)&0x7]+=1
#         print (ids.id >>25)&0x7


print 'nev, nvtx, nvtx/nev ',eventsRef.size(), nv, float(nv)/float(eventsRef.size())
print clusHIP
          
