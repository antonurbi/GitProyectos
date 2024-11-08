import pandas as pd
import numpy as np

class FinancialAnalysis:
    
    def __init__(self, data):
        """
        Initialize the class with a DataFrame containing the financial data.
        """
        self.df = data

    def calculate_metrics(self):
        """
        Calculate Gross Profit, Gross Profit Margin, and Operating Expense Ratio.
        """
        try:
            self.df['Gross Profit'] = self.df['Total Revenue'] - self.df['Cost Of Revenue']
            self.df['Gross Profit Margin'] = (self.df['Gross Profit'] / self.df['Total Revenue']) * 100
            self.df['Operating Expense Ratio'] = (self.df['Operating Expense'] / self.df['Total Revenue']) * 100
        except KeyError:
            print('One or more necessary columns are missing.')
    def analyze_growth(self):
        """
        Calculate year-over-year growth for revenue metrics.
        """
        try:
            for column in ['Total Revenue', 'Operating Revenue']:
                self.df[f'{column} Growth Rate'] = self.df[column].pct_change() * 100
        except KeyError:
            print('One or more necessary columns are missing.')
    def categorize_performance(self):
        """
        Categorize each year's performance into one of five categories based on financial metrics.
        """
        try:
            conditions = [
                (self.df['Gross Profit Margin'] > 40),
                (self.df['Gross Profit Margin'] > 30) & (self.df['Gross Profit Margin'] <= 40),
                (self.df['Gross Profit Margin'] > 20) & (self.df['Gross Profit Margin'] <= 30),
                (self.df['Gross Profit Margin'] > 10) & (self.df['Gross Profit Margin'] <= 20),
                (self.df['Gross Profit Margin'] <= 10)
            ]
            categories = ['Excellent', 'Good', 'Average', 'Below Average', 'Poor']
            self.df['Performance Category'] = pd.cut(self.df['Gross Profit Margin'], bins=[-np.inf, 10, 20, 30, 40, np.inf], labels=categories, right=False)
        except KeyError:
            print('One or more necessary columns are missing.')
class ProfitabilityMetrics:
    def __init__(self, data):
        """
        Initialize the class with a DataFrame containing the financial data.
        """
        self.df = data

    def calculate_metrics(self):
        """
        Calculate and append profitability related metrics to the DataFrame.
        """
        try: 
            self.df['Operating Margin'] = (self.df['Operating Income'] / self.df['Total Revenue']) * 100
            self.df['EBITDA Margin'] = (self.df['EBITDA'] / self.df['Total Revenue']) * 100
            self.df['Net Profit Margin'] = (self.df['Net Income'] / self.df['Total Revenue']) * 100
        except KeyError:
            print('One or more necessary columns are missing.')
    def analyze_trends(self):
        """
        Analyze historical trends for profitability metrics.
        """
        try:
            self.trends = {
                'Operating Income Trend': self.df['Operating Income'].pct_change(),
                'EBITDA Trend': self.df['EBITDA'].pct_change(),
                'Net Income Trend': self.df['Net Income'].pct_change()}
        except KeyError:
            print('One or more necessary columns are missing.')
        

    def categorize_performance(self):
        """
        Categorize performance based on Net Profit Margin.
        """
        try:
            conditions = [
                (self.df['Net Profit Margin'] > 20),
                (self.df['Net Profit Margin'] > 15) & (self.df['Net Profit Margin'] <= 20),
                (self.df['Net Profit Margin'] > 10) & (self.df['Net Profit Margin'] <= 15),
                (self.df['Net Profit Margin'] > 5) & (self.df['Net Profit Margin'] <= 10),
                (self.df['Net Profit Margin'] <= 5)
            ]
            categories = ['Excellent', 'Very Good', 'Good', 'Fair', 'Poor']
            self.df['Profitability Category'] = pd.cut(self.df['Net Profit Margin'], bins=[-np.inf, 5, 10, 15, 20, np.inf], labels=categories, right=False)
        except KeyError:
            print('One or more necessary columns are missing.') 
class CashFlowMetrics:
    def __init__(self, data):
        """
        Initialize the class with a DataFrame containing the financial data.
        """
        self.df = data

    # def analyze_depreciation(self):
    #     """
    #     Analyze adjustments made to standard depreciation.
    #     """
    #     # Example calculation (assuming depreciation columns exist)
    #     self.df['Reconciled Depreciation Impact'] = self.df['Reconciled Depreciation'] - self.df['Standard Depreciation']
    #     self.df['Depreciation Adjustment Ratio'] = self.df['Reconciled Depreciation'] / self.df['Standard Depreciation']

    def analyze_non_operating_income_expenses(self):
        """
        Review and analyze non-operating income and expenses trends.
        """
        try:
            self.df['Non Operating Impact'] = self.df['Other Non Operating Income Expenses'] / self.df['Operating Income']
        except KeyError:
            print('One or more necessary columns are missing.')

    def calculate_free_cash_flow(self):
        """
        Calculate Free Cash Flow.
        """
        try:
            self.df['Free Cash Flow'] = self.df['Reconciled Depreciation'] - self.df['Other Non Operating Income Expenses']
        except KeyError:
            print('One or more necessary columns are missing.')
    def cash_flow_analysis(self):
        """
        Assess the impact of metrics on overall cash flow.
        """
        try:
            self.df['Cash Flow Stability'] = self.df['Free Cash Flow'].rolling(window=3).std()
        except KeyError:
            print('One or more necessary columns are missing.')
    def categorize_performance(self):
        """
        Categorize performance based on cash flow metrics.
        """
        try: 
            conditions = [
                (self.df['Free Cash Flow'] > 0),
                (self.df['Free Cash Flow'] < 0)
            ]
            categories = ['Positive Cash Flow', 'Negative Cash Flow']
            self.df['Cash Flow Category'] = np.select(conditions, categories)
        except KeyError:
            print('One or more necessary columns are missing.') 
class LiquidityAndEfficiencyMetrics:
    def __init__(self, data):
        """
        Initialize the class with a DataFrame containing the financial data.
        """
        self.df = data

    def calculate_ratios(self):
        """
        Calculate key financial ratios relevant to liquidity and efficiency.
        """
        try:
            self.df['R&D to Revenue Ratio'] = (self.df['Research And Development'] / self.df['Total Revenue']) * 100
            self.df['SG&A to Revenue Ratio'] = (self.df['Selling General And Administration'] / self.df['Total Revenue']) * 100
            self.df['Operating Expense Ratio'] = (self.df['Operating Expense'] / self.df['Total Revenue']) * 100
            self.df['Expense to Revenue Ratio'] = (self.df['Total Expenses'] / self.df['Total Revenue']) * 100
        except KeyError:
            print('One or more necessary columns are missing.')
    def analyze_trends(self):
        """
        Analyze trends in the calculated financial ratios.
        """
        try:
            trend_metrics = ['R&D to Revenue Ratio', 'SG&A to Revenue Ratio', 'Operating Expense Ratio', 'Expense to Revenue Ratio']
            for metric in trend_metrics:
                self.df[f'{metric} Trend'] = self.df[metric].pct_change() * 100
        except KeyError:
            print('One or more necessary columns are missing.')
    def categorize_performance(self):
        """
        Categorize performance based on efficiency ratios.
        """
        try:
            # Define categories for each ratio
            categories = {
                'R&D to Revenue Ratio': {'High Investment': 15, 'Moderate Investment': 10, 'Low Investment': 5, 'Very Low Investment': 0},
                'SG&A to Revenue Ratio': {'High SG&A Spending': 30, 'Moderate SG&A Spending': 20, 'Low SG&A Spending': 10, 'Very Low SG&A Spending': 5},
                'Operating Expense Ratio': {'High Operating Cost': 60, 'Moderate Operating Cost': 40, 'Low Operating Cost': 20, 'Very Low Operating Cost': 10},
            }

            for ratio, thresholds in categories.items():
                # Sort the threshold values and include negative infinity for the lower bound and positive infinity for the upper bound
                sorted_thresholds = [-float('inf')] + sorted(thresholds.values()) + [float('inf')]

                # Labels for the categories, adjusted to match intervals created by the sorted_thresholds
                cat_labels = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']  # Includes an extra category for the highest interval

                # Apply the categorization
                self.df[f'{ratio} Category'] = pd.cut(self.df[ratio], bins=sorted_thresholds, labels=cat_labels, right=False)
        except KeyError:
            print('One or more necessary columns are missing.')
class DebtAndInterestMetrics:
    def __init__(self, data):
        """
        Initialize the class with a DataFrame containing the financial data.
        """
        self.df = data

    def calculate_ratios(self):
        """
        Compute crucial financial ratios related to debt and interest.
        """
        try:
            self.df['Interest Coverage Ratio'] = self.df['EBIT'] / self.df['Interest Expense']
            self.df['Net Interest Margin'] = (self.df['Net Interest Income'] / self.df['Total Expenses']) * 100
        except KeyError:
            print('One or more necessary columns are missing.')
      
    def analyze_trends(self):
        """
        Analyze trends in interest-related metrics and ratios.
        """
        try:
            trend_metrics = ['Interest Expense', 'Net Interest Income', 'Interest Coverage Ratio', 'Net Interest Margin']
            for metric in trend_metrics:
                self.df[f'{metric} Trend'] = self.df[metric].pct_change() * 100
        except KeyError:   
            print('One or more necessary columns are missing.')
    def categorize_performance(self):
        """
        Categorize performance based on financial ratios.
        """
        try:
            # Categorization based on Interest Coverage Ratio
            conditions = [
                (self.df['Interest Coverage Ratio'] < 1.5),
                (self.df['Interest Coverage Ratio'] >= 1.5) & (self.df['Interest Coverage Ratio'] < 2.5),
                (self.df['Interest Coverage Ratio'] >= 2.5)
            ]
            categories = ['High Risk', 'Moderate Risk', 'Low Risk']
            self.df['Interest Coverage Category'] = pd.cut(self.df['Interest Coverage Ratio'], bins=[0, 1.5, 2.5, float('inf')], labels=categories, right=False)

            # Categorization based on Net Interest Margin
            conditions = [
                (self.df['Net Interest Margin'] < 2),
                (self.df['Net Interest Margin'] >= 2) & (self.df['Net Interest Margin'] < 5),
                (self.df['Net Interest Margin'] >= 5)
            ]
            categories = ['Low Efficiency', 'Moderate Efficiency', 'High Efficiency']
            self.df['Net Interest Margin Category'] = pd.cut(self.df['Net Interest Margin'], bins=[0, 2, 5, float('inf')], labels=categories, right=False)
        except KeyError:
            print('One or more necessary columns are missing.')
class TaxationAndMinorityInterestMetrics:
    def __init__(self, data):
        """
        Initialize the class with a DataFrame containing the financial data.
        """
        self.df = data

    def calculate_indicators(self):
        """
        Compute key indicators to assess tax management and minority interest impacts.
        """
        try:
            self.df['Effective Tax Rate (ETR)'] = (self.df['Tax Provision'] / self.df['Pretax Income']) * 100
            self.df['Minority Interest Percentage'] = (self.df['Net Income From Continuing Operation Net Minority Interest'] / self.df['Net Income Including Noncontrolling Interests']) * 100
        except KeyError:
            print('One or more necessary columns are missing.')
    def analyze_trends(self):
        """
        Analyze trends in tax provisions, effective tax rates, and minority interests.
        """
        try:
            trend_metrics = ['Tax Provision', 'Effective Tax Rate (ETR)', 'Net Income From Continuing Operation Net Minority Interest']
            for metric in trend_metrics:
                self.df[f'{metric} Trend'] = self.df[metric].pct_change() * 100
        except KeyError:
            print('One or more necessary columns are missing.')
    def categorize_performance(self):
        """
        Categorize performance based on financial ratios.
        """
        try:
        # Categorization based on Effective Tax Rate (ETR)
            self.df['ETR Category'] = pd.cut(self.df['Effective Tax Rate (ETR)'], bins=[0, 20, 35, 50, float('inf')],
                                            labels=['Low', 'Moderate', 'High', 'Very High'], right=False)

            # Categorization based on Minority Interest Percentage
            self.df['Minority Interest Category'] = pd.cut(self.df['Minority Interest Percentage'], bins=[0, 10, 20, 30, float('inf')],
                                                        labels=['Low', 'Moderate', 'High', 'Very High'], right=False)
        except KeyError:
            print('One or more necessary columns are missing.')
class EPSShareMetrics:
    def __init__(self, data):
        """
        Initialize the class with a DataFrame containing the financial data.
        """
        self.df = data

    def calculate_eps(self):
        """
        Compute both Basic and Diluted EPS for each year.
        """
        try:
            self.df['Basic EPS'] = self.df['Net Income'] / self.df['Basic Average Shares']
            self.df['Diluted EPS'] = self.df['Diluted NI Availto Com Stockholders'] / self.df['Diluted Average Shares']
        except KeyError:   
            print('One or more necessary columns are missing.')
    def analyze_trends(self):
        """
        Examine the trends in EPS over the collected period.
        """
        try:
            self.df['Basic EPS Trend'] = self.df['Basic EPS'].pct_change() * 100
            self.df['Diluted EPS Trend'] = self.df['Diluted EPS'].pct_change() * 100
        except KeyError:
            print('One or more necessary columns are missing.')
    def dilution_analysis(self):
        """
        Assess the effect of potential dilution.
        """
        try:
            self.df['Dilution Impact'] = self.df['Basic EPS'] - self.df['Diluted EPS']
            self.df['Percentage of Dilution'] = (self.df['Dilution Impact'] / self.df['Basic EPS']) * 100
        except KeyError:
            print('One or more necessary columns are missing.')
    def categorize_performance(self):
        """
        Provide actionable insights based on EPS growth and dilution effects.
        """
        try:
            conditions = [
                (self.df['Basic EPS Trend'] > 0) & (self.df['Percentage of Dilution'] < 5),
                (self.df['Percentage of Dilution'] >= 5)
            ]
            categories = ['Strong Investment Opportunity', 'Potential Dilution Concern']
            self.df['EPS Performance Category'] = pd.cut(self.df['Basic EPS Trend'], bins=[-float('inf'), 0, float('inf')],
                                                        labels=categories)
        except KeyError:
            print('One or more necessary columns are missing.')
class SpecialItemsMetrics:
    def __init__(self, data):
        """
        Initialize the class with a DataFrame containing the financial data.
        """
        self.df = data

    def categorize_items(self):
        """
        Categorize special items into incomes and expenses.
        """
        try:
        # Assuming columns for each type of item are defined in the DataFrame
            self.df['Unusual Expenses'] = self.df['Total Unusual Items'] + self.df['Special Income Charges']
            self.df['Unusual Incomes'] = self.df['Gain On Sale Of Business'] + self.df['Gain On Sale Of Security']
        except KeyError:
            self.df['Unusual Incomes'] = 0
    def analyze_individual_impact(self):
        """
        Evaluate the impact of each category on the financials.
        """
        try:
            
            self.df['Impact on Net Income'] = self.df['Unusual Expenses'] + self.df['Unusual Incomes']
            self.df['Percentage of Net Income'] = (self.df['Impact on Net Income'] / self.df['Net Income']) * 100
        except KeyError:
            pass
    def trend_analysis(self):
        """
        Examine trends in the frequency and impact of unusual items.
        """
        try:
            self.df['Frequency of Unusual Items'] = self.df[['Total Unusual Items', 'Special Income Charges', 'Gain On Sale Of Security']].notnull().sum(axis=1)
            self.df['Direction of Impact'] = self.df['Impact on Net Income'].apply(lambda x: 'Gain' if x > 0 else 'Loss')
        except KeyError:
            pass
    def normalize_earnings(self):
        """
        Calculate earnings excluding all unusual items to assess underlying performance.
        """
        try:
            self.df['Normalized Earnings'] = self.df['Net Income'] - self.df['Impact on Net Income']
        except KeyError:
            pass