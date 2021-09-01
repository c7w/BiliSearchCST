
class Pagination:
    def __init__(self, src, baseUrl, **kwargs):
        self.src = src
        self.count = kwargs.get('count', 10)
        self.baseUrl = baseUrl
        self.length = kwargs.get('length', -1)
        if self.length == -1:
            self.length = len(src)

    def getMaxPage(self):
        return (self.length + (self.count-1)) // self.count

    def getPageSrc(self, val):
        if(val < 1 or val > self.getMaxPage()):
            return []
        else:
            return self.src[self.count * (val-1): self.count*val]

    def getPage(self, val):

        if self.length == 0:
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
        result = {
            "baseUrl": self.baseUrl,
            "max": self.getMaxPage(),
            "list": l,
            "current": val,
            "count": self.length,
        }
        return result
