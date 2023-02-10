import numpy as np

class DIANA:
    def __init__(self,data,label,n_cls):
        self.data = data
        self.label = label
        self.n_cls = n_cls
        self.old_party = []
        self.splinter_group = []
        self.clusters = []
        self.dist = self.cal_dist()
    def cal_dist(self):
        #计算距离矩阵
        p1 = np.expand_dims(self.data,axis=1)
        p2 = np.expand_dims(self.data,axis=0)
        d = np.square(p1-p2)
        d = np.sqrt(np.sum(d,axis=2))
        return d
    def Max_Dissimilarity(self):
        #计算相异度
        max_dissimilarity =0
        max_idx = None
        for idx in self.old_party:
            dissimilarity = np.sum(self.dist[idx])
            if dissimilarity >= max_dissimilarity:
                max_dissimilarity = dissimilarity
                max_idx = idx
        self.old_party.remove(max_idx)
        self.splinter_group.append(max_idx)
    def splinter_group_add(self):
        for idx in self.old_party.copy():
            idx_list = self.old_party.copy()
            idx_list.remove(idx)
            if np.min(self.dist[idx][idx_list]) > np.min(self.dist[idx][self.splinter_group]):
                self.old_party.remove(idx)
                self.splinter_group.append(idx)
        self.clusters.append(self.splinter_group)
        self.splinter_group=[]
    def summary(self):
        results = []
        for cluster in self.clusters:
            cls = []
            for idx in cluster:
                print(self.data[idx],end='')
                cls.append(self.data[idx])
            print()
            results.append(cls)
        return results
    def find_cluster(self):
        #找到最大半径的簇
        r = [ np.max(self.dist[cluster]) for cluster in self.clusters]
        max_cluster_idx = np.argmax(r)
        self.old_party = self.clusters[max_cluster_idx]
        self.splinter_group = []
    def run(self):
        self.clusters.append([i for i in range(len(self.data))])
        n=1
        while n<self.n_cls:
            self.find_cluster()
            self.Max_Dissimilarity()
            self.splinter_group_add()
            n+=1
        return self.summary()
if __name__ == '__main__':
    data  = np.array([[10,5],
                      [20,20],
                      [30,30],
                      [30,15],
                      [5,10]])
    clustering = DIANA(
        data=data,
        label=[],
        n_cls=3,
    )
    results = clustering.run()
    print(results)

