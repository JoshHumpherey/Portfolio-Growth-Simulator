"""
tkinter: used for GUI
random: used for generating random years to choose
matplotlib: used for plotting our monte-carlo results
"""
import tkinter as tk
import random
import matplotlib
import time
from functools import wraps
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

FIELDS = ('Annual Contribution', 'Current Age', 'Retirement Age', 'Current Portfolio Value',
          'Percent in Stocks (vs. Bonds)', 'Inflation')
AGE_SPREAD = [15]
STOCK_ALLOCATION = []

STRATEGIES = {'Fixed Allocations', 'Shifting Bond Allocations'}
OFFSET = 1928
STOCK_MAP = dict()
BOND_MAP = dict()

with open('stock_history.txt') as stock_file:
    STOCK_DATA = stock_file.readlines()
    for year in range(OFFSET, 2017):
        STOCK_MAP[year] = STOCK_DATA[year-OFFSET]

with open('bond_history.txt') as bond_file:
    BOND_DATA = bond_file.readlines()
    for year in range(OFFSET, 2017):
        BOND_MAP[year] = BOND_DATA[year-OFFSET]

class Results:
    """ The Results class holds the data from a signle simulation instance. """
    def __init__(self, simulation_number, final_balance, growth_history):
        self.simulation_number = simulation_number
        self.final_balance = final_balance
        self.growth_history = growth_history

class Investor:
    """ The Investor class holds information that the user enters about themselves. """
    def __init__(self, entries):
        self.contribution = (float(entries['Annual Contribution'].get()))
        self.current_age = (int(entries['Current Age'].get()))
        self.retirement_age = (int(entries['Retirement Age'].get()))
        self.starting_value = (float(entries['Current Portfolio Value'].get()))
        self.stock_percentage = float(entries['Percent in Stocks (vs. Bonds)'].get())/100
        self.inflation = float(entries['Inflation'].get())/100
        self.investment_timeline = int(self.retirement_age-self.current_age)

def get_final_balance(obj):
    """ Takes in the data from a year and returns it's final balance. """
    return obj.final_balance

def calculate_portfolio(entries, results_array):
    """
    This is currently the main method for the program.
    It uses nested while loops to simulate an investors lifetime (inner loop)
    a certain number of times (outer loop)
    and then output and graph the results.
    """
    investor_values = Investor(entries)
    STOCK_ALLOCATION.append(investor_values.stock_percentage)
    portfolio_spread = [investor_values.starting_value]
    balance = float(portfolio_spread[0])
    matrix_length = investor_values.retirement_age - investor_values.current_age
    matrix_height = 10000
    data_matrix = create_matrix(matrix_length, matrix_height)
    for sim_count in range(10000):
        iteration_age = investor_values.current_age
        iteration_balance = balance
        length_offset = investor_values.current_age
        for i in range(iteration_age, investor_values.retirement_age+1):
            current_year_tuple = get_yearly_information(investor_values)
            iteration_balance = update_balance(iteration_balance,
                                               investor_values.contribution, current_year_tuple)
            data_matrix[sim_count][i-length_offset-1] = iteration_balance
        result_object = Results(sim_count, data_matrix[sim_count][iteration_age-length_offset-1],
                                data_matrix[sim_count][:])
        results_array.append(result_object)

    quartile_tuple = get_quartile_data(10000)
    plot_trendlines(quartile_tuple, results_array)
    display_capital(investor_values.investment_timeline, investor_values.contribution, investor_values.starting_value)

def update_balance(iteration_balance, contribution, current_year_tuple):
    """ Takes in a single year's data during a single simulation and updates the balance. """
    STOCK_RATE = 0
    BOND_RATE = 1
    STOCK_PCT = 2
    iteration_balance = iteration_balance + contribution
    stock_balance = iteration_balance * current_year_tuple[STOCK_PCT]
    bond_balance = iteration_balance * (1-current_year_tuple[STOCK_PCT])
    stock_balance += (stock_balance * current_year_tuple[STOCK_RATE])
    bond_balance += (bond_balance * current_year_tuple[BOND_RATE])
    #print("Portfolio started at " + str(iteration_balance) + " and after a year of " + str(current_year_tuple[STOCK_RATE]) + " change it is now at: " + str(stock_balance + bond_balance))
    iteration_balance = stock_balance + bond_balance
    return iteration_balance

def get_quartile_data(number_of_simulations):
    """ Take in the number of simulations and output the quartile line numbers. """
    std_increment = round(number_of_simulations/100)
    lower_quartile = round(std_increment*5)
    middle_quartile = round(std_increment*10)
    upper_quartile = round((std_increment*15))
    quartile_tuple = (lower_quartile, middle_quartile, upper_quartile)
    return quartile_tuple

def plot_trendlines(quartile_tuple, results_array):
    """ Take in the line numbers to plot and output a plot of those lines. """
    plt.clf()
    LOWER = 0
    MID = 1
    UPPER = 2
    sorted_results = sorted(results_array, key=get_final_balance)
    plt.xlabel('Years of Growth')
    plt.ylabel('Portfolio Value')
    plt.title('Investment Growth Calculator')
    smooth_lower = smooth_trendlines(quartile_tuple[LOWER], 100, sorted_results)
    smooth_middle = smooth_trendlines(quartile_tuple[MID], 100, sorted_results)
    smooth_upper = smooth_trendlines(quartile_tuple[UPPER], 100, sorted_results)
    plt.plot(smooth_lower)
    plt.plot(smooth_middle)
    plt.plot(smooth_upper)
    lower_result = round(smooth_lower[-1])
    middle_result = round(smooth_middle[-1])
    upper_result = round(smooth_upper[-1])
    lower_string = str(format(lower_result, ",d"))
    middle_string = str(format(middle_result, ",d"))
    upper_string = str(format(upper_result, ",d"))
    results_string = ("  Bottom Quartile: $" + lower_string + " * Middle Quartile: $"
                      + middle_string + " * Upper Quartile: $" + upper_string + "  ")
    PERFORMANCE_VAR.set(results_string)

def display_capital(investment_length, added_yearly, initial_capital):
    total_capital = round(initial_capital + (investment_length*added_yearly))
    formatted_capital = str(format(total_capital, ",d"))
    results_string = ("Total Invesment Capital: $" + formatted_capital)
    CAPITAL_VAR.set(results_string)

def smooth_trendlines(n_quartile, smooth_amount, sorted_results):
    """ This averages the results of a quartile against it's neighbours. """
    half = (smooth_amount) // 2
    my_line = sorted_results[n_quartile].growth_history
    for line in range(n_quartile-half, n_quartile+half):
        other_line = sorted_results[line].growth_history
        for i in range(len(my_line)):
            my_line[i] += other_line[i]
    for i in range(len(my_line)):
        my_line[i] /= smooth_amount
    return my_line

def create_matrix(length, height):
    """ Creates a matrix to store data in using a certain length and height. """
    matrix = [[0 for x in range(length)] for y in range(height)]
    return matrix

def get_yearly_information(investor_information):
    """ This function grabs stock/bond data from a random year. """
    random_year = random.randint(1928, 2016)
    inflation = investor_information.inflation
    stock_rate = float(STOCK_MAP[random_year])
    bond_rate = float(BOND_MAP[random_year])
    stock_percentage = float(STOCK_ALLOCATION[0])
    year_tuple = (stock_rate-int(inflation), bond_rate-int(inflation), stock_percentage)
    return year_tuple

def create_form(ROOT):
    """ This creates the main form using tkinter. """
    create_initial_figure()
    create_performance_text()
    ents = make_form(ROOT, FIELDS)
    create_buttons(ents)
    ROOT.wm_iconbitmap('images/money.ico')

def create_initial_figure():
    """ This creates the graph on which the results are ploted. """
    fig = plt.figure(1)
    plt.ion()
    plt.xlabel('Years of Growth')
    plt.ylabel('Portfolio Value')
    plt.title('Investment Growth Calculator')
    canvas = FigureCanvasTkAgg(fig, master=ROOT)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack()

def make_form(ROOT, FIELDS):
    """ This takes our FIELDS parameter and generates text boxes from them. """
    entries = {}
    for field in FIELDS:
        row = tk.Frame(ROOT)
        lab = tk.Label(row, width=22, text=field+": ", anchor='w')
        ent = tk.Entry(row)
        ent.insert(0, "0")
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries[field] = ent
    return entries

def create_buttons(ents):
    """ This creates the buttons a user can interact with. """
    button_2 = tk.Button(ROOT, text='Quit', command=ROOT.quit)
    button_2.pack(side=tk.BOTTOM, padx=5, pady=5)
    button_1 = tk.Button(ROOT, text='Calculate', command=(lambda e=ents: calculate_portfolio(e, [])))
    button_1.pack(side=tk.BOTTOM, padx=5, pady=5)

def create_performance_text():
    """ This creates the text describing how each of the quartiles ended up. """
    global PERFORMANCE_VAR
    global CAPITAL_VAR
    PERFORMANCE_VAR = tk.StringVar()
    PERFORMANCE_VAR.set("")
    performance_label = tk.Label(textvariable=PERFORMANCE_VAR, font=(None, 15))
    performance_label.pack(side=tk.TOP)

    CAPITAL_VAR = tk.StringVar()
    CAPITAL_VAR.set("")
    capital_label = tk.Label(textvariable=CAPITAL_VAR, font=(None, 15))
    capital_label.pack(side=tk.TOP)

if __name__ == '__main__':
    ROOT = tk.Tk()
    ROOT.wm_title("Portfolio Growth Estimator")
    create_form(ROOT)
    ROOT.mainloop()
