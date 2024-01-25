import pandas as pd
import os
import numpy as np


df_res = pd.DataFrame(columns=['cycle', 'Voltages', 'C_rate', 'D_rate', 'Tem', 'Capacity'])
files = os.listdir('./Dataset_3_NCM_NCA_battery/')
for file in range(len(files)):
    Tem = int(files[file][2:4])
    data_r = pd.read_csv(os.path.join('./Dataset_3_NCM_NCA_battery/', files[file]))
    k = np.min(data_r['cycle number'].values)
    data_k = data_r[data_r['cycle number'] == k]
    Q_p = np.max(np.array(data_k['Q discharge/mA.h']))
    delta = 1
    for i in range(int(np.min(data_r['cycle number'].values)), int(np.max(data_r['cycle number'].values))+1):
        data_i = data_r[data_r['cycle number'] == i]
        Ecell = np.array(data_i['Ecell/V'])
        Q_dis = np.array(data_i['Q discharge/mA.h'])
        Current = np.array(data_i['<I>/mA'])
        control = np.array(data_i['control/V/mA'])
        cr = np.array(data_i['control/mA'])[1] / 2500
        cr_d = int(files[file][8])
        if np.max(Q_dis) < 1650 or np.max(Q_dis) > 2510:
            delta = delta + 1
            continue
        # Remove points where capacity changes too quickly
        if np.abs(np.max(Q_dis) - Q_p) > delta * 10:
            delta = delta + 1
            continue
        delta = 1
        Q_p = np.max(Q_dis)
        index = np.where(np.abs(control) == 0)
        if index[0][0] > 0:
            start = index[0][0]
        else:
            start = index[0][14]
            print(i)
        if control[start + 19] == 0:
            df_res = pd.concat([df_res, pd.DataFrame.from_dict({'cycle': i, 'Voltages': Ecell[start:start + 59], 'C_rate': cr, 'D_rate': cr_d, 'Tem': Tem,
                                    'Capacity': np.max(Q_dis)})], ignore_index=True)
# Save to excel file
df_res.to_excel('Dataset_3_NCM_NCA_battery.xlsx', index=False)
# Or save to csv file
# df_res.to_csv('Dataset_3_NCM_NCA_battery.csv', index=False)
print('Features extraction is done')
