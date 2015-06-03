# lazyPlot
A super simple CLI tool for plotting CSV and columnar data sets *quickly*. lazyPlot automagically detects columns of numbers and renders them. Several options for selecting columns, multiple data sets, and setting plot styles. Simple operations like averaging, scaling and smoothing are possible all directly from the command line. 

#Examples

Lets try out lazy. Suppose you have a set of raw data that is formatted in columns, space seperated but has a couple of lines of text in it and a couple of comments. lazy knows to ignore lines starting with '#' and lines that have too much text in them. If you happen to have text interspersed with your columns lazy knows to ignore the text but keep numeric data. So go into your data directory...

```
$> cd daDataRuns
$> ls
run1.dat run2.dat run3.dat run4.dat
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

OK great, we have a directory with 4 data sets. Lets plot the first one, we're interested in plotting the totEng on the x-axis and Pressure on the y-axis, those are columns 4 and 6 (0 indexed).

```
$> lazy.py 4 6 run1.dat
run1.dat
Wrote file /home/acadien/Dropbox/lazy.png
![alt tag](http://i.imgur.com/7Ku4nGp.png)