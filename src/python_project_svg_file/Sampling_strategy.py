import numpy as np
import matplotlib.pyplot as plt

class Filter():
    
    def __init__(self):
        pass
    
    def mask(self,x,y,radius):
        pass

    def show_mask(self):
        i,j = self.mask(0,0,10)
        print(i,j)
        plt.scatter(i,j)
        plt.show()
        return
        

class simple_filter(Filter):
    def mask(self, x, y, radius):
        return np.meshgrid([-1,0,1],[-1,0,1])


class square_filter(Filter):
    def mask(self, x, y, radius,density=0.2):
        i = np.concatenate((np.linspace(-radius+x,0,int(radius*density),endpoint=False,dtype=np.intc),np.linspace(0,radius+x,int(radius*density)+1,dtype=np.intc)))
        j = np.concatenate((np.linspace(-radius+y,0,int(radius*density),endpoint=False,dtype=np.intc),np.linspace(0,radius+y,int(radius*density)+1,dtype=np.intc)))
    
        return np.meshgrid(i,j)
    


class circle_filter(Filter):
    def mask(self, x, y, radius,density=0.5):

        x_ = np.concatenate((np.linspace(-radius+x,0,int(radius*density),endpoint=False,dtype=np.intc),np.linspace(0,radius+x,int(radius*density)+1,dtype=np.intc)))
        y_ = np.concatenate((np.linspace(-radius+y,0,int(radius*density),endpoint=False,dtype=np.intc),np.linspace(0,radius+y,int(radius*density)+1,dtype=np.intc)))

        X, Y = np.meshgrid(x_, y_)

        X_out = X[np.where((X ** 2) + (Y ** 2) < radius ** 2)]
        Y_out = Y[np.where((X ** 2) + (Y ** 2) < radius ** 2)]

        return X_out,Y_out
    
if __name__ == '__main__':
    filter = square_filter()
    filter.show_mask()