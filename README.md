# lazyPlot
A super simple command line tool for plotting CSV and columnar data sets **quickly**. lazy automagically detects columns of numbers and renders them using the options you provide. There are switches for selecting columns, multiple data sets, and setting plot styles. Simple operations like averaging, scaling and smoothing are possible all directly from the command line. 

#Examples

If you need help installing lazy check out the installation directions at the bottom.

lazy only parses and stores columns of numeric data, it does its best to ignore comments and bigs of garbage strewn in files of mostly clean data.

###Lets get lazy###
```
$> cd daDataRuns
$> ls
run04.dat run1.dat run2.dat run3.dat
$> head run1.dat
#This is some important datastuff
Oops I forgot to start this with the common comment #line, hopefully my plotting tool knows how to handle this

#Some error statistics before we provide data results:
blah blah blah blah

#header and actual data, this is where lazyPlot will start parsing.
Step Temp potEng kinEng totEng Enthalpy Pressure ExtPressure Pxx Pyy Pzz Pxy Pxz Pyz
0       699.92  -4.0957468125   0.0901580694444 -4.00558874306  -3.98324257334  0.819156342252  0.38    0.418   0.294   0.427   0.313   0.34    0.12
1       699.84  -4.09592838889  0.0901477638889 -4.005780625    -3.98576585073  0.802106147219  0.363   0.443   0.262   0.382   0.297   0.327   0.053
2       699.76  -4.09591165625  0.0901374583333 -4.00577419792  -3.9875414527   0.789055952186  0.35    0.471   0.234   0.345   0.271   0.306   -0.006
```

OK great, we have a directory with 4 data sets and each of them looks like the file shown above. Lets plot one, we're interested in plotting the totEng on the x-axis and Pressure on the y-axis, those are columns 4 and 6 (0 indexed).

```
$> lazy.py 4 6 run1.dat
run1.dat
```
![alt tag](http://i.imgur.com/BfBlJJ8.png)

Great! Notice that lazy pulls the appropriate names for the x-axis and y-axis labels. These can be over-written using the -xlabel and -ylabel switches, you can also set a title. Lets compare all four of these runs...

```
$> lazy.py 4 6 run*.dat
run04.dat
run1.dat
run2.dat
run3.dat
```
![alt tag](http://i.imgur.com/VJKwU13.png)

COOL! But I want my files plotted in order... 
```
$> lazy.py 4 6 run*.dat -sort
run04.dat
run1.dat
run2.dat
run3.dat
```
![alt tag](http://i.imgur.com/V2IcBpO.png)

WOWSERS! But I want that data to be transparent...
```
$> lazy.py 4 6 run*.dat -sort -alpha 0.7
run04.dat
run1.dat
run2.dat
run3.dat
```
![alt tag](http://i.imgur.com/CPEBm6p.png)

IMPRESSIVE! But I want to spread things out a bit...
```
$> lazy.py 4 6 run*.dat -sort -stagger
run04.dat
run1.dat
run2.dat
run3.dat
```
![alt tag](http://i.imgur.com/eCKwtz3.png)

SPECTACULAR! But I want to switch the axes and apply a windowed average to the x-axis with window of size 103 points.
```
$> lazy.py 6 4s103 run*.dat -sort
run04.dat
run1.dat
run2.dat
run3.dat
```
![alt tag](http://i.imgur.com/GdQxARp.png)

SMOOOOOOOOOOOOOTHER! And on both axes.
```
$> lazy.py 6s500 4s500 run*.dat -sort
run04.dat
run1.dat
run2.dat
run3.dat
```
![alt tag](http://i.imgur.com/PUh7H2A.png)

YESSSSSSSSSSS! Now make it a scatter plot with only 1/100 points plotted!
```
$> lazy.py 6s500 4s500 run*.dat -scatter 100
run04.dat
run1.dat
run2.dat
run3.dat
```
![alt tag](http://i.imgur.com/4qFPbQf.png)

Now lets go insane and plot columns 8 & 6 for some files and columnes 7 & 6 for other files. Scale column 6 by 0.5
and label the y-axis to "lazyuser".
```
$> lazy.py 8 6 run04.dat run1.dat 7 6x0.5 run2.dat run3.dat -ylabel lazyuser
run04.dat
run1.dat
run2.dat
run3.dat
```
![alt tag](http://i.imgur.com/6B8ZSzB.png)

```
$> lazy.py -1 0 singlecolumn.dat
singlecolumn.dat
```
![alt tag](http://i.imgur.com/V5ETGHy.png)

##Other supported options:
- -avg : does a point for point averaging accross files with selected columns
- -saveFig : saves a "lazy.png" figure to the local directory instead of plotting
- -noLeg: turn off the legend
- -logx, -logy: log scale for the desired axis
- -altSmooth: turns on an alternative smoothing algorithm that uses a gaussian mixture, scaling parameter should be ~0.5.

**Run lazy with -h or with no arguments and it will give you a list of options.**

##Use lazy on a remote server without X11 forwarding.
Sometimes you need to generate a plot from your cell phone during a meeting (wait what), or maybe you're using a remote server that does not allow X11 forwarding with (AIX I'm looking at you). lazy will automatically detect when X11 is not available and it will write your figure to a directory of your choosing. Set the variable:
REMOTESESSION_BASEDIR at the top of the plotRemote.py script to choose a new base directory. Works great in conjunction with Dropbox or some other directory sharing service.


#Installation

You'll need: python (2.7+) numpy, matplotlib and scipy. Clone this repo:
```
git clone git@github.com:acadien/lazyPlot.git
```

Edit your .bashrc and add the lines:
```
export PYTHONPATH=$PYTHONPATH:"/directory/to/lazyPlot/"
export PATH=$PATH:"/directory/to/lazyPlot/"
```

And consider adding the alias:
```
alias lazy=lazy.py
```
