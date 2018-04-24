import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

fields = ('Annual Contribution', 'Current Age', 'Retirement Age','Current Portfolio Value','Percent in Stocks (vs. Bonds)','# of Simulations')
ageSpread = [15]
portfolioSpread = [0]
stockAllocation = []
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

class yearlyData:
    def __init__(self,stockReturn,bondReturn,stockPercentage):
        self.stockReturn = stockReturn
        self.bondReturn = bondReturn
        self.stockPercentage = stockPercentage

class Investor:
    def __init__(self,entries):
        self.contribution = (float(entries['Annual Contribution'].get()))
        self.currentAge = currentAge = (int(entries['Current Age'].get()))
        self.retirementAge = (int(entries['Retirement Age'].get()))
        self.startingValue = (float(entries['Current Portfolio Value'].get()))
        self.numberOfSimulations = (int(entries['# of Simulations'].get()))
        self.stockPercentage = float(entries['Percent in Stocks (vs. Bonds)'].get())

class QuartileResults:
    def __init__(self, lower, middle, upper):
        self.lower = lower
        self.middle = middle
        self.upper = upper

def GetFinalBalance(obj):
    return obj.finalBalance

def CalculatePortfolio(entries):
    investorValues = Investor(entries)
    stockAllocation.append(investorValues.stockPercentage)
    portfolioSpread = [investorValues.startingValue]
    balance = float(portfolioSpread[0])
    matrixLength = investorValues.retirementAge - investorValues.currentAge
    matrixHeight = investorValues.numberOfSimulations
    dataMatrix = CreateMatrix(matrixLength,matrixHeight)
    simCount = 0
    while (simCount < investorValues.numberOfSimulations):
        iterationAge = investorValues.currentAge
        iterationBalance = balance
        lengthOffset = investorValues.currentAge
        while (iterationAge < investorValues.retirementAge):
            currentYearInfo = GetYearlyInformation()
            iterationBalance = UpdateBalance(iterationBalance,investorValues.contribution,currentYearInfo)
            iterationAge = iterationAge + 1
            dataMatrix[simCount][iterationAge-lengthOffset-1] = iterationBalance

        resultObject = Results(simCount,dataMatrix[simCount][iterationAge-lengthOffset-1],dataMatrix[simCount][:])
        results_array.append(resultObject)
        simCount = simCount + 1

    quartileData = GetQuartileData(investorValues.numberOfSimulations)
    PlotTrendlines(quartileData.lower,quartileData.middle,quartileData.upper)


def UpdateBalance(iterationBalance, contribution,currentYearInfo):
    iterationBalance = iterationBalance + contribution
    stockBalance = iterationBalance * currentYearInfo.stockPercentage
    bondBalance = iterationBalance * (1 - currentYearInfo.stockPercentage)
    stockBalance = stockBalance + stockBalance * currentYearInfo.stockReturn
    bondBalance = bondBalance + bondBalance * currentYearInfo.bondReturn
    iterationBalance = stockBalance + bondBalance
    return iterationBalance

def GetQuartileData(numberOfSimulations):
    stdIncrement = round(numberOfSimulations/100)
    lowerQuartile = round(stdIncrement*25)
    middleQuartile = round(stdIncrement*50)
    upperQuartile = round((stdIncrement*75))
    dataObject = QuartileResults(lowerQuartile,middleQuartile,upperQuartile)
    return dataObject

def PlotTrendlines(lowerQuartile,middleQuartile,upperQuartile):
    plt.clf()
    sortedResults = SortResults(results_array)
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
    l,h = length,height
    Matrix = [[0 for x in range(l)] for y in range(h)]
    #print(np.matrix(Matrix))
    return Matrix

def GetYearlyInformation():
    randomYear = random.randint(1,88)
    stockRate = float(stockData[randomYear])
    bondRate = float(bondData[randomYear])
    stockPct =  float(stockAllocation[0])
    yearObject = yearlyData(stockRate,bondRate,stockPct)
    return yearObject

def FindRandomBondRate():
    randomYear = random.randint(1,30)
    return float(bondData[randomYear])

def PlotChart(ageSpread,portfolioSpread):
        plt.plot(ageSpread,portfolioSpread)
        plt.xlabel('Years of Growth')
        plt.ylabel('Portfolio Value')
        plt.title('Investment Growth Calculator')


def CreateForm(root):
    CreateInitialFigure()
    CreatePerformanceText()
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

def CreatePerformanceText():
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
