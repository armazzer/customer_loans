import matplotlib.pyplot as plt
import missingno as msno
import numpy as np
import pandas as pd
import plotly_express as px
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import normaltest
from statsmodels.graphics.gofplots import qqplot

class Plotter:
    def __init__ (self, data):
        self.data = data
        self.ax = None

    def msno_plot(self):
        msno.matrix(self.data)
    
    def heatmap(self, w, h):
        plt.figure(figsize=(w, h))
        sns.heatmap(self.data.isnull(), cmap='viridis', cbar=False)
        plt.title('Missing Data Heatmap')
        plt.show()
    
    def corr_calc(self):
        numeric_cols = self.data.select_dtypes(include=["int64", "float64"])
        correlation_matrix = numeric_cols.corr()
        return correlation_matrix

    def correlation(self, w, h):
        correlation_matrix = self.corr_calc()
        plt.figure(figsize=(w, h))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
        plt.show()

    def scatter(self, x, y, hue=None, loc="upper left"):
        sns.scatterplot(data=self.data, x=x, y=y, hue=hue)
        plt.legend(loc=loc, title=hue)
        plt.show()

    def scatter_reg(self, x, y, text_x=1, text_y=1):
        sns.regplot(data=self.data, x=x, y=y, scatter_kws={'s': 10}, line_kws={'color': 'red'})
        plt.gca().set_zorder(1) 
        model = sm.OLS(self.data[y], sm.add_constant(self.data[x])).fit()
        plt.text(text_x, text_y, f"Y = {model.params[0]:.2f} + {model.params[1]:.3f}X\nR-squared = {model.rsquared:.3f}", fontsize=10)

    def histogram(self, column, bins=20, kde=True):
        self.ax = sns.histplot(self.data[column], bins=bins, kde=kde)
        return self
        
    def format_hist(self, x_rot=45, num_labels=20):
        self.ax.tick_params(axis='x', rotation=x_rot)
        self.ax.xaxis.set_major_locator(plt.MaxNLocator(num_labels))
        plt.show()
        #return self
    
    def qq_plot(self, column):
        qqplot(self.data[column], scale=1, line='q')
        plt.show()

    def k2_test(self, column):
        data = self.data[column]
        # D’Agostino’s K^2 Test
        stat, p = normaltest(data, nan_policy='omit')
        print(f"{column}:", "K^2 test statistic = %.3f, p = %.3f" % (stat, p))
        return round(stat, 2)
    
    def skew_test(self, column):
        data = self.data[column]
        skew = data.skew()
        skew = round(skew, 3)
        print(f"{column}: skew = {skew}")
        return skew

    def dpd_plot(self, column, x_rot=0, legend=None):
        probabilities = self.data[column].value_counts(normalize=True)
        sns.barplot(y=probabilities.values, x=probabilities.index)
        plt.ylabel("Probability")
        plt.xticks(rotation=x_rot)

    def dpd_multi_plot(self, columns, x_rot):
        probabilities = self.data[columns].value_counts(normalize=True)
        probabilities_df = pd.DataFrame(probabilities)
        sns.barplot(probabilities_df, y="proportion", x=columns[0], hue=columns[1])
        plt.ylabel("Probability")
        plt.xticks(rotation=x_rot)

    def sns_barplot(self, x_col, y_col, hue=None, x_rot=0):
        sns.barplot(self.data, x=x_col, y=y_col, hue=hue)
        plt.ylabel(y_col)
        plt.xticks(rotation=x_rot)

    def bar_plot(self, columns, y_label, w, h):
        fig, ax1 = plt.subplots(figsize=(w, h))
        self.data[columns].plot(kind='bar', ax=ax1, width=0.5)
        ax1.set_ylabel(y_label)
        ax1.tick_params(axis='y')
        fig.tight_layout()

    def dual_prob_plot(self, col_x, col_cat, marginal="box", barnorm="fraction", w=500, h=500):
        fig = px.histogram(self.data, x=col_x, color=col_cat, marginal=marginal, barnorm=barnorm, title='Probability Bar Plots', width=w, height=h)
        fig.show()

    def bar_plot_twin_y(self, column_a, column_b, y_left, y_right, w, h):
        fig, ax1 = plt.subplots(figsize=(w, h))

        color1 = 'tab:blue'
        self.data[column_a].plot(kind='bar', ax=ax1, width=0.5, position=1, color=color1)
        ax1.set_ylabel(y_left, color=color1)
        ax1.tick_params(axis='y', labelcolor=color1)
        #ax1.set_ylim(bottom=-2.5) need to work out default values for these
        #ax1.set_ylim(top=35)

        ax2 = ax1.twinx()
        color2 = 'tab:red'
        self.data[column_b].plot(kind='bar', ax=ax2, width=0.5, position=0, color=color2)
        ax2.set_ylabel(y_right, color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        #ax2.set_ylim(bottom=-25000)
        #ax2.set_ylim(top=350000)
        fig.tight_layout()

    def box_plot(self, column, w=2.5, h=3):
        plt.figure(figsize=(w, h))
        sns.boxplot(y=self.data[column], color='lightgreen', showfliers=True)
        plt.title(f'Box plot of {column}')
        plt.show()

    def box_plot_px(self, column, points, w, h):
        fig = px.box(self.data[column], y=column , points=points, width=w, height=h)
        fig.show()

    def box_plot_multi(self, columns, points, w, h):
        fig = px.box(self.data[columns], y=columns , points=points, width=w, height=h)
        fig.show()

# Create class that inherits from Plotter

class SkewChecker(Plotter):
   def __init__ (self, data):
        super().__init__(data)
        self.skew_dict = {}
        self.k2_dict = {} 

   def skew_check(self, column, bins=20, kde=True, rot=45, num_labels=20):
        skew = self.skew_test(column)
        self.skew_dict[column] = skew
        k2 = self.k2_test(column)
        self.k2_dict[column] = k2
        self.histogram(column, bins, kde).format_hist(rot, num_labels)
        self.qq_plot(column)

   def show_skew_dict(self):
        print(self.skew_dict)
        return(self.skew_dict)
   
   def show_k2_dict(self):
        print(self.k2_dict)
        return(self.k2_dict)
   
   # Create another class that inherits from Plotter

class PlotStats(Plotter):
    def __init__ (self, data):
        super().__init__(data)
        self.quantiles_dict = {}

    def quantiles(self, column):
        # Box plot
        self.box_plot(column)
        # Calculate IQR
        num_types = ["int64", "float64"]
        Q1 = round((np.percentile(self.data[column], 25)), 3) if self.data[column].dtypes in num_types else np.percentile(self.data[column], 25)
        Q3 = round((np.percentile(self.data[column], 75)), 3) if self.data[column].dtypes in num_types else np.percentile(self.data[column], 75)
        IQR = round((Q3 - Q1), 3) if self.data[column].dtypes in num_types else Q1 - Q3
        # Calculate Whiskers
        lower_whisker = round((Q1 - 1.5 * IQR), 3) if self.data[column].dtypes in num_types else Q1 - 1.5 * IQR
        upper_whisker = round((Q3 + 1.5 * IQR), 3) if self.data[column].dtypes in num_types else Q1 + 1.5 * IQR
        quantiles_dict_col = {"Q1": Q1, "Q3": Q3, "IQR": IQR, "lower_whisker": lower_whisker, "upper_whisker": upper_whisker}
        self.quantiles_dict[column] = quantiles_dict_col
        print(f"{column}: {quantiles_dict_col}")

    def show_quantiles(self):
        print(self.quantiles_dict)
        return(self.quantiles_dict)