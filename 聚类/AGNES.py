import numpy as np

class AGNES:
    def __init__(self,data,n_cls):
        self.data = data
        self.n_cls = n_cls
        self.clusters = []
        self.dist = self.cal_dist()
    def cal_dist(self):
        #计算距离矩阵
        p1 = np.expand_dims(self.data,axis=1)
        p2 = np.expand_dims(self.data,axis=0)
        d = np.square(p1-p2)
        d = np.sqrt(np.sum(d,axis=2))
        return d
    def merge(self):
        #合并
        clusters_dist = np.zeros((len(self.clusters),len(self.clusters)))
        for i,cluster1 in enumerate(self.clusters):
            for j,cluster2 in enumerate(self.clusters):
                if i==j:
                    clusters_dist[i][j]=1000000000
                else:
                    clusters_dist[i][j] = np.min(self.dist[np.ix_(cluster1,cluster2)])
        merge_clusters = np.unravel_index(np.argmin(clusters_dist),shape=clusters_dist.shape)
        cluster1=self.clusters[merge_clusters[0]]
        cluster2= self.clusters[merge_clusters[1]]
        self.clusters.remove(cluster1)
        self.clusters.remove(cluster2)
        self.clusters.append(cluster1+cluster2)
    def summary(self):
        for cluster in self.clusters:
            print(cluster)
    def run(self):
        self.clusters = [[i] for i in range(len(self.data))]
        n=len(self.data)
        while n>self.n_cls:
            self.merge()
            n=n-1
        self.summary()

if __name__ == '__main__':
    data  = np.array([[0,2],
                      [0,0],
                      [1.5,0],
                      [5,0],
                      [5,2]])

    clustering = AGNES(data=data,n_cls=2)
    clustering.run()