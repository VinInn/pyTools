from DataFormats.FWLite import Handle, Events
from ROOT import gROOT, gStyle, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F, TProfile
import os

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




def loop(fname) :
    genPars = Handle("vector<reco::GenParticle>")
    genParsLabel = "prunedGenParticles"
    
    gPar = [Handle("vector<pat::PackedGenParticle>"), "packedGenParticles"]
    vertices = [Handle("vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices" ]

    mus = [Handle("vector<pat::Muon>"), "slimmedMuons"]

    
    sip2d = TH1F("SIP2D","SIP2D",40,-10.,10.)
    sip3d = TH1F("SIP3D","SIP3D",40,-10.,10.)
    sipxy = TH1F("tk2d","TK SIPXY",40,-10.,10.)
    sipz = TH1F("tk3z","TK SIPZ",40,-10.,10.)



    sip3d_l = TH1F("SIP2D l","SIP2D l",40,-10.,10.)
    sip3d_h = TH1F("SIP2D h","SIP2D h",40,-10.,10.)
    sip3d_best = TH1F("SIP2D best","SIP2D best",40,-10.,10.)
    vert = TH1F("zpv","zpv",100,-10.,10.)
    sip_v =  TProfile("SIP2D vs zpv","SIP2D best vs zpv",50,0.,5.,0.,10.)
    #
    eventsRef = Events(fname)
    nw=0
    nehpt=0
    nwhpt=0
    nech=0
    nwch=0
    #
    for i in range(0, eventsRef.size()):
        a= eventsRef.to(i)
        print "Event", i
        a=eventsRef.getByLabel(genParsLabel, genPars)
        zpv=0
        gpvp = genPars.product()[0].vertex()
        for part in genPars.product():
            if (part.vz()!=0) : 
                zpv = part.vz()
                gpvp = part.vertex()
                break
        print "zpv " , zpv
        #
        nmu=0
        nel=0
        nch1=0
        nch2=0
        gmu = []
        for part in genPars.product():
            if (part.status()!=1) : continue
            if (abs(part.pdgId())==13 and part.pt()>5 and abs(part.eta())<2.4) :
                gmu.append((part.phi(),part.eta(), part.charge()*part.pt()))
            if (abs(part.pdgId())==13 and part.pt()>5 and abs(part.eta())<2.4) : nmu+=1
            if (abs(part.pdgId())==11 and part.pt()>7 and abs(part.eta())<2.4) : nel+=1
            if (abs(part.pdgId())==13 and part.pt()>8 and abs(part.eta())<2.4) : nch1+=1
            if (abs(part.pdgId())==11 and part.pt()>10 and abs(part.eta())<2.4) : nch1+=1
            if (abs(part.pdgId())==13 and part.pt()>20 and abs(part.eta())<2.4) : nch2+=1
            if (abs(part.pdgId())==11 and part.pt()>20 and abs(part.eta())<2.4) : nch2+=1
            #    if (abs(part.pdgId())==13): 
            #        print "part", part.phi(),part.eta(), part.pt(), part.vz(), part.vx(), part.vy(), part.mass(), part.pdgId(), part.status()                                   
        #  print "nmu ", nmu,nel
        #  print gmu
        a=eventsRef.getByLabel(vertices[1],vertices[0])
        minz=99999.
        iv=0
        ii=0
        pv = vertices[0].product()[0]
        pvp = vertices[0].product()[0].position()
        nv = vertices[0].product().size()
        for v in vertices[0].product() :
            if (abs(v.z()-zpv) < minz) :
                minz=abs(v.z()-zpv)
                iv = ii
            ii+=1
        print "pv ", iv, minz
        if (iv!=0) : nw+=1
        #   if (nmu+nel>3) :
        if (nmu>1) :
            nehpt+=1
            if (iv!=0) :  nwhpt+=1
        #    if (nch1>0 and nch2>0) :
        if (nch1<1) : continue
        #
        nech+=1
        if (iv!=0) : nwch+=1
        a=eventsRef.getByLabel(mus[1],mus[0])
        pmus = []
        for mu in mus[0].product() :
            if (mu.pt()<5) : continue
            #         if (  mu.isTrackerMuon() or mu.isGlobalMuon()) :
            if ( mu.isGlobalMuon()) :
                pmus.append(( mu.phi(), mu.eta(), mu.pt()*mu.charge(), mu.dB(2)/mu.edB(2), mu.dB(1)/mu.edB(1),
                              mu.track().dxy(gpvp)/mu.track().dxyError(),
                              mu.track().dz(gpvp)/mu.track().dzError(), mu.track().hitPattern().pixelLayersWithMeasurement()  ))
                #        print 'mu', iv, mu.phi(), mu.eta(), mu.pt(), mu.dB(2)/mu.edB(2), mu.dB(1)/mu.edB(1), mu.isTrackerMuon(), mu.isGlobalMuon()
        #     print pmus
        matches = []
        i=0
        for g in gmu :
          j = 0
          for mu in pmus :
              j+=1
              if ( g[2]/mu[2] < 0.5 or g[2]/mu[2] > 2.0 ) : continue
              dr = dR2(g[0],g[1],mu[0],mu[1])
              if ( dr > 0.04 ) : continue
              matches.append((i,j-1, dr, abs(1.-g[2]/mu[2])))
              #print "matched mu", mu
          i+=1
        if (len(matches)<1 ) : continue

        vert.Fill((pv.z()-zpv)/pv.zError())

        k=matches[0][0]
        best = 99999
        dr = 999999
        for m in matches :
            #            if (abs(pv.z()-zpv)<3*pv.zError()) :
            if(pmus[m[1]][7]>2) :
            # if (nv<21) :
                sip3d_l.Fill(pmus[m[1]][3])
            else :  sip3d_h.Fill(pmus[m[1]][3])
            sip2d.Fill(pmus[m[1]][4])
            sip3d.Fill(pmus[m[1]][3])
            sipxy.Fill(pmus[m[1]][5])
            sipz.Fill(pmus[m[1]][6])
            sip_v.Fill(abs(pv.z()-zpv)/pv.zError(),abs(pmus[m[1]][5]))
            if (m[0]!=k) :
                sip3d_best.Fill(best)
                k=m[0]
                best = pmus[m[1]][4]
                dr = m[3]
            else :
                if (m[3]<dr ):
                    dr = m[3]
                    best = pmus[m[1]][4]
        if (dr<9999) : sip3d_best.Fill(best)


    print "wrong pv", nw, nehpt, nwhpt,nech,nwch

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
    sip3d_l.DrawNormalized()
    e.Draw("same")
    c1.cd(6).SetLogy()
    sip3d_h.DrawNormalized()
    e.Draw("same")


    
#    sip3d_best.DrawNormalized()
    c1.cd(7).SetLogy()
    vert.DrawNormalized()
#    ev = TF1("qv","0.2*exp(-0.5*x*x)/sqrt(6.28)",-10.,10.)
#    ev.Draw("same")      
    c1.cd(8)
    sip_v.Draw()

    c1.Print("sipall"+fname+".png")


files = [
#         "SingleMuPt10.root",
#         "Zmumu2.root",
#         "ZmumuPU502.root",
#         "ZmumuPU2.root",
         'ZmumuPUnoDI.root'
#         'Zmumu5314.root',
#         'Zmumu720ph14_50.root',
#         'Zmumu720ph14.root', 
#         "ZZ4l.root"
         ]
for f in files : loop(f)
