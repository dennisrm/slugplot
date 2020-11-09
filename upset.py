"""
A module for making upset plots. Usage:

myPlot = upset.makeUpset(category_dict,label)
myPlot.show()
"""

import matplotlib.pyplot as plt
from matplotlib import patches

class Upset:
   
    def __init__(self, category_dict):
        
        self.intersections = self.intersection_sizes(category_dict)
        self.cat_counts = {cat:len(elements) for cat,elements in category_dict.items()}
        
        self.groups = sorted(self.intersections.keys(),key=self.intersections.get,reverse=True)
        self.group_order = {group:i for i,group in enumerate(self.groups)}
 
        self.cat_order = {cat:i for i,cat in enumerate(category_dict.keys())}
        
        fig_cat_height = 0.4*len(category_dict)
        fig_bar_height = 3
        fig_bar_width = 0.5*len(self.groups)
        fig_width = 3.5 + fig_bar_width
        fig_height = fig_cat_height + fig_bar_height + 0.65
        
        self.figure = plt.figure(figsize=(fig_width,fig_height))
        self.figure.patch.set_facecolor("white")

        cat_height = fig_cat_height/fig_height
        bar_height = fig_bar_height/fig_height
        catbar_width = 1.5/fig_width
        cat_width = 1.2/fig_width
        bar_width = fig_bar_width / fig_width
        title_width = 2/fig_width
        side_margin = 0.15/fig_width
        left = cat_width+catbar_width+side_margin
        height_margin = 0.3/fig_height
        
        self.titlebox = plt.axes([side_margin,cat_height+2*height_margin,title_width,bar_height],frameon=False)
        self.bar = plt.axes([left, cat_height+2*height_margin, bar_width, bar_height])
        self.dots = plt.axes([left, height_margin, bar_width, cat_height])
        self.catbar = plt.axes([side_margin,height_margin,catbar_width,cat_height])
        self.cats = plt.axes([catbar_width+side_margin, height_margin, cat_width, cat_height],frameon=False)
                
    def intersection_sizes(self,category_dict):
        """Parse elements from categories to determine numbers of overlapping elements"""
        matches = {}
        for category,elements in category_dict.items():
            for element in elements:
                if element in matches:
                    matches[element].append(category)
                else:
                    matches[element] = [category]
        intersections = {}
        for element,group in matches.items():
            group = tuple(sorted(set(group)))
            try:
                intersections[group].append(element)
            except KeyError:
                intersections[group] = [element]
        return {group:len(elements) for group,elements in intersections.items()}

    def title(self,label):
        self.titlebox.text(0,0,label,fontsize=11,
                           horizontalalignment='center',verticalalignment='center')
        self.titlebox.set_xlim(-1,1)
        self.titlebox.set_ylim(-1,1)
        self.titlebox.axis("off")

    def categoryLabels(self):
        
        # Label Text
        for cat,y in self.cat_order.items():
            self.cats.text(0,y,cat,horizontalalignment='center',verticalalignment='center')
            
        # Faint gray boxes for every other category
        for i in range(len(self.cat_order)):
            if i%2 == 0:
                self.cats.add_patch(patches.Rectangle((-.8,i-.5),2,1,color=(.97,.97,.97)))
                
        # Set bounds (Flipped axis so order of categories is descending)
        self.cats.set_ylim(len(self.cat_order)-.5,-.5)
        self.cats.set_xlim(-1,1)
        self.cats.axis("off")

    def intersectionDots(self):
        num_bars = len(self.group_order)

        self.dots.axis("off")
        self.dots.set_ylim(len(self.cat_order)-.5,-.5)
        self.dots.set_xlim(-.5,num_bars-.5)


        xs,ys = [],[]
        for i in range(len(self.cat_order)):
            if i%2 == 0:
                self.dots.add_patch(patches.Rectangle((-1,i-.5),num_bars+1,1,color=(.96,.96,.96)))
            for j in range(num_bars):
                xs.append(j)
                ys.append(i)
        self.dots.plot(xs,ys,linewidth=0,marker="o",markersize=15,color=(.9,.9,.9))

        for i,group in enumerate(self.group_order):
            ys = [self.cat_order[cat] for cat in group]
            xs = [i]*len(group)

            self.dots.plot(xs,ys,linewidth=3,marker="o",markersize=15,color="black")

       
    def intersectionBars(self):
        num_bars = len(self.group_order)
        xs,ys = [],[]
        for i,group in enumerate(self.group_order):
            xs.append(i)
            ys.append(self.intersections[group])

        self.bar.bar(xs,ys,color=(.4,.4,.4))
        self.bar.set_xlim(-.5,num_bars-.5)
        self.bar.set_xticklabels([self.intersections[g] for g in self.group_order])
        self.bar.set_xticks(range(num_bars))
        self.bar.tick_params('x',length=0)
        self.bar.locator_params(axis='y', nbins=4)
        self.bar.set_ylabel("Size of Intersection")
        
        
    def categoryBars(self):
        xs,ys = [],[]
        for tool,count in self.cat_counts.items():
            ys.append(self.cat_order[tool])
            xs.append(count)
        self.catbar.barh(ys,xs,color=(.5,.5,.5))
        self.catbar.set_xlim(max(xs)*1.1,0)
        self.catbar.set_ylim(len(self.cat_order)-.5,-.5)
        self.catbar.set_yticks([])
        self.catbar.set_title("Size of Group",fontsize=10)

        
    def colorBars(self,category,color):
        xs,ys = [],[]
        if type(category) == str:
            categories = {category}
        else:
            categories = set(category)
        for i,group in enumerate(self.group_order):
            if categories.issubset(group):
                xs.append(i)
                ys.append(self.intersections[group])

        self.bar.bar(xs,ys,color=color,edgecolor=(.4,.4,.4))
        
        
    def colorDots(self,category,color):
        for i,group in enumerate(self.group_order):
            if category in group:
                self.dots.plot(i,self.cat_order[category],marker="o",markersize=13,color = color)
        


    
    def show(self):
        self.figure.show()

        
def makeUpset(category_dict,label):
    upset = Upset(category_dict)
    upset.title(label)
    upset.categoryLabels()
    upset.categoryBars()
    upset.intersectionDots()
    upset.intersectionBars()
    return upset

