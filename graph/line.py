import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker
from matplotlib.dates import MonthLocator, DateFormatter  # 修改后的导入语句

# 准备数据
data = {
    'Date': ['2024/7/23', '2024/8/26', '2025/2/12'],
    'Hemoglobin': [91, 97, 101],
    'RBC': [3.18, 3.43, 3.48],
    'WBC': [7.54, 8.33, 7.94],
    'Platelets': [502, 487, 429]
}
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# 创建图表
plt.style.use('default')  # 恢复默认简洁样式
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# 主标题
fig.suptitle('Hematologic Trends',
             fontsize=14, y=1.0)

# 血红蛋白子图
axs[0,0].plot(df['Date'], df['Hemoglobin'], marker='o', color='#ff461f')
axs[0,0].axhline(y=110, color='gray', linestyle='-', linewidth=1)
axs[0,0].set_ylabel('Hemoglobin (g/L)')
axs[0,0].yaxis.set_major_locator(ticker.MultipleLocator(2))  # 修改为以2为间距的刻度

# 红细胞子图
axs[0,1].plot(df['Date'], df['RBC'], marker='o', color='#ff461f')
axs[0,1].axhline(y=3.5, color='gray', linestyle='-', linewidth=1)
axs[0,1].set_ylabel('RBC (×10¹²/L)')

# 白细胞子图
axs[1,0].plot(df['Date'], df['WBC'], marker='o', color='#afdd22')
axs[1,0].axhline(y=10.0, color='gray', linestyle='-', linewidth=1)
axs[1,0].axhline(y=4.0, color='gray', linestyle='-', linewidth=1)
axs[1,0].set_ylabel('WBC (×10⁹/L)')

# 血小板子图
axs[1,1].plot(df['Date'], df['Platelets'], marker='o', color='#cca4e3')
axs[1,1].axhline(y=300, color='gray', linestyle='-', linewidth=1)
axs[1,1].set_ylabel('Platelets (×10⁹/L)')

# 统一调整所有子图
for ax in axs.flat:
    # 设置双数月份显示（2,4,6,8,10,12月）
    ax.xaxis.set_major_locator(MonthLocator(bymonth=(2,4,6,8,10,12), interval=1))
    # 设置日期格式为年月
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
    # 坐标轴标签
    ax.tick_params(axis='both', which='major', labelsize=10)
    # 去除标签旋转设置
    plt.setp(ax.get_xticklabels(), rotation=0, ha='center')  # 修改为不旋转且居中对齐
plt.tight_layout()
plt.savefig('Hematologic_Parameters.png', dpi=300, bbox_inches='tight')
plt.show()