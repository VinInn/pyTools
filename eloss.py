from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F, TProfile
import os

gStyle.SetOptStat(111111)


rhoH = TProfile("rho",'rho',100,0.,200.)
zH = TProfile("z",'z',100,0.,300.)
xyH = TH2F("xy",'xy',50,-120,120,50,-120,120)
xyeH = TH2F("xye",'xye',50,-120,120,50,-120,120)
etaH = TProfile("eta",'eta',100,-2.5,2.5)
phiH = TProfile("phi",'phi',60,-3.1415,3.1415)


def loop(fname) :
    mus = [Handle("vector<reco::Track> "), "generalTracks"]

    eventsRef = Events(fname)
    for i in range(0, eventsRef.size()):
        a= eventsRef.to(i)
        a=eventsRef.getByLabel(mus[1],mus[0])
        pmus = []
        for mu in mus[0].product() :
            if (mu.pt()<5) : continue
            if (not mu.innerOk()) : continue
            e = 1000*(mu.momentum().r()-mu.outerMomentum().r())
            if (e<0) : continue
            print e
            z = abs(mu.outerPosition().z())
            r = mu.outerPosition().rho()
	    #rhoH.Fill(mu.outerPosition().rho(),e)
            zH.Fill(mu.outerPosition().z(),e)
            etaH.Fill(mu.outerPosition().eta(),e)
            if (z>240) :
                xyeH.Fill(mu.outerPosition().x(),mu.outerPosition().y(),e)
                xyH.Fill(mu.outerPosition().x(),mu.outerPosition().y(),1)
                if (r<120) :phiH.Fill(mu.outerPosition().phi(),e)
                rhoH.Fill(r,e)


    c1 = TCanvas( 'c1', fname, 200, 10, 1000, 1400 )
    gStyle.SetOptStat(111111)
    gStyle.SetHistLineWidth(2)
    c1.Divide(2,3)
    c1.cd(1)
    rhoH.Draw()
    c1.cd(2)
    zH.Draw()
    c1.cd(3)
    xyH.Draw("COLZ")
    c1.cd(4)
    xyeH.Divide(xyH)
    xyeH.Draw("COLZ")
    c1.cd(5)
    etaH.Draw()
    c1.cd(6)
    phiH.Draw()

    c1.Print("eloss"+fname+".png")

files = ["SingleMuPt10_RECO.root"
         ]
for f in files : loop(f)
