from DataFormats.FWLite import Handle, Events

from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F, TProfile
import os

gStyle.SetOptStat(111111)


#eventsRef = Events("step3_40PU25ns_ori.root")
#eventsNew = Events("step3_40PU25ns_ori.root")
#eventsNew = Events("step3_40PU25ns_vinoptmatch.root")

eventsRef = Events('SinglePiPt1_ori.root')
#eventsNew = Events('SinglePi1_vinpotmatch.root')

#eventsRef = Events('SingleGamma10_ori.root')
#eventsNew = Events('SingleGamma10_vinpotmatch.root')

#eventsRef = Events('step2_SingleMuPt100_ori.root')
#eventsNew = Events('step2_SingleMuPt100_vinoptmatch.root')

#eventsRef = Events("TTBAR_relval_ori.root")
#eventsNew = Events("TTBAR_relval_vinpoptmatch.root") 

# eventsNew = Events("jetHT_reco_new2.root")
#eventsNew = Events('jetHT_reco_newTkGeom.root')
#eventsRef = Events("jetHT_reco_710_ori.root")

tracksRef = Handle("std::vector<reco::Track>")
tracksNew = Handle("std::vector<reco::Track>")
label = "generalTracks"

#tracksRef = Handle("std::vector<reco::GsfTrack>")
#tracksNew = Handle("std::vector<reco::GsfTrack>")
#label = "electronGsfTracks"

#quality = "tight"
quality = "highPurity"

c1 = TCanvas( 'c1', 'vi', 200, 10, 1000, 500 )
gStyle.SetOptStat(111111)

pulls = TH1F("strip pulls","strip pulls",20,-5,5)
# lostHit = TH2F("lost hit","lost hit",10,0.,10.,50,0.,0.5)
#lostHit = TProfile("lost hit","lost hit",10,0.,10.,50,0.,0.5,'')
lostHit = TProfile("lost hit","lost hit",50,0.,0.5)


for i in range(0, eventsRef.size()) :
# for i in range(0, 1):
    a= eventsRef.to(i)
    print "Event", i
    a=eventsRef.getByLabel(label, tracksRef)
    for track in tracksRef.product():
        if ( not track.quality(track.qualityByName(quality))) : continue
        dp = abs(track.outerPosition().phi()-track.outerMomentum().phi())
        res = track.residuals()
        hitP = track.hitPattern()
        bin=lostHit.Fill(dp,hitP.numberOfLostHits(),)
        j=0
        for ih in range(0,hitP.numberOfHits()) :
            p = hitP.getHitPattern(ih)
            if hitP.validHitFilter(p) :
                if hitP.stripHitFilter(p) :
                    bin = pulls.Fill(res.residualX(j))
                j+=1


c1 = TCanvas( 'c1', 'vi', 200, 10, 1000, 1000 )
gStyle.SetOptStat(111111)
c1.Divide(2)
c1.cd(1)
#c1.SetLogy()
pulls.Draw()
c1.cd(2)
lostHit.Draw()

c1.Print("pullsttbar.png")
os.system("mv pullsttbar.png ~/www/histos/.")


