import pandas as pd
import numpy as np
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams["figure.dpi"] = 140

def get_gua_base(three_yao):
    if three_yao == [1,1,1]: #"天"
        idx = 1
    elif three_yao == [1,1,0]: #"澤"
        idx = 2
    elif three_yao == [1,0,1]: #"火"
        idx = 3
    elif three_yao == [1,0,0]: #"雷"
        idx = 4
    elif three_yao == [0,1,1]: #"風"
        idx = 5
    elif three_yao == [0,1,0]: #"水"
        idx = 6
    elif three_yao == [0,0,1]: #"山"
        idx = 7
    elif three_yao == [0,0,0]: #"地"
        idx = 8
    return idx

def is_power (x, y):
    if (x == 1):
        return (y == 1)
    pow = 1
    while (pow < y):
        pow = pow * x
    return (pow == y)


# Init
gua = []
for i in range(1,9):
    for j in range(1,9):
        gua.append(f'上{i}下{j}')

combi = []
for i in range(1,7):
    for j in range(1,7):
        if i == j:
            continue
        combi.append(f'主{i}參{j}')
cols = ['卦辭為主','卦辭為參','主1','主2','主3','主4','主5','主6']
cols.extend(combi)


# Start Simulation
total_steps = 2**20+1
df_gua = pd.DataFrame(np.zeros([len(gua),len(cols)]),index=gua,columns=cols)
for step in range(total_steps):
    toss = np.random.randint(2, size=[6,3])

    toss_tr = toss + 2
    toss_tr_sum = toss_tr.sum(axis=1)
    toss_binary = toss_tr_sum % 2
    toss_down,toss_up = list(toss_binary[:3]),list(toss_binary[3:])
    idx_down, idx_up = get_gua_base(toss_down), get_gua_base(toss_up)
    gua_ti = f'上{idx_up}下{idx_down}'


    if (9 in toss_tr_sum) or (6 in toss_tr_sum):
        count_bian = np.count_nonzero(toss_tr_sum == 6) + np.count_nonzero(toss_tr_sum == 9)
        if count_bian == 1:
            #print('一變')
            bian1 = np.where((toss_tr_sum==9)|(toss_tr_sum==6))[0][0]
            res = f'主{bian1+1}'
            df_gua.loc[gua_ti,res] += 1
        elif count_bian == 2:
            #print('二變')
            bian1, bian2 = np.where((toss_tr_sum==9)|(toss_tr_sum==6))[0]
            res = f'主{bian2+1}參{bian1+1}'
            df_gua.loc[gua_ti,res] += 1
        elif count_bian == 3:
            #print('三變')
            bian1, bian2, bian3 = np.where((toss_tr_sum==9)|(toss_tr_sum==6))[0]
            toss_binary_bian = toss_binary.copy()
            toss_binary_bian[np.where((toss_tr_sum==9)|(toss_tr_sum==6))[0]] = np.abs(toss_binary[np.where((toss_tr_sum==9)|(toss_tr_sum==6))[0]]-1)
            toss_down,toss_up = list(toss_binary_bian[:3]),list(toss_binary_bian[3:])
            idx_down, idx_up = get_gua_base(toss_down), get_gua_base(toss_up)
            gua_ti_bian = f'上{idx_up}下{idx_down}'
            df_gua.loc[gua_ti_bian,'卦辭為主'] += 1
            df_gua.loc[gua_ti,'卦辭為參'] += 1
        elif count_bian == 4:
            #print('四變')
            no_bian1, no_bian2 = np.where((toss_tr_sum!=9)&(toss_tr_sum!=6))[0]
            toss_binary_bian = toss_binary.copy()
            toss_binary_bian[np.where((toss_tr_sum==9)|(toss_tr_sum==6))[0]] = np.abs(toss_binary[np.where((toss_tr_sum==9)|(toss_tr_sum==6))[0]]-1)
            toss_down,toss_up = list(toss_binary_bian[:3]),list(toss_binary_bian[3:])
            idx_down, idx_up = get_gua_base(toss_down), get_gua_base(toss_up)
            gua_ti_bian = f'上{idx_up}下{idx_down}'
            res = f'主{no_bian1+1}參{no_bian2+1}'
            df_gua.loc[gua_ti_bian,res] += 1
        elif count_bian == 5:
            #print('五變')
            no_bian1 = np.where((toss_tr_sum!=9)&(toss_tr_sum!=6))[0][0]
            toss_binary_bian = toss_binary.copy()
            toss_binary_bian[np.where((toss_tr_sum==9)|(toss_tr_sum==6))[0]] = np.abs(toss_binary[np.where((toss_tr_sum==9)|(toss_tr_sum==6))[0]]-1)
            toss_down,toss_up = list(toss_binary_bian[:3]),list(toss_binary_bian[3:])
            idx_down, idx_up = get_gua_base(toss_down), get_gua_base(toss_up)
            gua_ti_bian = f'上{idx_up}下{idx_down}'
            res = f'主{no_bian1+1}'
            df_gua.loc[gua_ti_bian,res] += 1
        elif count_bian == 6:
            #print('六變')
            if len(np.unique(toss)) == 1: # 乾坤二卦時
                df_gua.loc[gua_ti,'主6'] += 1
            else: # 其餘六十二卦
                toss_binary_bian = toss_binary.copy()
                toss_binary_bian[np.where((toss_tr_sum==9)|(toss_tr_sum==6))[0]] = np.abs(toss_binary[np.where((toss_tr_sum==9)|(toss_tr_sum==6))[0]]-1)
                toss_down,toss_up = list(toss_binary_bian[:3]),list(toss_binary_bian[3:])
                idx_down, idx_up = get_gua_base(toss_down), get_gua_base(toss_up)
                gua_ti_bian = f'上{idx_up}下{idx_down}'
                df_gua.loc[gua_ti_bian,'卦辭為主'] += 1
    else:
        #print('不變')
        df_gua.loc[gua_ti,'卦辭為主'] += 1
    
    if is_power(2, step):
        sp_gua = df_gua.copy()
        sp_gua /= step

        fig, ax = plt.subplots(figsize=(12,4))
        fig.tight_layout()

        plt.ylabel('機率')
        plt.title(f'金錢卦-模擬次數:{step}')
        sp_gua.sum().plot.bar(ax=ax)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        plt.grid()
        plt.savefig(f'金錢卦-BAR({step:09d}).png')
    
        fig, ax = plt.subplots(figsize=(12,12)) 
        sns.heatmap(sp_gua, ax=ax)
        plt.title(f'金錢卦-模擬次數:{step}')
        plt.savefig(f'金錢卦-HEATMAP({step:09d}).png')
        
df_gua /= total_steps
df_gua = pd.DataFrame(np.zeros([len(gua),len(cols)]),index=gua,columns=cols)