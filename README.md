# slugplot
Python visualization tools

# upset.py
For making upset plots for visualization intersection sizes for multiple sets
### Usage
import upset
category_dict = {"group1":data1, "group2":data2, "group3":data3, ...}
myPlot = upset.makeUpset(category_dict, label)
myPlot.show()
