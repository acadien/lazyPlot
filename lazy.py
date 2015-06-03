#!/usr/bin/env python

#local
import plotRemote as pr
#standard
import re, sys, select
import pylab as pl
import numpy as np
#local
from smoothing import windowAvg,superSmooth
from colors import vizSpec

#attempts to parse a file, keeping only rows that can be converted to floats
#keeps rows with the most common number of columns.
def parse(fname,delim=None):
    fraw = open(fname,"r").readlines()

    data=list() 
    dataIndex=list()
    for i,line in enumerate(fraw):

        #drop lines with only newline characters
        if len(line) < 2: continue
            
        #drop comment lines
        if line[0]=="#": continue
            
        #drop lines that don't contain columns of numbers
        l=line.split(delim)
        f=list()
        count=0
        for elem in l:
            try:
                f.append(float(elem))
            except ValueError:
                count+=1

        if count==len(l):
            continue

        data.append(f)
        dataIndex.append(i)

    #Keep only data with the most common number of columns
    columnLengths=map(len,data)

    colN=[columnLengths.count(i) for i in range(max(columnLengths)+1)]
    colNi=colN.index(max(colN))
    [dataNum,parsedData]=zip(*[[dataIndex[i],d] for i,d in enumerate(data) if columnLengths[i]==colNi])

    parsedData=zip(*parsedData)

    labels=fraw[dataNum[0]-1].split(delim)
    n=len(labels)
    try:
        map(float,labels)
        labels=[" "]*n
    except:
        pass

    return labels,parsedData

def usage():
    print "\nUsage: %s <x-data column><s><window size> <y-data column><s><window size> <filenames>"\
        %sys.argv[0].split("/")[-1]
    print "\nUsage: %s <x-data column><x><scale> <y-data column><x><scale> <filenames>"%sys.argv[0].split("/")[-1]
    print "\nA general use plotter of 2D data. \nAttempts to find data in column format and plot the desired columns."
    print "If x-data column is -1 then range(len(y)) is used"
    print "If the column number is followed by an <s> then a window average is applied to that data."
    print "If the column number is followed by an <x> then scaling by that value is applied"
    print "examples:"
    print "./plot2.py datafile "
    print "./plot2.py 0 1 datafile1 datafile2 datafile3"
    print "./plot2.py 0 1 datafile1 0 2 datafile2 datafile3"
    print "./plot2.py 0 1s25 datafile1     #windowed average of width 25 is applied"
    print "./plot2.py 0x0.5 1x2.0 datafile #scale of 0.5 on x-axis and scale of 2.0 on y-axis"
    print "switches: -stagger, -sort, -avg, -scatter, -noLeg, -altSmooth, -logx, -logy, -saveFig"
    print "switches with parameters: -alpha <alpha>, -title <title> -xlabel <xlabel> -ylabel <ylabel>"
    print ""

if len(sys.argv)==1:
    if select.select([sys.stdin,],[],[],0.0)[0]:
        import fileinput
        sys.argv += fileinput.input().readline().split()

if __name__=="__main__":

    if len(sys.argv)<2:
        usage()
        exit(0)

    columnIndeces=list()
    fileIndeces=list()
    columnFileCounter=list()

    #Pre-parse for switches
    nbins=80
    alpha=1.0 #transparency
    switches={"-stagger":False,"-sort":False,"-avg":False,"-scatter":False, "-noLeg":False, "-saveData":False, "-saveFig":False, "-altSmooth":False, "-h":False,"-alpha":None,"-logx":False,"-logy":False,"-title":False,"-xlabel":False,"-ylabel":False}

    for i in range(len(sys.argv)-1,-1,-1):

        if "-alpha" == sys.argv[i]: #special case alpha
            switches["-alpha"]=True
            sys.argv.pop(i)
            alpha = float(sys.argv.pop(i))

        elif "-xlabel" == sys.argv[i]:
            sys.argv.pop(i)
            switches["-xlabel"]=sys.argv.pop(i)

        elif "-ylabel" == sys.argv[i]:
            sys.argv.pop(i)
            switches["-ylabel"]=sys.argv.pop(i)

        elif "-title" == sys.argv[i]:
            sys.argv.pop(i)
            switches["-title"]=sys.argv.pop(i)

        elif "-scatter" == sys.argv[i]:
            sys.argv.pop(i)
            switches["-scatter"]=sys.argv.pop(i)

        elif sys.argv[i] in switches.keys(): 
            switches[sys.argv[i]]=True
            sys.argv.pop(i)

    if switches["-h"]:
        usage()
        exit(0)

    #Parse for column selection and file selection.
    for i in range(1,len(sys.argv)):
        reresult=re.search('^[-]?\d+[sx]?[-]?[\d]*\.?[\d]*$',sys.argv[i])
        try:
            if reresult.group(0) == sys.argv[i]:
                columnIndeces.append(i)
                #How many files will have these columns selected
                if len(columnIndeces)%2==0:
                    columnFileCounter.append(0)
        except AttributeError: 
            fileIndeces.append(i)
            try:
                columnFileCounter[-1]+=1
            except IndexError: pass
            
    if len(columnIndeces)!=0:
        if len(columnIndeces)%2!=0 or columnIndeces[0]!=1:
            usage()
            print "***Error***: improperly formed column selection"
            exit(0)
    else:
        columnFileCounter=[len(sys.argv[1:])]

    xSmoothEnables=[]
    ySmoothEnables=[]
    xScaleEnables=[]
    yScaleEnables=[]
    xScales=[]
    yScales=[]
    xCols=[]
    yCols=[]
    xWANs=[]
    yWANs=[]
    if len(columnIndeces)==0:
        for i in fileIndeces:
            xCols.append(0)
            yCols.append(1)
            xSmoothEnables.append(False)
            ySmoothEnables.append(False)
            xScaleEnables.append(False)
            yScaleEnables.append(False)
            xWANs.append(0)
            yWANs.append(0)
            xScales.append(1.)
            yScales.append(1.)
    else:
        xcs=[c for i,c in enumerate(columnIndeces) if i%2==0]
        ycs=[c for i,c in enumerate(columnIndeces) if (i+1)%2==0]

        for i in range(len(columnFileCounter)):
            xc=sys.argv[xcs[i]]
            xsc=False
            xsm=False
            xw=0
            xscale=1.
            if "s" in xc:
                xsm=True
                r=xc.split("s")
                xc=int(r[0])
                if r[1]=="":
                    xw=10
                else:
                    xw=int(r[1])
            elif "x" in xc:
                xsc=True
                r=xc.split("x")
                xc=int(r[0])
                if r[1]=="":
                    xscale=1.
                else:
                    xscale=float(r[1])
            else:
                xc=int(xc)

            yc=sys.argv[ycs[i]]
            ysc=False
            ysm=False
            yw=0
            yscale=1.0
            if "s" in yc:
                ysm=True
                r=yc.split("s")
                yc=int(r[0])
                if r[1]=="":
                    yw=10
                else:
                    yw=int(r[1])
            elif "x" in yc:
                ysc=True
                r=yc.split("x")
                yc=int(r[0])
                if r[1]=="":
                    yscale=1.
                else:
                    yscale=float(r[1])
            else:
                yc=int(yc)

            for j in range(columnFileCounter[i]):
                xCols.append(xc)
                xSmoothEnables.append(xsm)
                xWANs.append(xw)
                xScaleEnables.append(xsc)
                xScales.append(xscale)
                yCols.append(yc)
                ySmoothEnables.append(ysm)
                yWANs.append(yw)
                yScaleEnables.append(ysc)
                yScales.append(yscale)

    #Grab the file name
    fileNames=[sys.argv[i] for i in fileIndeces]
    nFileNames = len(fileNames)
    if switches['-sort']:
        #Sorting might introduce undesirable behavior so skip it
        #if you're only selecting 1 column then sort the file names
        if len(columnFileCounter)==1: 
            try:
                fnamenumbers=map(lambda x:float(".".join(re.findall('\d+',x))),fileNames)
                if nFileNames == len(fnamenumbers):
                    fileNames=zip(*sorted(zip(fileNames,fnamenumbers),key=lambda x:x[1]))[0]
            except ValueError:
                pass

    #Initialize Average
    initAvg=True
    count=0.

    #Colors
    colors = None

    #Load up the data and the label guesses
    labels=list()
    fdatas=list()
    for fname in fileNames:
        if fname[-3:]=="csv":
            l,f = parse(fname,",")
        else:
            l,f = parse(fname)

        labels.append(l)
        fdatas.append(f)
        print fname
    label=labels[0]

    fig=pl.figure()
    pl.grid()
    
    for i in range(sum(columnFileCounter)):
        fdata=fdatas[i]
        xCol=xCols[i]
        yCol=yCols[i]

        #Error check on column selection
        if yCol >= len(fdata):
            print "Error: Max column number is %d, but %d requested."%(len(fdata)-1,yCol)
        if xCol >= len(fdata):
            print "Error: Max column number is %d, but %d requested."%(len(fdata)-1,xCol)
        
        #Column selection
        ydata=fdata[yCol]
        if xCol==-1:
            xdata=range(len(ydata))
        else:
            xdata=fdata[xCol]

        #Smoothing:
        xSmoothEnable=xSmoothEnables[i]
        ySmoothEnable=ySmoothEnables[i]
        xWAN=xWANs[i]
        yWAN=yWANs[i]
        xdataSmooth=[]
        ydataSmooth=[]

        if xSmoothEnable:
            if switches["-altSmooth"]:
                xdataSmooth=superSmooth(xdata,ydata,xWAN/100.0)
            else:
                xdataSmooth=windowAvg(xdata,xWAN)
        if ySmoothEnable:
            if switches["-altSmooth"]:
                ydataSmooth=superSmooth(xdata,ydata,yWAN/100.0)
            else:
                ydataSmooth=windowAvg(ydata,yWAN)

        #Correct for window offset, average introduces extra points that need to be chopped off
        if not switches["-altSmooth"] and xSmoothEnable or ySmoothEnable: 
            WAN=max(xWAN,yWAN)
            xdataSmooth=xdataSmooth[WAN/2+1:WAN/-2]
            ydataSmooth=ydataSmooth[WAN/2+1:WAN/-2]
            xdata=xdata[WAN/2+1:WAN/-2]
            ydata=ydata[WAN/2+1:WAN/-2]

        #Scaling - multiply by constant
        xScaleEnable=xScaleEnables[i]
        yScaleEnable=yScaleEnables[i]
        xScale=xScales[i]
        yScale=yScales[i]
        
        if xScaleEnable:
            xdata=[x*xScale for x in xdata]
            xdataSmooth=[x*xScale for x in xdataSmooth]
        if yScaleEnable:
            ydata=[y*yScale for y in ydata]
            ydataSmooth=[y*yScale for y in ydataSmooth]
        if switches["-logx"]:
            xdata=np.log(xdata)
        if switches["-logy"]:
            ydata=np.log(ydata)
        if switches["-stagger"]:
            m=min(ydata)
            if i==0:
                dely=(max(ydata)-min(ydata))/2.
            ydata=[y-m+i*dely for y in ydata]
            ydataSmooth=[y-m+i*dely for y in ydataSmooth]
            pl.tick_params(labelleft='off')

        #Plotting
        #Use column labels if available
        if switches["-avg"] and initAvg:
            initAvg=False
            avgx=xdata
            avgy=np.zeros(len(ydata))

        if i==0 and switches["-avg"]:
            ybins = range(nbins)
            mn=min(ydata)
            mx=max(ydata)

        if i==0 and len(label)==len(fdata):
            if xCol!=-1:
                pl.xlabel( label[xCol] )
            pl.ylabel( label[yCol] )

        if switches["-avg"]:
            if len(avgy)!=len(ydata):
                print "Not all data is the same length, unable to average lists of different lengths."
                exit(0)
            if ySmoothEnable:
                avgy+=np.array(ydataSmooth)
            else:
                avgy+=np.array(ydata)
            count+=1

        elif switches["-scatter"]:
            if xSmoothEnable:
                xdata=xdataSmooth
            if ySmoothEnable:
                ydata=ydataSmooth
            
            nPoints = int(switches["-scatter"])
            pl.scatter(xdata[::nPoints],ydata[::nPoints],lw=0.1,label=fileNames[i],facecolor=vizSpec(float(i)/max((nFileNames-1),1) ))


        else: #Regular plot, multiple lines
            cc=vizSpec(float(i)/max(nFileNames-1,1) )

            if xSmoothEnable:
                xdata=xdataSmooth
            if ySmoothEnable:
                ydata=ydataSmooth
            pl.plot(xdata,ydata,lw=1.5,c=cc,label=fileNames[i],alpha=alpha)            
            
    if switches["-avg"]:
        avgy=[i/count for i in avgy]
        pl.plot(avgx,avgy)
    
    """ #Still figuring this one out...
    if switches["-saveData"]:
        data=label[xCol] + " " + label[yCol] + "\n"
        for x,y in zip(avgx,avgy):
            data+=str(x)+" "+str(y)+"\n"
        open("lazy.data","w").write(data)
    """

    if not switches["-noLeg"]:
        pl.legend(loc=0)

    pl.gca().autoscale_view(True,True,True)

    if switches["-title"]:
        pl.title(switches["-title"])

    if switches["-xlabel"]:
        pl.xlabel(switches["-xlabel"])

    if switches["-ylabel"]:
        pl.ylabel(switches["-ylabel"])

    if switches["-saveFig"]:
        pl.savefig("lazy.png")
        print "Wrote file lazy.png"
    else:
        pr.prshow("lazy.png")
