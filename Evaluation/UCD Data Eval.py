import seaborn as sns  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from scipy.stats import shapiro
from scipy.stats import ttest_rel
from scipy.stats import wilcoxon


# load data
data = pd.read_csv('ucd data.csv')
pd.DataFrame(data)

data.drop(['Unnamed: 12'], axis=1, inplace=True)
data.drop(['Unnamed: 13'], axis=1, inplace=True)
data.drop(['Unnamed: 14'], axis=1, inplace=True)
data.drop(['Unnamed: 15'], axis=1, inplace=True)

data = data.iloc[0:20]

for col in data.columns[:-1]:
    data[col] = data[col].astype(int)

# create masks to separate groups
a_mask = data['group'] == 'a'
b_mask = data['group'] == 'b'

# split groups
group_a = data[a_mask]
group_b = data[b_mask]

# drop columns not needed for analysis
group_a = group_a.drop(['group', 'pp'], axis=1)
group_b = group_b.drop(['group', 'pp'], axis=1)

# confirm group lengths
# print(f'group A length: {len(group_a)}')
# print(f'group B length: {len(group_b)}')


# select variables for analysis (deslect homescreen ratings)
d_variables = data.columns[1:-3]



sig_diff = []

# perform tests
for var in d_variables:
    
    p_list = []

    # check normality
    stat, p = shapiro(group_a[var])
    p_list.append(p)

    if p > 0.05:
        print(f"Group A {var} is normally distributed.")
    else:
        print(f"Group A {var} is NOT normally distributed.")
    print(f'group A p-value = {p}\n')


    stat, p = shapiro(group_b[var])
    p_list.append(p)

    if p > 0.05:
        print(f"Group B {var} is normally distributed.")
    else:
        print(f"Group B {var} is NOT normally distributed.")
    print(f'group B p-value = {p}\n')

    # perform tests of difference
    if p_list[0] > 0.05 and p_list[1] > 0.05:
        stat, test_p = ttest_rel(group_a[var], group_b[var])
        print(f'T-test p-value = {test_p}')
        print(f'T-test stat = {stat}\n')
    else:
        stat, test_p = wilcoxon(group_a[var], group_b[var])
        print(f'Wilcoxon p-value = {test_p}')
        print(f'Wilcoxon stat = {stat}\n')

    
    if test_p > 0.05:
        print("There is NO significant difference between groups.")
    else:
        print("There IS a significant difference between groups.")
        sig_diff.append(var)

    # compare medians
    group_a_median = group_a[var].median()
    group_b_median = group_b[var].median()
    median_diff = group_a_median - group_b_median

    if group_a_median > group_b_median:
        print(f"Group A median ({group_a_median}) is greater than Group B median ({group_b_median}).")
    elif group_a_median < group_b_median:
        print(f"Group B median ({group_b_median}) is greater than Group A median ({group_a_median}).")

    print("-----------------------------\n")

 
# redifining data for homescreen ratings
group_a = data[a_mask]
group_b = data[b_mask]

homescreen_a_ratings = data.iloc[:,9]
homescreen_b_ratings = data.iloc[:,10]

# normalise ratings to 0-1
homescreen_a_ratings = homescreen_a_ratings.apply(lambda x: x / 5)
homescreen_b_ratings = homescreen_b_ratings.apply(lambda x: x / 5)

p_list = []

# check normality of homescreen ratings A
stat, p = shapiro(homescreen_a_ratings)
print(f'homescreen A p-value = {p}')
p_list.append(p)

if p > 0.05:
    print(f"homescreen A ratings ARE normally distributed.\n")
else:
    print(f"homescreen A ratings are NOT normally distributed.\n")

# check normality of homescreen ratings B
stat, p = shapiro(homescreen_b_ratings)
print(f'homescreen B p-value = {p}')
p_list.append(p)

if p > 0.05:
    print(f"homescreen B ratings ARE normally distributed.\n")
else:
    print(f"homescreen B ratings are NOT normally distributed.\n")


# perform tests of significance
if p_list[0] > 0.05 and p_list[1] > 0.05:
    stat, test_p = ttest_rel(homescreen_a_ratings, homescreen_b_ratings)
    print(f'T-test p-value = {test_p}\n')
    print(f'T-test stat = {stat}\n')

    # find centres of each group
    homescreen_a_centre = homescreen_a_ratings.mean()
    homescreen_b_centre = homescreen_b_ratings.mean()
    centre_diff = homescreen_a_centre - homescreen_b_centre
    if homescreen_a_centre > homescreen_b_centre:
        print(f"Group A mean ({homescreen_a_centre}) is greater than Group B mean ({homescreen_b_centre}).")
    elif homescreen_a_centre < homescreen_b_centre:
        print(f"Group B mean ({homescreen_b_centre}) is greater than Group A mean ({homescreen_a_centre}).")

else:
    stat, test_p = wilcoxon(homescreen_a_ratings, homescreen_b_ratings)
    print(f'Wilcoxon p-value = {test_p}')
    print(f'Wilcoxon stat = {stat}\n')

    # find centres of each group
    homescreen_a_centre = homescreen_a_ratings.mean()
    homescreen_b_centre = homescreen_b_ratings.mean()
    centre_diff = homescreen_a_centre - homescreen_b_centre
    if homescreen_a_centre > homescreen_b_centre:
        print(f"Group A mean ({homescreen_a_centre}) is greater than Group B mean ({homescreen_b_centre}).")
    elif homescreen_a_centre < homescreen_b_centre:
        print(f"Group B mean ({homescreen_b_centre}) is greater than Group A mean ({homescreen_a_centre}).")

if test_p > 0.05:
    print("There is NO significant difference between groups.")
else:
    print("There IS a significant difference between groups.")

print("-----------------------------\n")

print(f"variables with significant differences: {sig_diff}")






# Group B edit dark mode time is normally distributed.
# group B p-value = 0.19578940089452057

# Wilcoxon p-value = 0.40625
# Wilcoxon stat = 19.0

# There is NO significant difference between groups.
# Group B median (15.0) is greater than Group A median (11.0).
# -----------------------------

# Group A edit font time is normally distributed.
# group A p-value = 0.3254417829509001

# Group B edit font time is normally distributed.
# group B p-value = 0.2976463385689727

# T-test p-value = 1.0
# T-test stat = 0.0

# There is NO significant difference between groups.
# Group B median (10.0) is greater than Group A median (9.5).
# -----------------------------

# Group A add recipe time is NOT normally distributed.
# group A p-value = 0.012682154470160408

# Group B add recipe time is NOT normally distributed.
# group B p-value = 0.01863104044352393

# Wilcoxon p-value = 0.365234375
# Wilcoxon stat = 18.0

# There is NO significant difference between groups.
# -----------------------------

# Group A save recipe taps is normally distributed.
# group A p-value = 0.1909907199069698

# Group B save recipe taps is normally distributed.
# group B p-value = 0.379841919237063

# T-test p-value = 0.044568343939717925
# T-test stat = -2.3324447490696727

# There IS a significant difference between groups.
# Group B median (4.5) is greater than Group A median (3.0).
# -----------------------------

# Group A edit dark mode taps is NOT normally distributed.
# group A p-value = 0.004796996174231894

# Group B edit dark mode taps is normally distributed.
# group B p-value = 0.5745052650689695

# Wilcoxon p-value = 0.365234375
# Wilcoxon stat = 18.0

# There is NO significant difference between groups.
# Group B median (5.0) is greater than Group A median (4.0).
# -----------------------------

# Group A edit font taps is normally distributed.
# group A p-value = 0.25755075097087055

# Group B edit font taps is normally distributed.
# group B p-value = 0.15201182891854603

# T-test p-value = 0.1038881310621017
# T-test stat = 1.8090680674665816

# There is NO significant difference between groups.
# Group A median (3.5) is greater than Group B median (3.0).
# -----------------------------

# Group A add recipe taps is NOT normally distributed.
# group A p-value = 0.015408869221726223

# Group B add recipe taps is normally distributed.
# group B p-value = 0.14879821985688607

# Wilcoxon p-value = 0.00390625
# Wilcoxon stat = 0.0

# There IS a significant difference between groups.
# Group B median (5.0) is greater than Group A median (4.0).
# -----------------------------

# homescreen A p-value = 0.014237768761802105
# homescreen A ratings are NOT normally distributed.

# homescreen B p-value = 0.0012971330264874895
# homescreen B ratings are NOT normally distributed.

# Wilcoxon p-value = 0.00024304789855789704
# Wilcoxon stat = 0.0

# Group B mean (0.78) is greater than Group A mean (0.5000000000000001).
# There IS a significant difference between groups.
# -----------------------------


#################################################
#################################################


# variables with significant differences: ['save recipe taps', 'add recipe taps']

# significant differences in "save recipe taps" (group B took more taps) and "add recipe taps" (group B took more taps)
# no significant difference in time taken for tasks between groups

# significant difference in homescreen ratings (group B has higher rating)

# although group B took more taps to add and save recipes, they still rated the homescreen higher than group A
