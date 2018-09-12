import numpy as np
import matplotlib.pyplot as plt

n_groups = 5

means_men = (20, 35, 30, 35, 27)
means_women = (25, 32, 34, 20, 25)

fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
print(index)
rects1 = plt.bar(index, means_men, bar_width,alpha=1, color='g',label= 'Men')

rects2 = plt.bar(index + bar_width, means_women, bar_width,alpha=1,color='y',label='Women')

plt.xlabel('Group')
plt.ylabel('Scores')
plt.title('Scores by group and gender')
#设置x轴的标称，输入有位置和名字
plt.xticks(index + (bar_width/2), ('A', 'B', 'C', 'D', 'E'))
#y轴的范围
plt.ylim(0,40)

#图例，就是柱状图的名称
plt.legend()
#自动调整图像外部边缘
plt.tight_layout()
plt.show()