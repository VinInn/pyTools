from DataFormats.FWLite import Handle, Events

from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os

gStyle.SetOptStat(111111)


eventsRef = Events("step3_40PU25ns_ori.root")
#eventsNew = Events("step3_40PU25ns_ori.root")
eventsNew = Events("step3_40PU25ns_vinoptmatch.root")
dir = 'ttbar_40PU25ns'

#eventsRef = Events('step2_SingleMuPt100_ori.root')
#eventsNew = Events('step2_SingleMuPt100_vinoptmatch.root')

#eventsRef = Events('SingleGamma10_ori.root')
#eventsNew = Events('SingleGamma10_vinpotmatch.root')

#eventsRef = Events('SinglePiPt1_ori.root')
#eventsNew = Events('SinglePi1_vinpotmatch.root')
#dir = "pi1"


#eventsRef = Events("TTBAR_relval_ori.root")
#eventsNew = Events("TTBAR_relval_vinpoptmatch.root") 
#dir = 'ttbar'


eventsNew = Events("jetHT_reco_new2.root")
# eventsNew = Events('jetHT_reco_newTkGeom.root')

eventsRef = Events("jetHT_reco_710_ori.root")
# eventsNew = Events('jetHT_vinoptmatch_3.root')
dir = 'run2012C'

tracksRef = Handle("std::vector<reco::Track>")
tracksNew = Handle("std::vector<reco::Track>")
label = "generalTracks"
#quality = "tight"
quality = "highPurity"

#tracksRef = Handle("std::vector<reco::GsfTrack>")
#tracksNew = Handle("std::vector<reco::GsfTrack>")
#label = "electronGsfTracks"
# quality = "loose"


c1 = TCanvas( 'c1', 'vi', 200, 10, 1000, 500 )
gStyle.SetOptStat(111111)
gStyle.SetHistLineWidth(2)

hh = TH1F("pt diff","pt diff",100,-0.001,0.001);
hn = TH1F("hit diff","hit diff",20,-10,10);
hm = TH1F("miss layer all","miss layer all",20,-10,10);
hp = TH1F("miss layer","miss layer",20,-10,10);
dof = TH1F("dof","dof",20,-10,10);
chi2 = TH1F("chi2","chi2",100,-4.,4.);

hne = TH1F("hit diff e","hit diff e",20,-10,10);
hnb = TH1F("hit diff b","hit diff b",20,-10,10);
h2 = TH2F("pt diff vs eta","pt diff vs eta",100,-0.001,0.001,60,-3,3);
ptall  = TH1F("pt all","pt all",100,-10.,10.)
ptmiss = TH1F("pt miss","pt miss",100,-10.,10.)
ptr = TH1F("pt ratio","pt ratio",100,-10.,10.)
d0all  = TH1F("d0 all","d0 all",100,-5.,5.)
d0miss = TH1F("d0 miss","d0 miss",100,-5.,5.)
d0r = TH1F("d0  ratio","d0 ratio",100,-5.,5.)
dpall  = TH1F("dp all","dp all",100,-0.5,0.5)
dpmiss = TH1F("dp miss","dp miss",100,-0.5,0.5)
dpr = TH1F("dp ratio","dp ratio",100,-0.5,0.5)

algoall = TH1F("algo all","algo all",20,0,20)
algomiss = TH1F("algo miss","algo miss",20,0,20)
algor = TH1F("algo  ratio","algo ratio",20,0,20)

# for event in eventsRef:
for i in range(0, eventsRef.size()):
    a= eventsRef.to(i)
    a= eventsNew.to(i)
    print "Event", i
    a=eventsRef.getByLabel(label, tracksRef)
    a=eventsNew.getByLabel(label, tracksNew)
    trRef = []
    j = 0
    for track in tracksRef.product():
        if (track.found()<8) : continue
        if (track.quality(track.qualityByName(quality))) :
            dp = track.outerPosition().phi()-track.outerMomentum().phi()
            trRef.append((j,track.charge()*track.pt(), track.phi()+track.eta(),track.eta(),track.found(), track.hitPattern(), track.ndof(), track.chi2(), track.dxy(),dp, track.algo() ))
        j += 1
    a = trRef.sort(key=lambda tr: tr[2])
    print j
    trNew = []
    j = 0
    for track in tracksNew.product():
        if (track.found()<8) : continue
        if (track.quality(track.qualityByName(quality))) :
            dp = track.outerPosition().phi()-track.outerMomentum().phi()
            trNew.append((j,track.charge()*track.pt(), track.phi()+track.eta(),track.eta(),track.found(), track.hitPattern(), track.ndof(), track.chi2(), track.dxy(),dp, track.algo() ))
        #print "    Track", j, track.charge()*track.pt(), track.phi(), track.eta(), track.dxy(), track.dz()
        j += 1
    a = trNew.sort(key=lambda tr: tr[2])
    print j
    jr=1
    # get closest in eta+phi, compare pt
    if (len(trNew)<1 or len(trRef)<2) : continue
    for jn in range(0, len(trNew)) :
        while (trRef[jr][2] < trNew[jn][2] and jr<(len(trRef)-1)) : jr+=1
        d1 = abs(trNew[jn][2] - trRef[jr][2])
        d2 = abs(trNew[jn][2] - trRef[jr-1][2])
        k = jr
        if (d2<d1) : k = jr-1
        if (abs(trRef[k][3]-trNew[jn][3])>0.1) : continue
        if (abs(trRef[k][1] - trNew[jn][1])>0.001) : print trRef[k][1], trNew[jn][1]
        bin = hh.Fill((trRef[k][1]-trNew[jn][1])/trRef[k][1])
        bin = hn.Fill((trRef[k][4]-trNew[jn][4]))
        bin = hm.Fill(trRef[k][5].stripLayersWithoutMeasurement()-trNew[jn][5].stripLayersWithoutMeasurement())
        if (abs(trRef[k][3])<0.7) : bin = hnb.Fill((trRef[k][4]-trNew[jn][4]))
        if (abs(trRef[k][3])>1.2) : bin = hne.Fill((trRef[k][4]-trNew[jn][4]))
        bin = h2.Fill((trRef[k][1]-trNew[jn][1])/trRef[k][1],trRef[k][3])
        bin = ptall.Fill(trRef[k][1])
        bin = d0all.Fill(trRef[k][8])
        bin = dpall.Fill(trRef[k][9])
        bin = algoall.Fill(trRef[k][10])
        if (trRef[k][4]-trNew[jn][4] > 0 and trRef[k][4]-trNew[jn][4] <3) :
            bin=hp.Fill(trRef[k][5].stripLayersWithoutMeasurement()-trNew[jn][5].stripLayersWithoutMeasurement())
            bin=dof.Fill(trRef[k][6]-trNew[jn][6])
            bin=chi2.Fill(trRef[k][7]/trRef[k][6]-trNew[jn][7]/trNew[jn][6])
            bin = ptmiss.Fill(trRef[k][1])
            bin = d0miss.Fill(trRef[k][8])
            bin = dpmiss.Fill(trRef[k][9])
            bin = algomiss.Fill(trRef[k][10])


#

os.system("rm -r ~/www/histos/"+dir)
os.system("mkdir ~/www/histos/"+dir)
wdir =  " ~/www/histos/"+dir+"/."

c1 = TCanvas( 'c1', 'vi', 200, 10, 1000, 500 )
gStyle.SetOptStat(111111)
c1.Divide(2,2)
c1.SetLogy()
c1.cd(1).SetLogy()
hn.Draw()
c1.cd(2).SetLogy()
hnb.Draw()
c1.cd(3).SetLogy()
hne.Draw()
c1.cd(4).SetLogy()
hm.Draw()

c1.Print("hit_diff.png")
os.system("mv hit_diff.png "+wdir)

c1 = TCanvas( 'c1', 'vi', 200, 10, 1000, 500 )
gStyle.SetOptStat(111111)
c1.Divide(2,2)
c1.SetLogy()
c1.cd(1).SetLogy()
dof.Draw()
c1.cd(2).SetLogy()
chi2.Draw()
c1.SetLogy()
c1.cd(3).SetLogy()
hn.Draw()
c1.cd(4).SetLogy()
hp.Draw()
c1.Print("chi2.png")
os.system("mv chi2.png"+wdir)

c1 = TCanvas( 'c1', 'vi', 200, 10, 1000, 1000 )
gStyle.SetOptStat(111111)
c1.Divide(3,4)
c1.SetLogy()
c1.cd(1).SetLogy()
ptall.Draw()
c1.cd(2).SetLogy()
ptmiss.Draw()
c1.cd(3).SetLogy()
ptmiss.Copy(ptr)
ptr.Divide(ptall)
ptr.Draw()

c1.cd(4).SetLogy()
d0all.Draw()
c1.cd(5).SetLogy()
d0miss.Draw()
c1.cd(6).SetLogy()
d0miss.Copy(d0r)
d0r.Divide(d0all)
d0r.Draw()

c1.cd(7).SetLogy()
dpall.Draw()
c1.cd(8).SetLogy()
dpmiss.Draw()
c1.cd(9).SetLogy()
dpmiss.Copy(dpr)
dpr.Divide(dpall)
dpr.Draw()


c1.cd(10).SetLogy()
algoall.Draw()
c1.cd(11).SetLogy()
algomiss.Draw()
c1.cd(12).SetLogy()
algomiss.Copy(algor)
algor.Divide(algoall)
algor.Draw()


c1.Print("pt_d0_dphi.png")
os.system("mv pt_d0_dphi.png"+wdir)

c1 = TCanvas( 'c1', 'vi', 200, 10, 1000, 1000 )
gStyle.SetOptStat(111111)
c1.Divide(1)
c1.SetLogy()
hh.Draw()
c1.Print("dptOverpt.png")
os.system("mv dptOverpt.png"+wdir)

h2.Draw()
c1.SetLogy()
c1.cd(2)
hh.Draw()
c1.Print("gen_opt_tight.png")
os.system("mv gen_opt_tight.png ~/www/histos/.")




from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F
import os
c1 = TCanvas( 'c1', 'vi', 200, 10, 1000, 700 )
gStyle.SetOptStat(111111)
gStyle.SetHistLineWidth(2)
#c1.Divide(2)
#c1.cd(1)
newF = TFile("mtv_newvin.root")
# newF.ls()
oriF = TFile('mtv_ori.root')
# oriF.ls()
hn = newF.Get("DQMData/Tracking/Track/cutsReco_quickAssociatorByHits/assocSharedHit")
ho = oriF.Get("DQMData/Tracking/Track/cutsReco_quickAssociatorByHits/assocSharedHit")
hn.UseCurrentStyle()
gStyle.SetHistLineColor(2)
hn.Draw()
#c1.cd(2)
gStyle.SetHistLineColor(4)
ho.UseCurrentStyle()
ho.Draw("same")
c1.Print("assocSharedHit.png")
os.system("mv assocSharedHit.png ~/www/histos/.")
