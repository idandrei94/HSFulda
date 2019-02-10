import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

files = ["Compromise/pc.txt", "General/pc.txt", "Compromise/android.txt", "General/android.txt"]

def parseData(filename):
    file = open(filename)
    data = [x.split(":")[1] for x in file.readlines() if x.split(":")[0] == "Frame Samples"]
    data = [x[:-1].split(" ")[:-1] for x in data]
    data = [item for sublist in data for item in sublist]
    data = [int(x) for x in data]
    mean = np.mean(data)
    std = np.std(data)
    topten = np.mean(sorted(data)[140:150])
    botten = np.mean(sorted(data)[:10])
    max = np.max(data)
    min = np.min(data)
    return {"Data": data, "Mean" : mean, "Std" : std, "Top 10%" : topten, "Bottom 10%" : botten, "Min" : min, "Max" : max}



results = [parseData(x) for x in files]

print("PC Mean %f / %f" % (results[0]["Mean"], results[1]["Mean"]))
print("PC Std %f / %f" % (results[0]["Std"], results[1]["Std"]))
print("PC Top 10 Mean  %f / %f" % (results[0]["Top 10%"], results[1]["Top 10%"]))
print("PC Bottom 10 Mean %f / %f" % (results[0]["Bottom 10%"], results[1]["Bottom 10%"]))
print("PC Min value %d / %d" % (results[0]["Min"], results[1]["Min"]))
print("PC Max value %d / %d" % (results[0]["Max"], results[1]["Max"]))
print("Android Mean %f / %f" % (results[2]["Mean"], results[3]["Mean"]))
print("Android Std %f / %f" % (results[2]["Std"], results[3]["Std"]))
print("Android Top Mean %f / %f" % (results[2]["Top 10%"], results[3]["Top 10%"]))
print("Android Bottom Mean %f / %f" % (results[2]["Bottom 10%"], results[3]["Bottom 10%"]))
print("Android Min value %d / %d" % (results[2]["Min"], results[3]["Min"]))
print("Android Max value %d / %d" % (results[2]["Max"], results[3]["Max"]))

plt.plot(range(150), results[0]["Data"], "#0000ff")
plt.plot(range(150), results[1]["Data"], "#008888")
plt.plot(range(150), results[2]["Data"], "#00ff00")
plt.plot(range(150), results[3]["Data"], "#888800")
plt.legend(["PC unoptimized", "PC optimized", "Android unoptimized", "Android optimized"])
plt.axis([0, 150, 0, 250])
plt.xlabel("Sample index")
plt.ylabel("Framerate")
plt.show()