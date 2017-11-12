from DataFormats.FWLite import Handle, Events
from bisect import bisect_left, bisect_right
import inspect

#file prefixes
xrd = 'root://cms-xrd-global.cern.ch//'
tier0 = 'root://cms-xrd-tzero.cern.ch//' # 'file:/eos/cms/tier0'
tier2 = 'root://eoscms.cern.ch//' #'file:/eos/cms'
myTracking = 'root://eoscms.cern.ch///store/group/phys_tracking/vincenzo/run2017/'

def fullFileName(prefix,files) :
    return map(lambda x : prefix+x,files)

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

    def __init__(self,ev):
        self.events = ev

    def __getitem__(self,i):
        a = self.events.to(i)
        return int(self.events.object().id().luminosityBlock())

    def __len__(self):
        return int(self.events.size())

def eventsInLumiRange(ev,l,h):
   ls = Lumi(ev)
   il = bisect_left(ls,l)
   return (il,bisect_right(ls,h,il))


class Mini :
  def __init__(self):
    self.jets = (Handle('vector<pat::Jet>'),"slimmedJets")
    self.lumi = (Handle("std::vector<LumiScalers>"),"scalersRawToDigi")
    self.vertices = (Handle("vector<reco::Vertex>"),"offlineSlimmedPrimaryVertices") 
    self.cand = (Handle("vector<pat::PackedCandidate>") ,"packedPFCandidates")
    self.ltk =	(Handle("vector<pat::PackedCandidate>") ,"lostTracks" )

  def set(self,ev) :
    for m in inspect.getmembers(self, lambda x : not inspect.ismethod(x)) :
       if (m[0][0]!='_') : a=ev.getByLabel(m[1][1],m[1][0])


