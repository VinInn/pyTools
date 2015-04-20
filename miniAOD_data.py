import ROOT
import itertools
import math
from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F, TProfile
import os
import csv

gStyle.SetOptStat(111111)



pi=3.141579
def deltaPhi(a,b) :
    _c=a-b
    if (_c>pi) :_c-=2*pi
    if (_c<=-pi) : _c+=2*pi
    return _c

def dR2(p1,e1,p2,e2) :
    _dp = deltaPhi(p1,p2)
    _de = e1-e2
    return _dp*_dp + _de*_de




def loop(flist,fname,aod) :

    csvfile = open(fname+'.csv','wb')
    writer = csv.writer(csvfile)

    vertices = [Handle("vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices" ]
    mus = [Handle("vector<pat::Muon>"), "slimmedMuons"]
    pfMETH  = [Handle('std::vector<pat::MET>'),"slimmedMETs"]
    if (aod) :
      vertices = [Handle("vector<reco::Vertex>"), "offlinePrimaryVertices" ]
      mus = [Handle("vector<pat::Muon>"),"cleanPatMuons"] 
      pfMETH  = [Handle('vector<pat::MET>'),"systematicsMET"]


    
    sip2d = TH1F("SIP2D","SIP2D",40,-10.,10.)
    sip3d = TH1F("SIP3D","SIP3D",40,-10.,10.)
    sipxy = TH1F("tk2d","TK SIPXY",40,-10.,10.)
    sipz = TH1F("tk3z","TK SIPZ",40,-10.,10.)

    recoilRawH = ROOT.TH1F("Raw MET","Raw MET",1000,0,1000)
    recoilH = ROOT.TH1F("Recoil","Recoil",100,-10,10)


    responsePt = ROOT.TProfile("responsePt","responsePt",20,0,100)
    resolutionPt = ROOT.TProfile("resolutionPt","resolutionPt",20,0,100)
    responsePU = ROOT.TProfile("responsePU","responsePU",20,0,40)
    resolutionPU = ROOT.TProfile("resolutionPU","resolutionPU",20,0,40)

    hmass = ROOT.TH1F("Z mass","Z mass",100,70,120)


    #
    eventsRef = Events(flist)
    nw=0
    nehpt=0
    nwhpt=0
    nech=0
    nwch=0
    #
    for i in range(0, eventsRef.size()):
        a= eventsRef.to(i)

        eventsRef.getByLabel(pfMETH[1],pfMETH[0])
        met = pfMETH[0].product()[0]
        recoilRawH.Fill(met.pt())

        if((i%5000)==0) : print "Event", i
        a=eventsRef.getByLabel(vertices[1],vertices[0])
        pv = vertices[0].product()[0]
        pvp = vertices[0].product()[0].position()
        nv = vertices[0].product().size()
        a=eventsRef.getByLabel(mus[1],mus[0])
        muons = mus[0].product()
        # print muons.size()
        for mu1,mu2 in itertools.combinations(muons,2):
          if not(mu1.pt()>15 and mu2.pt()>5): continue;
          if mu1.charge()+mu2.charge() !=0: continue;
          if not(mu1.isGlobalMuon() and mu2.isGlobalMuon()) : continue
#          print mu1.pt(),mu2.pt(),mu1.charge()+mu2.charge(), mu1.isGlobalMuon(), mu2.isGlobalMuon(), mu1.track().chi2(),mu1.track().ndof(),mu1.track().hitPattern().pixelLayersWithMeasurement()
          if (mu1.track().hitPattern().pixelLayersWithMeasurement()<1): continue
          if (mu2.track().hitPattern().pixelLayersWithMeasurement()<1):	continue
 
          mass = (mu1.p4()+mu2.p4()).M() 
          if not (mass>70 and mass<120): continue

          hmass.Fill(mass)

          diMu = mu1.p4()+mu2.p4()
          recoil = -(met.p4()+diMu)
        
          Z = diMu.Vect()
          R = recoil.Vect()
          Z.SetZ(0)
          R.SetZ(0)

          URSP = R.Dot(Z.Unit())
          URES = R.Dot(Z.Unit().Cross(ROOT.math.XYZVector(0,0,1)))

          writer.writerow([i,mass,diMu.pt(),URSP,URES,
          mu1.pt(),mu1.eta(),mu1.phi(),mu1.dB(2)/mu1.edB(2),mu1.dB(1)/mu1.edB(1),mu1.track().dxy(pvp)/mu1.track().dxyError(),mu1.track().dz(pvp)/mu1.track().dzError(),
          mu2.pt(),mu2.eta(),mu2.phi(),mu2.dB(2)/mu2.edB(2),mu2.dB(1)/mu2.edB(1),mu2.track().dxy(pvp)/mu2.track().dxyError(),mu2.track().dz(pvp)/mu2.track().dzError()])
          

          responsePt.Fill(diMu.pt(),URSP/diMu.Pt())
          resolutionPt.Fill(diMu.pt(),URES/diMu.Pt())
          if diMu.pt()>20.0:
            responsePU.Fill(nv,URSP/diMu.Pt())
            resolutionPU.Fill(nv,URES/diMu.Pt())
            recoilH.Fill( (URSP+diMu.Pt())/diMu.Pt())

          sip2d.Fill(mu1.dB(2)/mu1.edB(2))
          sip3d.Fill(mu1.dB(1)/mu1.edB(1))
          sipxy.Fill(mu1.track().dxy(pvp)/mu1.track().dxyError())
          sipz.Fill(mu1.track().dz(pvp)/mu1.track().dzError())

          sip2d.Fill(mu2.dB(2)/mu2.edB(2))
          sip3d.Fill(mu2.dB(1)/mu2.edB(1))
          sipxy.Fill(mu2.track().dxy(pvp)/mu2.track().dxyError())
          sipz.Fill(mu2.track().dz(pvp)/mu2.track().dzError())


    csvfile.close()

    c1 = TCanvas( 'c1', fname, 200, 10, 1000, 1400 )
    gStyle.SetOptStat(111111)
    gStyle.SetHistLineWidth(2)
    c1.Divide(2,4)
    c1.cd(1).SetLogy()
    sip2d.DrawNormalized()
    e = TF1("q","0.5*exp(-0.5*x*x)/sqrt(6.28)",-10.,10.)
    e.Draw("same")      
    c1.cd(2).SetLogy()
    sip3d.DrawNormalized()
    e.Draw("same")
    c1.cd(3).SetLogy()
    sipxy.DrawNormalized()
    e.Draw("same")
    c1.cd(4).SetLogy()
    sipz.DrawNormalized()
    e.Draw("same")
    c1.cd(5).SetLogy()
    hmass.DrawNormalized()
    c1.Print("dataHist/sipall"+fname+".png")

    c2 = TCanvas( 'c2', fname, 200, 10, 1000, 1400 )
    gStyle.SetOptStat(111111)
    gStyle.SetHistLineWidth(2)
    c2.Divide(2,3)
    c2.cd(1)
    responsePt.Draw()
    c2.cd(2)
    resolutionPt.Draw()
    c2.cd(3)
    responsePU.Draw()
    c2.cd(4)
    resolutionPU.Draw()
    c2.cd(5).SetLogy()
    recoilH.DrawNormalized()  
    c2.cd(6).SetLogy()
    recoilRawH.DrawNormalized()
    c2.Print("dataHist/ResponseZmumu"+fname+".png")




faods = [
'0015E625-6383-E211-94B1-E0CB4E29C50E.root',  '006EA63A-5982-E211-9ED6-E0CB4EA0A908.root',
'0094BEA5-0082-E211-8E8A-20CF300E9ECB.root',  '0227B56B-B382-E211-B72D-00259073E3A0.root',
'00AE9DB3-DB81-E211-AC38-20CF3027A59B.root',  '0245AC4D-1C82-E211-A6B9-90E6BA0D09BB.root',
'00D6EB46-E181-E211-937B-002590747D92.root',  '02641971-C182-E211-B487-0025905280BE.root',
'0081DAC0-2A84-E211-9C22-0025907750A0.root',  '02144ED7-AD82-E211-B27F-002590747E40.root',
'008FBF8F-F781-E211-AB51-90E6BA19A23C.root',  '021EC053-6082-E211-8683-90E6BA0D09D8.root']

aods = []
for aod in faods : aods.append('aod53x/patTuple_cfg-'+aod)


files = [
         ['DoubleMU2012/08967E6D-6CDC-E411-92DF-0025905B859E.root','DoubleMu2012_74X',False],
#         [aods,'DoubleMu2012_53X',True]
         ]
for f in files : loop(f[0],f[1],f[2])
