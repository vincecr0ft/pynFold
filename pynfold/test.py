from fold import fold
from matplotlib import pyplot as plt

f = fold()
print 'data before', f.data
f.data = [100,150]
print 'data after', f.data

print 'response before', f.response
f.response = [[0.08,0.02],[0.02,0.08]]
print 'response after', f.response


f.run()
trace = f.fbu.trace
print trace

plt.hist(trace[1],bins=20, alpha=0.85, normed=True)
plt.ylabel('probability')
plt.show()
