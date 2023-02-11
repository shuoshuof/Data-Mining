import numpy as np
import random
class DBSCAN:
    def __init__(self,data,minpts,epsilon):
        self.data = data
        self.clusters = []
        self.dist = self.cal_dist()
        self.epsilon =  epsilon
        self.minpts = minpts
        self.visited=np.zeros(len(self.data))#0:unvisited 1:visied 2:noise
        self.labels =np.zeros(len(self.data))#0:unclassified
    def cal_dist(self):
        #计算距离矩阵
        p1 = np.expand_dims(self.data,axis=1)
        p2 = np.expand_dims(self.data,axis=0)
        d = np.square(p1-p2)
        d = np.sqrt(np.sum(d,axis=2))
        d = [[10000000 if i==j else d[i][j] for j in range(len(d)) ]for i in range(len(d))]#防止在找相邻点时找到自己
        d = np.array(d)
        return d
    def get_unvisited(self):
        unvisited = np.where(self.visited==0)[0]
        idx = random.sample(unvisited.tolist(),1)[0]
        return idx
    def search(self,idx,cls_name):
        queue = [idx]#候选队列
        cluster=[]

        near_list = np.where(self.dist[idx] < self.epsilon)[0]#距离小于epsilon的附近点

        if len(near_list) < self.minpts:
            self.visited[idx] = 2
            return False
        while len(queue):
            idx = queue.pop(0)

            near_list = np.where(self.dist[idx] < self.epsilon)[0]
            if self.visited[idx] ==2 or len(near_list)<self.minpts:#噪声点或非核心
                self.visited[idx]=1
                self.labels[idx]=cls_name
                cluster.append(idx)
            else:#核心点
                uncls_list = np.where(self.visited != 1)[0]  # 未被分类的点
                near_uncls_list = [idx for idx in near_list if idx in uncls_list]#未被分类的附近点
                self.visited[idx]=1
                queue+=near_uncls_list
                self.labels[idx]=cls_name
                cluster.append(idx)
        self.clusters.append(cluster)
        return True
    def run(self):
        cls_num = 1
        while len(np.where(self.visited==0)[0]):
            idx = self.get_unvisited()

            if self.search(idx,cls_name=cls_num):
                cls_num+=1
        print(self.clusters)
        print(self.labels)
if __name__ == '__main__':

    data = np.array(
        [
            [1,3],
            [1,2],
            [2,4],
            [2,3],
            [2,2],
            [2,1],
            [3,2],
            [4,2],
            [5,3],
            [5,2],
            [5,1],
            [6,2]
        ]
    )
    clustering = DBSCAN(data=data,minpts=3,epsilon=1.1)
    clustering.run()

