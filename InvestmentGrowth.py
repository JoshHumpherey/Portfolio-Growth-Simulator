import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import numpy as np

fields = ('Annual Contribution', 'Current Age', 'Retirement Age','Current Portfolio Value','# of Simulations')
ageSpread = [15]
portfolioSpread = [0]
results_array = []
strategies = {'Fixed Allocations', 'Shifting Bond Allocations'}

with open('stockHistory.txt') as stockFile:
    stockData = stockFile.readlines()

with open('bondHistory.txt') as bondFile:
    bondData = bondFile.readlines()

class Results:
    def __init__(self,simulationNumber,finalBalance,growthHistory):
        self.simulationNumber = simulationNumber
        self.finalBalance = finalBalance
        self.growthHistory = growthHistory

def GetFinalBalance(obj):
    return obj.finalBalance

def CalculatePortfolio(entries):
    contribution = (float(entries['Annual Contribution'].get()))
    currentAge = (int(entries['Current Age'].get()))
    retirementAge = (int(entries['Retirement Age'].get()))
    startingValue = (float(entries['Current Portfolio Value'].get()))
    numberOfSimulations = (int(entries['# of Simulations'].get()))
    portfolioSpread = [startingValue]
    ageSpread = [currentAge]
    balance = float(portfolioSpread[0])
    matrixLength = retirementAge - currentAge
    matrixHeight = numberOfSimulations
    dataMatrix = CreateMatrix(matrixLength,matrixHeight)
    simCount = 0
    while (simCount < numberOfSimulations):
        iterationAge = currentAge
        iterationBalance = balance
        lengthOffset = currentAge
        while (iterationAge < retirementAge):
            randomReturnRate = FindRandomStockRate()
            iterationBalance = iterationBalance + contribution
            iterationBalance = iterationBalance + iterationBalance*randomReturnRate
            iterationAge = iterationAge + 1
            dataMatrix[simCount][iterationAge-lengthOffset-1] = iterationBalance

        resultObject = Results(simCount,dataMatrix[simCount][iterationAge-lengthOffset-1],dataMatrix[simCount][:])
        results_array.append(resultObject)
        simCount = simCount + 1
    ComputeTrendlines(numberOfSimulations)



def ComputeTrendlines(numberOfSimulations):
    plt.clf()
    sortedResults = SortResults(results_array)
    middleQuartile = round(numberOfSimulations/2)
    lowerQuartile = round(numberOfSimulations/4)
    upperQuartile = round((numberOfSimulations/4)*3)
    plt.xlabel('Years of Growth')
    plt.ylabel('Portfolio Value')
    plt.title('Investment Growth Calculator')
    plt.plot(sortedResults[lowerQuartile].growthHistory)
    plt.plot(sortedResults[middleQuartile].growthHistory)
    plt.plot(sortedResults[upperQuartile].growthHistory)
    lowerResult = round(sortedResults[lowerQuartile].finalBalance)
    middleResult = round(sortedResults[middleQuartile].finalBalance)
    upperResult = round(sortedResults[upperQuartile].finalBalance)
    lowerString = str(format(lowerResult,",d"))
    middleString = str(format(middleResult,",d"))
    upperString = str(format(upperResult,",d"))
    resultsString = "  Bottom Quartile: " + lowerString + " * Middle Quartile: " + middleString + " * Upper Quartile: " + upperString + "  "
    performanceVar.set(resultsString)


def SortResults(arrayToSort):
    sortedArray = sorted(arrayToSort, key=GetFinalBalance)
    return sortedArray

def CreateMatrix(length,height):
    w,h = length,height
    Matrix = [[0 for x in range(w)] for y in range(h)]
    #print(np.matrix(Matrix))
    return Matrix

def PrintBalance(portfolioSpread):
        index = len(portfolioSpread)-1
        balanceText = "Balance at Retirement: " + str(int(round(portfolioSpread[index])))
        finalBalance = Label(root, text=balanceText)
        finalBalance.pack(side=BOTTOM)

def FindRandomStockRate():
    randomYear = random.randint(1,88)
    return float(stockData[randomYear])

def FindRandomBondRate():
    randomYear = random.randint(1,30)
    return float(bondData[randomYear])

def PlotChart(ageSpread,portfolioSpread):
    try:
        plt.plot(ageSpread,portfolioSpread)
        plt.xlabel('Years of Growth')
        plt.ylabel('Portfolio Value')
        plt.title('Investment Growth Calculator')
        fig.canvas.draw()
    except:
        print("")


def CreateForm(root):
    CreateInitialFigure()
    CreatePerformanceText(root)
    ents = makeform(root, fields)
    CreateButtons(ents)
    CreateAllocationPopup()

def CreateInitialFigure():
    fig = plt.figure(1)
    plt.ion()
    plt.plot(ageSpread,portfolioSpread)
    plt.xlabel('Years of Growth')
    plt.ylabel('Portfolio Value')
    plt.title('Investment Growth Calculator')
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack()

def makeform(root, fields):
   entries = {}
   for field in fields:
      row = tk.Frame(root)
      lab = tk.Label(row, width=22, text=field+": ", anchor='w')
      ent = tk.Entry(row)
      ent.insert(0,"0")
      row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
      lab.pack(side=tk.LEFT)
      ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
      entries[field] = ent
   return entries

def CreateAllocationPopup():
    tkvar = tk.StringVar(root)
    tkvar.set('Shifting Bond Allocation')
    popupMenu = tk.OptionMenu(root, tkvar, *strategies)
    tk.Label(root, text='Portfolio Strategy')
    popupMenu.pack(side=tk.BOTTOM, padx=5,pady=5)

def CreateButtons(ents):
    b2 = tk.Button(root, text='Quit', command=root.quit)
    b2.pack(side=tk.BOTTOM, padx=5, pady=5)
    b1 = tk.Button(root, text='Calculate',command=(lambda e=ents: CalculatePortfolio(e)))
    b1.pack(side=tk.BOTTOM, padx=5, pady=5)

def CreatePerformanceText(root):
    global performanceVar
    performanceVar = tk.StringVar()
    performanceVar.set("")
    performanceLabel = tk.Label(textvariable=performanceVar, font=(None,15))
    performanceLabel.pack(side=tk.TOP)

if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title("Portfolio Growth Estimator")
    CreateForm(root)
    root.mainloop()
