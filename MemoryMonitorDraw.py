'''
Created on 2020-10-19
@author: dandan.yao
'''
import os,sys,json
import time, base64,requests
import configparser
import psutil
import queue
import _thread,threading
import datetime
import matplotlib.pyplot as plt
from matplotlib import pylab
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.axisartist import HostAxes, ParasiteAxes

global path
def load_Sys(path,filename):
    inFile = open(path, 'r')  # 以只读方式打开某fileName文件

    # 定义空list，用来存放文件中的数据
    X = []
    y1 =[]
    y2 =[]

    line_num=0
    for line in inFile:
        if(line_num>0):
            trainingSet = line.split()  # 对于每一行，按空格把数据分开，这里是分成两部分
            X.append(trainingSet[0])  # 第一部分，即文件中的第一列数据(Time)逐一添加到list X 中
            y1.append(trainingSet[1])  # 第二部分，即文件中的第二列数据(CPU%)逐一添加到list y1 中
            y2.append(trainingSet[2])  # 第三部分，即文件中的第三列数据(Memory%)逐一添加到list y2 中

        line_num+=1
    #plt.figure()
    Xtime = pylab.datestr2num(X)
    fig = plt.figure(figsize=(15, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylabel('CPU/Mem Usage(%)')
    ax.set_xlabel('time')
    y_major_locator = MultipleLocator(10)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylim(0, 100)
    ax.plot_date(Xtime, list(map(float, y1)), 'b-', label='CPU_Usage(%)')
    ax.plot_date(Xtime, list(map(float, y2)), 'r', label='Pysical_Mem(%)')
    plt.legend()
    #print(filename[:-4])
    plt.savefig(logpath+os.sep +'%s.png' % filename[:-4])
    #plt.show()


def load_Process(path,filename):
    inFile = open(path, 'r')  # 以只读方式打开某fileName文件

    # 定义空list，用来存放文件中的数据
    X = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []

    line_num=0
    for line in inFile:
        if(line_num>0):
            trainingSet = line.split()  # 对于每一行，按空格把数据分开，这里是分成两部分
            X.append(trainingSet[0])  # 第一部分，即文件中的第一列数据(Time)逐一添加到list X 中
            y1.append(trainingSet[1])  # 第二部分，即文件中的第二列数据(CPU%)逐一添加到list y1 中
            y2.append(trainingSet[2])  # 第三部分，即文件中的第三列数据(Memory%)逐一添加到list y2 中
            y3.append(trainingSet[3])  # 第二部分，即文件中的第二列数据(Mem_Size)逐一添加到list y3 中
            y4.append(trainingSet[4])  # 第三部分，即文件中的第三列数据(VM_Size)逐一添加到list y4 中
        line_num+=1

    fig = plt.figure(figsize=(15, 5))  # 定义图像的大小（以英寸为单位，1英寸=2.53厘米）
    time = pylab.datestr2num(X)
    # 设置日期显示范围
    ax_cof = HostAxes(fig, [0.15, 0.1, 0.65, 0.8])  # 用[left, bottom, weight, height]的方式定义axes，0 <= l,b,w,h <= 1
    # 创建主轴用HostAxes(figure,[ 左，下，宽，高 ]） 然后寄生出独立的y轴来，并共享x轴。独立的y轴对应独立的曲线 将寄生轴加入主轴的列表

    # parasite addtional axes, share x
    ax_CPU = ParasiteAxes(ax_cof, sharex=ax_cof)
    ax_Mem = ParasiteAxes(ax_cof, sharex=ax_cof)
    ax_Vitual = ParasiteAxes(ax_cof, sharex=ax_cof)

    # append axes
    ax_cof.parasites.append(ax_CPU)
    ax_cof.parasites.append(ax_Mem)
    ax_cof.parasites.append(ax_Vitual)

    # invisible right axis of ax_cof
    ax_cof.axis['right'].set_visible(False)
    ax_cof.axis['top'].set_visible(False)
    ax_Mem.axis['right'].set_visible(True)
    ax_Mem.axis['right'].major_ticklabels.set_visible(True)
    ax_Mem.axis['right'].label.set_visible(True)

    ax_Vitual.axis['right'].set_visible(False)
    ax_Vitual.axis['right'].major_ticklabels.set_visible(False)
    ax_Vitual.axis['right'].label.set_visible(False)

    # set label for axis
    ax_cof.set_ylabel('CPU/Mem Usage(%)')
    ax_cof.set_xlabel('time')
    ax_Mem.set_ylabel('Mem_Size(K)')
    ax_Vitual.set_ylabel('VM_Size(K)')

    load_axisline = ax_Mem.get_grid_helper().new_fixed_axis

    ax_Vitual.axis['right2'] = load_axisline(loc='right', axes=ax_Vitual, offset=(80, 0))

    fig.add_axes(ax_cof)

    ax_cof.set_ylim(0, 100)

    ax_cof.plot_date(time, list(map(float, y1)), 'b-', label="CPU Usage(%)")
    ax_cof.plot_date(time, list(map(float, y2)), 'r', label="Mem Usage(%)")
    ax_Mem.plot_date(time, list(map(float, y3)), 'k', label="MemSize(K)")
    ax_Vitual.plot_date(time, list(map(float, y4)), 'm', label="VM_Size(K)")


    ax_cof.legend(loc='upper right')

    # 轴名称，刻度值的颜色
    ax_Mem.axis['right'].label.set_color('black')
    ax_Vitual.axis['right2'].label.set_color('purple')

    ax_Mem.axis['right'].major_ticks.set_color('black')
    ax_Vitual.axis['right2'].major_ticks.set_color('purple')

    ax_Mem.axis['right'].major_ticklabels.set_color('black')
    ax_Vitual.axis['right2'].major_ticklabels.set_color('purple')

    ax_Mem.axis['right'].line.set_color('black')
    ax_Vitual.axis['right2'].line.set_color('purple')

    #TitleName = _all_software_name + '-' + ProcessName[:ProcessName.rfind(".")] + ProcessName[ProcessName.rfind(
    #    "-"):] + '_CMV'  # 将文件夹名字处理一下，添加软件名称，并去掉后面的.exe和进程ID
    #print(filename[:-4])
    plt.savefig(logpath+os.sep +'%s.png' % filename[:-4])
    #plt.show()  # 让绘制的图像在屏幕上



if __name__ == '__main__':

    # get config
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    elif __file__:
        path = os.path.dirname(os.path.abspath(__file__))

    #path = os.getcwd()
    configPath = os.path.join(path, "Config.ini")
    config = configparser.ConfigParser()
    config.read_file(open(configPath))
    logpath = config.get("Config", "path")

    filelist = os.listdir(logpath)
    for filename in filelist:
        de_path = os.path.join(logpath, filename)
        #if os.path.isfile(de_path):
        if de_path.endswith(".txt"): #Specify to find the txt file.
            if "System" in filename:
                load_Sys(de_path,filename)
            else:
                load_Process(de_path,filename)

