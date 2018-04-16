from tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random

fields = ('Annual Contribution', 'Current Age', 'Retirement Age','Current Portfolio Value')
ageSpread = [15]
portfolioSpread = [0]
strategies = {'Fixed Allocations', 'Shifting Bond Allocations'}

with open('stockHistory.txt') as stockFile:
    stockData = stockFile.readlines()

with open('bondHistory.txt') as bondFile:
    bondData = bondFile.readlines()

def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"0")
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
   return entries

def CalculatePortfolio(entries):
    contribution = (float(entries['Annual Contribution'].get()))
    currentAge = (int(entries['Current Age'].get()))
    retirementAge = (int(entries['Retirement Age'].get()))
    startingValue = (float(entries['Current Portfolio Value'].get()))
    portfolioSpread = [startingValue]
    ageSpread = [currentAge]
    balance = float(portfolioSpread[0])

    while (currentAge < retirementAge+1):
        randomReturnRate = FindRandomStockRate()
        balance = balance + contribution
        balance = balance + balance*randomReturnRate
        currentAge = currentAge + 1
        ageSpread.append(currentAge)
        portfolioSpread.append(balance)
        if (currentAge == retirementAge):
            index = len(portfolioSpread)-1
            balanceText = "Balance at Retirement: " + str(int(round(portfolioSpread[index])))
            finalBalance = Label(root, text=balanceText)
            finalBalance.pack(side=BOTTOM)
    PlotChart(ageSpread,portfolioSpread)

def FindRandomStockRate():
    randomYear = random.randint(1,88)
    return float(stockData[randomYear])

def FindRandomBondRate():
    randomYear = random.randint(1,30)
    return float(bondData[randomYear])

def PlotChart(ageSpread,portfolioSpread):
    try:
        plt.bar(ageSpread,portfolioSpread)
        plt.xlabel('Age')
        plt.ylabel('Portfolio Value')
        plt.title('Investment Growth Calculator')
        fig.canvas.draw()
    except:
        print("")

def CreateInitialFigure():
    fig = plt.figure(1)
    plt.ion()
    plt.bar(ageSpread,portfolioSpread)
    plt.xlabel('Age')
    plt.ylabel('Portfolio Value')
    plt.title('Investment Growth Calculator')
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack()

def CreateAllocationPopup():
    tkvar = StringVar(root)
    tkvar.set('Shifting Bond Allocation')
    popupMenu = OptionMenu(root, tkvar, *strategies)
    Label(root, text='Portfolio Strategy')
    popupMenu.pack(side=BOTTOM, padx=5,pady=5)

def CreateForm(root):
    ents = makeform(root, fields)

    b2 = Button(root, text='Quit', command=root.quit)
    b2.pack(side=BOTTOM, padx=5, pady=5)
    b1 = Button(root, text='Calculate',command=(lambda e=ents: CalculatePortfolio(e)))
    b1.pack(side=BOTTOM, padx=5, pady=5)

    CreateAllocationPopup()

if __name__ == '__main__':
    root = Tk()
    root.wm_title("Portfolio Growth Estimator")
    CreateInitialFigure()
    CreateForm(root)
    root.mainloop()
