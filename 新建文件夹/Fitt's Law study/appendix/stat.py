import os
import csv
import math
import matplotlib.pyplot as plt
import pingouin as pg
import pandas as pd

mou_dir = os.path.join('original data', 'mouse')
mob_dir = os.path.join('original data', 'mobile')

def calculate(dir, name="", device=""):
    all_x, all_y = [], []
    all_others = []
    all_corr, all_fals = 0, 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            f = open(os.path.join(dir, file), 'r')
            reader = csv.reader(f)
            row_header = next(reader)
            corr, fals = 0, 0
            x, y = [], []
            others = [] # name, device, width, distance
            for kind in range(9):
                local_corr, d_s, cost = 0, 0, 0
                name, width, distance = '', '', ''
                for trial in range(19):
                    if trial == 0:
                        row = next(reader)
                        name = row[0]
                        d_s = float(row[3]) / float(row[2])
                        distance = row[3]
                        width = row[2]
                    else:
                        row = next(reader)
                        if row[6] == 'true' or row[6] == 'TRUE':
                            local_corr += 1
                            corr += 1
                            cost += float(row[5])
                        if row[6] == 'false' or row[6] == 'FALSE':
                            fals += 1
                x.append(math.log(d_s, 2))
                y.append(cost / local_corr)
                others.append([name, device, width, distance])
                print("D/S: %f, log2(D/S+1): %f, time: %f" %(d_s, math.log(d_s, 2), cost / local_corr))
            all_x.append(x)
            all_y.append(y)
            all_others.append(others)
            all_corr += corr
            all_fals += fals
            # print("T: %d, F: %d" %(corr, fals))
            f.close()

    return all_x, all_y, all_others, [all_corr, all_fals]

def init_vali():
    name = "lmq"
    print("### Mouse")
    x, y1, _, _ = calculate(mou_dir, name, "mouse")
    print("### Mobile")
    _, y2, _, _ = calculate(mob_dir, name, "mobile")
    x = x[0]
    y1 = y1[0]
    y2 = y2[0]

    plt.scatter(x, y1, marker='o', label='mouse')
    plt.scatter(x, y2, marker='*', label='mobile')
    plt.legend()
    plt.show()

def data_pro():
    _, mou_time, mou_others, mou_corr = calculate(mou_dir, device="mouse")
    _, mob_time, mob_others, mob_corr = calculate(mob_dir, device="mobile")
    def data_write(time, others):
        file_data = os.path.join('', 'data.csv')
        if not os.path.exists(file_data):
            with open(file_data, 'a', newline="") as f:
                csv_writter = csv.writer(f)
                csv_writter.writerow(['Name', 'Device', 'Width(cm)', 'Distance(cm)', 'Time(ms)'])# Name	Device	Width(cm)	Distance(cm)	Time(ms)
        with open(file_data, 'a', newline="") as f:
            csv_writter = csv.writer(f)
            for (t, o) in zip(time, others):
                for i in range(9):
                    csv_writter.writerow([o[i][0], o[i][1], o[i][2], o[i][3], t[i]])
                    
    # data_write(mou_time, mou_others)
    # data_write(mob_time, mob_others)

    print("### Mouse:  T: %d; F: %d; err_rate: %f" %(mou_corr[0], mou_corr[1], mou_corr[1] / (mou_corr[1] + mou_corr[0])))
    print("### Mobile:  T: %d; F: %d; err_rate: %f" %(mob_corr[0], mob_corr[1], mob_corr[1] / (mob_corr[1] + mob_corr[0])))
    
def anova():
    Fpath = './data.csv'
    df = pd.read_csv(Fpath)
    data = df.dropna()
    # Distance
    print('DISTANCE')
    aov1 = pg.anova(dv='Time(ms)', between="Distance(cm)", data=df, detailed=True)
    print(aov1)

    # Width
    print('WIDTH')
    aov2 = pg.anova(dv='Time(ms)', between="Width(cm)", data=df, detailed=True)
    print(aov2)

    # Device
    print('DEVICE')
    aov3 = pg.anova(dv='Time(ms)', between="Device", data=df, detailed=True)
    print(aov3)

if __name__ == "__main__":
    # 初步验证
    init_vali()
    # 数据整理，整理后为 data.csv
    # data_pro()
    # 方差分析，直接输出结果
    anova()