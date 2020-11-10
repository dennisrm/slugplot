# slugplot
Python visualization tools

# upset.py
For making upset plots for visualization intersection sizes for multiple sets

### Example
![Example Plot](/example_upset_party2020.png)
### Usage
```python
import upset
data1 = ['A','B','C', ...]
data2 = ['B','C','D', ...]
data3 = ['A','D','E', ...]
...
category_dict = {"group1":data1, "group2":data2, "group3":data3, ...}
label = "Title and info"
myPlot = upset.makeUpset(category_dict, label)
myPlot.show()
```
