
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