"""
tkinter: used for GUI
random: used for generating random years to choose
matplotlib: used for plotting our monte-carlo results
"""
import tkinter as tk
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

FIELDS = ('Retirement Income', 'Withrdawls Begin At', 'Withdrawls End At', 'Current Portfolio Value',
          'Percent in Stocks (vs. Bonds)', 'Inflation', '# of Simulations')
AGE_SPREAD = [15]
STOCK_ALLOCATION = []
RESULTS_ARRAY = []
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

class YearlyData:
    """ The YearlyData class holds the values of a single simulated year. """
    def __init__(self, stock_return, bond_return, stock_percentage):
        self.stock_return = stock_return
        self.bond_return = bond_return
        self.stock_percentage = stock_percentage

class Investor:
    """ The Investor class holds information that the user enters about themselves. """
    def __init__(self, entries):
        self.withdrawl = (float(entries['Retirement Income'].get()))
        self.current_age = (int(entries['Withrdawls Begin At'].get()))
        self.death_age = (int(entries['Withdrawls End At'].get()))
        self.starting_value = (float(entries['Current Portfolio Value'].get()))
        self.number_of_simulations = (int(entries['# of Simulations'].get()))
        self.stock_percentage = float(entries['Percent in Stocks (vs. Bonds)'].get())
        self.inflation = float(entries['Inflation'].get())

class QuartileResults:
    """ The QuartileResults class holds the simulation number for each quartile. """
    def __init__(self, lower, middle, upper):
        self.lower = lower
        self.middle = middle
        self.upper = upper

def get_final_balance(obj):
    """ Takes in the data from a year and returns it's final balance. """
    return obj.final_balance

def calculate_portfolio(entries):
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
    matrix_length = investor_values.death_age - investor_values.current_age
    matrix_height = investor_values.number_of_simulations
    data_matrix = create_matrix(matrix_length, matrix_height)
    for sim_count in range(investor_values.number_of_simulations):
        iteration_age = investor_values.current_age
        iteration_balance = balance
        length_offset = investor_values.current_age
        for i in range(iteration_age, investor_values.death_age+1):
            current_year_info = get_yearly_information(investor_values)
            iteration_balance = update_balance(iteration_balance,
                                               investor_values.withdrawl, current_year_info)
            data_matrix[sim_count][i-length_offset-1] = iteration_balance
        result_object = Results(sim_count, data_matrix[sim_count][iteration_age-length_offset-1],
                                data_matrix[sim_count][:])
        RESULTS_ARRAY.append(result_object)

    quartile_data = get_quartile_data(investor_values.number_of_simulations)
    plot_trendlines(quartile_data.lower, quartile_data.middle, quartile_data.upper)


def update_balance(iteration_balance, withdrawl, current_year_info):
    """ Takes in a single year's data during a single simulation and updates the balance. """
    iteration_balance = iteration_balance - withdrawl
    stock_balance = iteration_balance * current_year_info.stock_percentage
    bond_balance = iteration_balance * (1-current_year_info.stock_percentage)
    stock_balance = stock_balance + stock_balance * current_year_info.stock_return
    bond_balance = bond_balance + bond_balance * current_year_info.bond_return
    iteration_balance = stock_balance + bond_balance
    return iteration_balance

def get_quartile_data(number_of_simulations):
    """ Take in the number of simulations and output the quartile line numbers. """
    std_increment = round(number_of_simulations/100)
    lower_quartile = round(std_increment*25)
    middle_quartile = round(std_increment*50)
    upper_quartile = round((std_increment*75))
    data_object = QuartileResults(lower_quartile, middle_quartile, upper_quartile)
    return data_object

def plot_trendlines(lower_quartile, middle_quartile, upper_quartile):
    """ Take in the line numbers to plot and output a plot of those lines. """
    plt.clf()
    sorted_results = sorted(RESULTS_ARRAY, key=get_final_balance)
    plt.xlabel('Years of Living on Nest Egg')
    plt.ylabel('Portfolio Value')
    plt.title('Retirement Income Calculator')
    smooth_lower = smooth_trendlines(lower_quartile, 100, sorted_results)
    smooth_middle = smooth_trendlines(middle_quartile, 100, sorted_results)
    smooth_upper = smooth_trendlines(upper_quartile, 100, sorted_results)
    plt.plot(smooth_lower)
    plt.plot(smooth_middle)
    plt.plot(smooth_upper)
    lower_result = round(smooth_lower[-1])
    middle_result = round(smooth_middle[-1])
    upper_result = round(smooth_upper[-1])
    lower_string = str(format(lower_result, ",d"))
    middle_string = str(format(middle_result, ",d"))
    upper_string = str(format(upper_result, ",d"))
    successes = 0
    for i in range(len(sorted_results)):
        if sorted_results[i].final_balance > 0:
            successes += 1
    results_string = ("Success Rate: " + str(round((successes/(len(sorted_results)))*100)) + "%")
    PERFORMANCE_VAR.set(results_string)

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
    year_object = YearlyData(stock_rate, bond_rate-int(inflation), stock_percentage-int(inflation))
    return year_object

def create_form(ROOT):
    """ This creates the main form using tkinter. """
    create_initial_figure()
    create_performance_text()
    ents = make_form(ROOT, FIELDS)
    create_buttons(ents)

def create_initial_figure():
    """ This creates the graph on which the results are ploted. """
    fig = plt.figure(1)
    plt.ion()
    plt.xlabel('Years of Living on Nest Egg')
    plt.ylabel('Portfolio Value')
    plt.title('Retirement Income Calculator')
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
    button_1 = tk.Button(ROOT, text='Calculate', command=(lambda e=ents: calculate_portfolio(e)))
    button_1.pack(side=tk.BOTTOM, padx=5, pady=5)

def create_performance_text():
    """ This creates the text describing how each of the quartiles ended up. """
    global PERFORMANCE_VAR
    PERFORMANCE_VAR = tk.StringVar()
    PERFORMANCE_VAR.set("")
    performance_label = tk.Label(textvariable=PERFORMANCE_VAR, font=(None, 15))
    performance_label.pack(side=tk.TOP)

if __name__ == '__main__':
    ROOT = tk.Tk()
    ROOT.wm_title("FIRE Calculator")
    create_form(ROOT)
    ROOT.mainloop()
