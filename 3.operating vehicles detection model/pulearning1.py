# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:02:23 2020

@author: Jeremy
"""
import time
start_time = time.clock()


import pandas as pd                    # for data handling
import numpy as np                     # for random selections, mainly
import matplotlib.pyplot as plt        # for plotting                
plt.rcParams['figure.figsize'] = 7,7   # graph dimensions
plt.rcParams['font.size'] = 14         # graph font size

#data set
df_chuzuche_feature=pd.read_csv(open(r'C:\Users\Jeremy\Desktop\2019.12.18\20161205_title_chuzuche_yueB_regular_zhibiao.csv'),header=0,index_col='car_id')
df_chuzuche_time_feature=pd.read_csv(open(r'C:\Users\Jeremy\Desktop\2019.12.18\20161205_title_chuzuche_time_yueB_regular_zhibiao.csv'),header=0,index_col='car_id')
df_chuzuche_feature=pd.merge(df_chuzuche_feature,df_chuzuche_time_feature,how='inner',on='car_id')
df_chuzuche_feature=df_chuzuche_feature.dropna()#删除所有有空值的行
#df_chuzuche_feature.reset_index(drop=True,inplace=True)#重置索引
df_shehuiche_feature=pd.read_csv(open(r'C:\Users\Jeremy\Desktop\2019.12.18\20161205_title_shehuiche_yueB_regular_zhibiao.csv'),header=0,index_col='car_id')
df_shehuiche_time_feature=pd.read_csv(open(r'C:\Users\Jeremy\Desktop\2019.12.18\20161205_title_shehuiche_time_yueB_regular_zhibiao.csv'),header=0,index_col='car_id')
df_shehuiche_feature=pd.merge(df_shehuiche_feature,df_shehuiche_time_feature,how='inner',on='car_id')
df_shehuiche_feature=df_shehuiche_feature.dropna()#删除所有有空值的行
#df_shehuiche_feature.reset_index(drop=True,inplace=True)#重置索引
X=pd.concat([df_chuzuche_feature,df_shehuiche_feature])
#X.reset_index(drop=True,inplace=True)#重置索引
y = np.zeros(len(df_chuzuche_feature)+len(df_shehuiche_feature))
y[:len(df_chuzuche_feature)] = 1.0
car_id=list(X.index)#删除只出行一次的车辆，car_id表示出行次数大于1的车辆ID
y = pd.Series(y,index=car_id)
print('%d data points and %d features' % (X.shape))
print('%d positive out of %d total' % (sum(y), len(y)))

y_orig = y.copy()
# Unlabel a certain number of data points
hidden_size = int(len(df_chuzuche_feature)*0.2)
y.loc[
    np.random.choice(
        y[y == 1].index, 
        replace = False, 
        size = hidden_size
    )
] = 0  #从y=1的样本中随机选择2700个，使其标签变为0
# Check the new contents of the set
print('%d positive out of %d total' % (sum(y), len(y)))



#1111111111111111111111
# We'll use a generic random forest
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(
    n_estimators = 1000,  # Use 1000 trees########################################
    n_jobs = -1           # Use all CPU cores
)
rf.fit(X, y)

# Store the scores assigned by this approach
results = pd.DataFrame({
    'truth'      : y_orig,   # The true labels
    'label'      : y,        # The labels to be shown to models in experiment
    'output_std' : rf.predict_proba(X)[:,1]   # The random forest's scores；第i行第j列上的数值是模型预测第i个预测样本为某个标签的概率
}, columns = ['truth', 'label', 'output_std'])
print("1111111111111111111111111111111")


#22222222222222222222
# Use 1000 trees
from sklearn.tree import DecisionTreeClassifier
n_estimators = 1000########################################
estimator = DecisionTreeClassifier()

# Keep track of the indices of positive and unlabeled data points
iP = y[y > 0].index #标记正样本的索引
iU = y[y <= 0].index  #未标记样本的索引

# For each data point, keep track of how many times it has been OOB...
num_oob = pd.DataFrame(np.zeros(shape = y.shape), index = y.index)

# ...and the sum of its OOB scores
sum_oob = pd.DataFrame(np.zeros(shape = y.shape), index = y.index)

for _ in range(n_estimators):
    # Get a bootstrap sample of unlabeled points for this round
    ib = np.random.choice(iU, replace=True, size = len(iP)) #从未标记样本中随机选择索引(按标记样本的数量)

    # Find the OOB data points for this round
    i_oob = list(set(iU) - set(ib))  #未标记样本中未被选择样本的索引

    # Get the training data (ALL positives and the bootstrap 
    # sample of unlabeled points) and build the tree
    Xb = X[y > 0].append(X.loc[ib])
    yb = y[y > 0].append(y.loc[ib])
    estimator.fit(Xb, yb)
    
    # Record the OOB scores from this round
    sum_oob.loc[i_oob, 0] += estimator.predict_proba(X.loc[i_oob])[:,1]
    num_oob.loc[i_oob, 0] += 1

# Finally, store the scores assigned by this approach
results['output_bag'] = sum_oob / num_oob
#print(results)
#print(y)
print("2222222222222222222222222222222222")




#3333333333333333333
from baggingPU import BaggingClassifierPU
bc = BaggingClassifierPU(
    DecisionTreeClassifier(), 
    n_estimators = 1000,  # 1000个树###################################
    max_samples = int(sum(y)), # 在每个袋中平衡标记正样本和未标记样本数量
#    n_jobs = -1           # cpu里的所有core进行工作
)
bc.fit(X, y)
results['output_skb'] = bc.oob_decision_function_[:,1]
print("33333333333333333333333333333333")




#44444444444444444444444444
# Create a new target vector, with 1 for positive, -1 for unlabeled, and 
# 0 for "reliable negative" (there are no reliable negatives to start with)
ys = 2 * y - 1    #ys为新标签，1表示标记正样本，0表示可靠负样本，-1表示未标记样本

# Get the scores from before
pred = rf.predict_proba(X)[:,1]  #使用方法1中的分类器rf，样本为1的概率

# Find the range of scores given to positive data points
range_P = [min(pred * (ys > 0)), max(pred * (ys > 0))]  #range_P为标记正样本的概率范围

# STEP 1
# If any unlabeled point has a score above all known positives, 
# or below all known positives, label it accordingly
iP_new = ys[(ys < 0) & (pred >= range_P[1])].index #未标记样本中概率大于标记正样本的最大概率的索引，赋值1
iN_new = ys[(ys < 0) & (pred <= range_P[0])].index #未标记样本中概率小于标记正样本的最小概率的索引，赋值0
ys.loc[iP_new] = 1
ys.loc[iN_new] = 0

# Classifier to be used for step 2
rf2 = RandomForestClassifier(n_estimators = 1000, n_jobs = -1)#新分类器rf2##############################

# Limit to 10 iterations (this is arbitrary, but 
# otherwise this approach can take a very long time)
for i in range(10):
    # If step 1 didn't find new labels, we're done
    if len(iP_new) + len(iN_new) == 0 and i > 0:
        break
    
    print(
        'Step 1 labeled %d new positives and %d new negatives.' 
        % (len(iP_new), len(iN_new))
    )
    print('Doing step 2... ', end = '')
    
    # STEP 2
    # Retrain on new labels and get new scores
    rf2.fit(X, ys)
    pred = rf2.predict_proba(X)[:,-1] #样本为1的概率
    
    # Find the range of scores given to positive data points
    range_P = [min(pred * (ys > 0)), max(pred * (ys > 0))] #标记正样本为1的概率范围
    
    # Repeat step 1
    iP_new = ys[(ys < 0) & (pred >= range_P[1])].index #未标记样本中概率大于标记正样本的最大概率的索引，赋值1
    iN_new = ys[(ys < 0) & (pred <= range_P[0])].index #未标记样本中概率小于标记正样本的最小概率的索引，赋值0
    ys.loc[iP_new] = 1
    ys.loc[iN_new] = 0
# Lastly, get the scores assigned by this approach    
results['output_stp'] = pred
print("44444444444444444444444444444444444")



#555555555555555555555
# For each data point, calculate the average score from the three approaches
results['output_all'] = results[[
    'output_std', 'output_bag', 'output_stp'
]].mean(axis = 1)#三种方法计算每个样本为1的平均概率。output_std为标准分类，output_bag为bagging分类，output_skb也是bagging分类，output_stp为两步法
print(results)


# Prepare for graphing the performance 
# (i.e. the success in identifying hidden positives)
ts = range(100, hidden_size+100, 100)  #100-2700，步长为100。[100,...,2700]
y_std, y_bag, y_skb, y_stp, y_all = [], [], [], [], []
for t in ts:
    y_std.append(
        results[results.label == 0].sort_values(
            'output_std', ascending = False
        ).head(t).truth.mean()
    )#未标记样本按output_std降序排列，取头部t行，计算'truth'列的均值。即头部t个样本的truth标签为1的比例
    y_bag.append(
        results[results.label == 0].sort_values(
            'output_bag', ascending = False
        ).head(t).truth.mean()
    )#未标记样本按output_bag降序排列，取头部t行，计算'truth'列的均值。即头部t个样本的truth标签为1的比例
    y_skb.append(
        results[results.label == 0].sort_values(
            'output_skb', ascending = False
        ).head(t).truth.mean()
    )#未标记样本按output_skb降序排列，取头部t行，计算'truth'列的均值。即头部t个样本的truth标签为1的比例
    y_stp.append(
        results[results.label == 0].sort_values(
            'output_stp', ascending = False
        ).head(t).truth.mean()
    )#未标记样本按output_stp降序排列，取头部t行，计算'truth'列的均值。即头部t个样本的truth标签为1的比例
    y_all.append(
        results[results.label == 0].sort_values(
            'output_all', ascending = False
        ).head(t).truth.mean()
    )#未标记样本按output_all降序排列，取头部t行，计算'truth'列的均值。即头部t个样本的truth标签为1的比例
    print(t)
    
# Check the difference between PU bagging the 
# long way and using BaggingClassifierPU
[y_bag[i] - y_skb[i] for i in range(len(y_bag))] #计算两种bagging分类方法的差值

# Performance graphing
plt.rcParams['font.size'] = 16
plt.rcParams['figure.figsize'] = 15, 8

plt.plot(  #ts为[100,...,2700]
    ts, y_std,
    ts, y_bag,
    ts, y_stp,
    ts, y_all,
    lw = 3 #折线图的线条宽度
)

vals = plt.gca().get_yticks()  #vals为y轴的刻度位置列表
plt.yticks(vals, ['%.0f%%' % (v*100) for v in vals]) #在y轴原刻度位置vals上修改数值
plt.xlabel('Number of unlabeled data points chosen from the top rated')
plt.ylabel('Percent of chosen that are secretly positive')
plt.legend([
    'Standard classifier', 
    'PU bagging', 
    'Two-step approach', 
    'Average score'
])
#ylim = plt.gca().get_ylim()  #获取y轴的上下限
plt.title('Performance of the three approaches and of their average')
plt.grid()
plt.show()

##########################被定为未标记样本的出租车中识别正确比例
results_chuzuche=results.iloc[:len(df_chuzuche_feature)]
results_chuzuche_0=results_chuzuche[results_chuzuche.label==0]
results.index.name='car_id'
results.to_csv(r'C:\Users\Jeremy\Desktop\2019.12.18\20161205_results_all.csv')

from sklearn.externals import joblib
joblib.dump(rf,r'C:\Users\Jeremy\Desktop\rf_all.pickle')
joblib.dump(estimator,r'C:\Users\Jeremy\Desktop\estimator_all.pickle')
joblib.dump(bc,r'C:\Users\Jeremy\Desktop\bc_all.pickle')
joblib.dump(rf2,r'C:\Users\Jeremy\Desktop\rf2_all.pickle')

stop_time = time.clock()
cost = stop_time - start_time
print("cost %s second" % (cost))