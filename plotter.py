
import missingno as msno
import seaborn as sns
import matplotlib.pyplot as plt
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
    
    def correlation(self, w, h):
        numeric_cols = self.data.select_dtypes(include=["int64", "float64"])
        correlation_matrix = numeric_cols.corr()
        plt.figure(figsize=(w, h))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)

    def scatter(self, x, y):
        sns.scatterplot(data=self.data, x=x, y=y)

    def scatter_reg(self, x, y):
        sns.regplot(data=self.data, x=x, y=y, scatter_kws={'s': 10}, line_kws={'color': 'red'})
        plt.gca().set_zorder(1) 
        #model = sm.OLS(self.data[y], sm.add_constant(self.data[x])).fit()
        #plt.text(1.5, 5, f"Y = {model.params[0]:.2f} + {model.params[1]:.2f}X\nR-squared = {model.rsquared:.2f}", fontsize=10)

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

    def dpd_plot(self, column, x_rot):
        probabilities = self.data[column].value_counts(normalize=True)
        dpd = sns.barplot(y=probabilities.values, x=probabilities.index)
        plt.ylabel("Probability")
        plt.xticks(rotation=x_rot)

    def bar_plot(self, columns, y_label, w, h):
        fig, ax1 = plt.subplots(figsize=(w, h))
        self.data[columns].plot(kind='bar', ax=ax1, width=0.5)
        ax1.set_ylabel(y_label)
        ax1.tick_params(axis='y')
        fig.tight_layout()

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
