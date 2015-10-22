from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os


eventsRef = Events("step3.root")

clusRef = Handle("edmNew::DetSetVector<SiStripCluster>")
label =  "siStripClusters" 

clusHIP = [0,0,0,0,0,0,0,0,0]
for i in range(0, eventsRef.size()):
#for i in range(0, 200):
  a= eventsRef.to(i)
#  print "Event", i 
  a=eventsRef.getByLabel(label, clusRef)
  clusters = clusRef.product().data()
  for ids in clusRef.product().ids() :
    for k  in range(0,ids.size):
      clus = clusters[ids.offset+k]
      if (clus.amplitudes().size()>6 and clus.charge()/clus.amplitudes().size()>250) : 
         clusHIP[(ids.id >>25)&0x7]+=1
         print (ids.id >>25)&0x7


print 'nev ',eventsRef.size()
print clusHIP
          
