
class Pagination:
    def __init__(self, src, baseUrl, count=10):
        self.src = src
        self.count = count
        self.baseUrl = baseUrl

    def getMaxPage(self):
        return (len(self.src) + (self.count-1)) // self.count

    def getPageSrc(self, val):
        if(val < 1 or val > self.getMaxPage()):
            return []
        else:
            return self.src[self.count * (val-1): self.count*val]

    def getPage(self, val):
        
        if len(self.src) == 0:
            return {}
        
        def addToSet(s, val):
            for i in val:
                if 0 < i and i <= self.getMaxPage():
                    s.add(i)
        
        s = set()
        addToSet(s, [1, 2, self.getMaxPage(), self.getMaxPage()-1])
        addToSet(s, [i for i in range(val-2, val+3)])
        rl = list(s)
        rl.sort()
        l = []
        l.append('L')
        for index, element in enumerate(rl):
            if index > 0:
                if rl[index] - rl[index-1] > 1:
                    l.append(-1)
            l.append(element)
        l.append('R')
        return {
            "baseUrl": self.baseUrl,
            "max": self.getMaxPage(),
            "list": l,
        }
