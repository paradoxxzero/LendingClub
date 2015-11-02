
from fredapi import Fred
import pandas as pd
from chorogrid import Colorbin, Chorogrid
import os
import numpy as np


from scipy.stats.stats import pearsonr

####### Import the FRED Data #######

api_key = 'f213b90a3ec4042de2259bceceb6ccfa'
os.environ["FRED_API_KEY"] = api_key
apiFred = Fred()
dfFred = apiFred.search_by_release(112)

dfStateUnEmp = dfFred[dfFred['title'].str.contains("Unemployment Rate in ")&~dfFred['title'].str.contains("Census")&dfFred['seasonal_adjustment_short'].str.match('SA')&~dfFred['title'].str.contains('DISCONTINUED')]

srsStateUnIDs = dfStateUnEmp['id'][:]

dictStateUN = {}
for i in srsStateUnIDs:
    dictStateUN[i[:2]] = apiFred.get_series(i,observation_start='2007-01-01').mean()

dfStateUN = pd.DataFrame(list(dictStateUN.items()),columns=['State', 'Unemployment'])


##Make the Map
colors = ['#fff5eb', '#fee6ce', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#8c2d04']
chBin = Colorbin(dfStateUN['Unemployment'], colors, proportional=True, decimals=None)
chBin.set_decimals(1)
chBin.recalc(fenceposts=True)
chBin.fenceposts
colors_out = chBin.colors_out
legend_colors = chBin.colors_in
legend_labels = chBin.labels
cg = Chorogrid('X:\\Documents\\Research\\Tools\\Python\\chorogrid-master\\chorogrid\\databases\\usa_states.csv', list(dfStateUN['State']), colors_out)
cg.set_title('Average Unemployment by State (%)', font_dict={'font-size': 16})
cg.set_legend(legend_colors, legend_labels, title='% Unemployment')
cg.draw_map(spacing_dict={'margin_right': 400})
cg.done(show=True)


####### Import the LC Data #######

path = 'D:\\Andrew\\VM_Storage\\LendingClub\\LoanStats3.csv'

dfListings = pd.read_csv(path)

cat_names = {'Fully Paid': 1, 'Charged Off': 0, 'Current': 1, 'Late (31-120 days)': 0, 'In Grace Period': 1, 'Late (16-30 days)': 0, 'Default': 0, }
dfListings['status_cat'] =  dfListings['loan_status'].map(cat_names)
dfListings = dfListings [~dfListings['status_cat'].isnull()]

grpState = dfListings.groupby('addr_state')
tsNrLoansState = grpState['status_cat'].size()
tsStateDefault = grpState['status_cat'].aggregate(np.mean)[tsNrLoansState>100]

tsStateDefault  = (1-tsStateDefault)*100

chBin = Colorbin(tsStateDefault.values, colors, proportional=True, decimals=None)
chBin.set_decimals(1)
chBin.recalc(fenceposts=True)
chBin.fenceposts
colors_out = chBin.colors_out
legend_colors = chBin.colors_in
legend_labels = chBin.labels

cg = Chorogrid('X:\\Documents\\Research\\Tools\\Python\\chorogrid-master\\chorogrid\\databases\\usa_states.csv', list(tsStateDefault.keys()), colors_out)
cg.set_title('Average Default Rate by State (%)', font_dict={'font-size': 16})
cg.set_legend(legend_colors, legend_labels, title='Default %')
cg.draw_map(spacing_dict={'margin_right': 400})
cg.done(show=True)


