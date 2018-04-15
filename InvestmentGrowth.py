from matplotlib.ticker import FuncFormatter
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

fields = ('Annual Contribution', 'Growth Rate', 'Current Age', 'Retirement Age','Current Portfolio Value','Retirement Income')
ageSpread = [15]
portfolioSpread = [0]

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
    growthRate = (float(entries['Growth Rate'].get()))
    currentAge = (int(entries['Current Age'].get()))
    retirementAge = (int(entries['Retirement Age'].get()))
    startingValue = (float(entries['Current Portfolio Value'].get()))
    portfolioSpread = [startingValue]
    ageSpread = [currentAge]
    balance = portfolioSpread[0]

    while (currentAge < retirementAge+1):
        balance = balance + contribution
        balance = balance + balance*growthRate
        currentAge = currentAge + 1
        if currentAge == retirementAge:
            swr = 0.03
            maxIncome = balance*swr
            print("MaxIncome: " , maxIncome)
            entries['Retirement Income'].insert(0,str(round(maxIncome,2)))

        ageSpread.append(currentAge)
        portfolioSpread.append(balance)
    PlotChart(ageSpread,portfolioSpread)

def PlotChart(ageSpread,portfolioSpread):
    plt.bar(ageSpread,portfolioSpread)
    plt.xlabel('Age')
    plt.ylabel('Portfolio Value')
    plt.title('Investment Growth Calculator')
    fig.canvas.draw()

def millions(x, pos):
    'The two args are the value and tick position'
    return '$%1.1fM' % (x*1e-6)

def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect('key_press_event', on_key_event)

if __name__ == '__main__':
    root = Tk()
    root.wm_title("Portfolio Growth Estimator")
    fig = plt.figure(1)
    plt.ion()
    plt.bar(ageSpread,portfolioSpread)
    plt.xlabel('Age')
    plt.ylabel('Portfolio Value')
    plt.title('Investment Growth Calculator')
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))
    b1 = Button(root, text='Calculate',command=(lambda e=ents: CalculatePortfolio(e)))
    b1.pack(side=BOTTOM, padx=5, pady=5)
    b2 = Button(root, text='Quit', command=root.quit)
    b2.pack(side=BOTTOM, padx=5, pady=5)
    root.mainloop()
