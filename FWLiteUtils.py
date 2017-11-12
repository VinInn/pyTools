from DataFormats.FWLite import Handle, Events
from bisect import bisect_left, bisect_right

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

def eventInLumiRange(ev,l,h):
   ls = Lumi(ev)
   il = bisect_left(ls,l)
   return (il,bisect_right(ls,h,il))

