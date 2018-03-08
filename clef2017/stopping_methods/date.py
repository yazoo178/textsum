import datetime
import random
import matplotlib.pyplot as plt


start = datetime.datetime.strptime("10-1-2018", "%d-%m-%Y")
end = datetime.datetime.strptime("15-2-2018", "%d-%m-%Y")
x = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
y = [0.1, 0.1, 0.15, 0.2, 0.15, 0.15, 0.157, 0.159, 0.19, 0.21, 0.19, 0.194, 0.196, 0.18, 0.16, 0.15, 0.22, 0.25, 0.33, 0.4, 0.42, 0.41, 0.425, 0.435, 0.465, 0.460, 0.465, 0.47, 0.475, 0.48, 0.475, 0.488, 0.489, 0.492, 0.487, 0.49]

# plot
fig, ax = plt.subplots()
plt.plot(x,y)

for i, txt in enumerate(x):
    if i == 15:
        ax.annotate("← Matched", (x[i],y[i]))

# beautify the x-labels
plt.gcf().autofmt_xdate()
plt.title('Happiness')
plt.xlabel('Date')
plt.ylabel('Happiness Rate')
plt.show()