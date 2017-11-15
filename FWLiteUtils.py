from DataFormats.FWLite import Handle, Events
from bisect import bisect_left, bisect_right
import inspect
import subprocess

def accumul(lis):
    total = 0
    for x in lis:
        total += x
        yield total


#file prefixes
xrd = 'root://cms-xrd-global.cern.ch//'
tier0 = 'root://cms-xrd-tzero.cern.ch//' # 'file:/eos/cms/tier0'
tier2 = 'root://eoscms.cern.ch//' #'file:/eos/cms'
myTracking = 'root://eoscms.cern.ch///store/group/phys_tracking/vincenzo/run2017/'

def fullFileName(prefix,files) :
    return map(lambda x : prefix+x,files)

def eventsInLumis(f) :
   output = subprocess.check_output(['edmFileUtil', '--eventsInLumis',f])
   lines = output.split('\n')[4:]
   ls = []
   ev = []
   for l in lines :
     if len(l)<4 : continue
     ls.append(int(l.split()[1]))
     ev.append(int(l.split()[2]))
   ev = [0]+list(accumul(ev))
   return (ls,ev)

def runid(event,lumi) :
    id = event.object().id()
    a=event.getByLabel('scalersRawToDigi', lumi)
    return '{:d}:{:d}:{:.2e}'.format(int(id.run()),int(id.luminosityBlock()),\
                                     lumi.product()[0].instantLumi() if not lumi.product().empty() else 0)
def skip2Lumi(events,ls):
    for i in range(0,events.size()):
        a= events.to(i)
        id = events.object().id()
        if (int(id.luminosityBlock())==ls) : return i
    return events.size()


class Lumi:

    def __init__(self,f,ev):
        self.events = ev
        self.ls, self.ix = eventsInLumis(f)

    def __getitem__(self,i):
        a = self.events.to(i)
        return int(self.events.object().id().luminosityBlock())

    def __len__(self):
        return int(self.events.size())

def eventsInLumiRange(f, ev,l,h):
   lm = Lumi(f,ev)
   ils = []
   for i in range(0,len(lm.ls)) :
      if lm.ls[i]>= l and lm.ls[i]<=h : ils.append((lm.ix[i],lm.ix[i+1]))
   return ils


class Mini :
  def __init__(self):
    self.jets = (Handle('vector<pat::Jet>'),"slimmedJets")
    self.lumi = (Handle("std::vector<LumiScalers>"),"scalersRawToDigi")
    self.vertices = (Handle("vector<reco::Vertex>"),"offlineSlimmedPrimaryVertices") 
    self.cand = (Handle("vector<pat::PackedCandidate>") ,"packedPFCandidates")
    self.ltk =	(Handle("vector<pat::PackedCandidate>") ,"lostTracks" )
    self.triggerBits = (Handle("edm::TriggerResults"), ("TriggerResults","","HLT"))

  def set(self,ev) :
    for m in inspect.getmembers(self, lambda x : not inspect.ismethod(x)) :
       if (m[0][0]!='_') : a=ev.getByLabel(m[1][1],m[1][0])


  def ilumi(self) :
    return self.lumi[0].product()[0].instantLumi() if not self.lumi[0].product().empty() else 0

  def zbIndex(self,ev) :
     ti=[]
     names = ev.object().triggerNames(self.triggerBits[0].product())
     t1 = 'HLT_ZeroBias_v'
     t2 = 'HLT_ZeroBias_part'
     for i in xrange(self.triggerBits[0].product().size()):
       x = names.triggerName(i)
       if x[:len(t1)]==t1 or x[:len(t2)]==t2 : ti.append(i)
     return ti
