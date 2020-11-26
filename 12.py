import numpy as np
from matplotlib import pyplot as plt
x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
y = [3.18,7.98,8.98,9.58,9.78,9.98,10.17,10.27,10.47,10.69]
z = [10.69,10.98,11.186,11.326,11.476,11.746,12.156,12.776,14.306,17.426]
plt.figure(figsize=(40,20),dpi=100)
plt.plot(y,x,linestyle='--',label='up conversion/MHZ')
plt.grid(True, linestyle='--', alpha=0.5)
plt.plot(z,x[::-1], linestyle='--',label='low conversion/MHZ')
plt.legend(loc="best")
plt.title('一')
plt.xticks([i for i in(y+z)])
plt.yticks([i for i in (x)])
plt.savefig("./test.png")
plt.show()