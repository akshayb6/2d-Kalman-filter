import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

if __name__ == "__main__":
    
    # Retrive file name for input data
    if(len(sys.argv) < 5):
        print "Four arguments required: python kalman2d.py [datafile] [x1] [x2] [lambda]"
        exit()
    
    filename = sys.argv[1]
    x10 = float(sys.argv[2])
    x20 = float(sys.argv[3])
    scaler = float(sys.argv[4])

    # Read data
    lines = [line.rstrip('\n') for line in open(filename)]
    data = []
    for line in range(0, len(lines)):
        data.append(map(float, lines[line].split(' ')))

    # Print out the data
    print "The input data points in the format of 'k [u1, u2, z1, z2]', are:"
    for it in range(0, len(data)):
        print str(it + 1) + " " + str(data[it])

    I=np.identity(2)
    Q=np.matrix([[10**(-4), 2*10**(-5)],[2*10**(-5), 10**(-4)]])
    R=np.matrix([[10**(-2), 5*10**(-3)],[5*10**(-3), 2*10**(-2)]])
    P0=scaler*I
    
    u1 = []
    u2 = []
    z1 = []
    z2 = []
    u = []
    z = []

    for it in range(len(data)):
        u1.append(data[it][0])
        u2.append(data[it][1])
        z1.append(data[it][2])
        z2.append(data[it][3])
        u.append(np.matrix([[data[it][0]],[data[it][1]]]))
        z.append(np.matrix([[data[it][2]],[data[it][3]]]))

    #Calculating Pd,K,P    
    x0=np.matrix([[x10],[x20]])
    xd=[None]*(len(data)+1)
    Pd=[None]*(len(data)+1)
    P=[None]*len(data)
    x=[None]*len(data)
    K=[None]*len(data)
    Pd[0]=P0+Q
    k=0
    while(k<len(data)):
        K[k]=np.dot(Pd[k],np.linalg.inv(Pd[k]+R))
        P[k]=np.dot(I-K[k],Pd[k])
        k+=1
        if k<len(data):
            Pd[k]=P[k-1]+Q  

    #Calculating x values        
    xd[0]=x0+u[0]
    k=0
    while(k<len(data)):
        x[k]=xd[k]+np.dot(K[k],(z[k]-xd[k]))
        k+=1
        if k<len(data):
            xd[k]=x[k-1]+u[k]
    
    xc=[]
    yc=[]
    for i in range(len(data)):
        xc.append(x[i].item((0,0)))
        yc.append(x[i].item((1,0)))

    print K[2]
    plt.plot(xc,yc,'-o',color='red')
    plt.plot(z1,z2,'-o',color='green')
    red_patch = mpatches.Patch(color='red', label='xk(Calculated)')
    green_patch = mpatches.Patch(color='green', label='zk(Observed)')
    plt.legend(handles=[red_patch, green_patch])
    plt.show()
