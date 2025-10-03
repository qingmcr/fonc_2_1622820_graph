import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Rectangle, FancyBboxPatch

# 创建画布
plt.figure(figsize=(16, 12), dpi=300)
ax = plt.gca()
ax.set_facecolor('#f8f9fa')

# 自定义颜色
colors = {
    'SF3B1': '#e74c3c',  # 红宝石色
    'ASXL1': '#3498db',  # 蓝色
    'JAK2': '#2ecc71',  # 翠绿色
    'CBL': '#9b59b6',  # 紫色
    'mitochondria': '#f39c12',  # 橙色
    'erythroid': '#e74c3c',  # 红色系
    'megakaryocyte': '#2ecc71',  # 绿色系
    'clinical': '#34495e',  # 深灰色
    'Splicing': '#e74c3c',  # 修复KeyError
    'PRC2': '#3498db',  # 修复KeyError
    'JH2': '#2ecc71',  # 修复KeyError
    'TKB': '#9b59b6'  # 修复KeyError
}

# 创建节点位置
node_positions = {
    # 突变基因
    'SF3B1': (2, 8),
    'ASXL1': (5, 8),
    'JAK2': (8, 8),
    'CBL': (11, 8),

    # SF3B1通路
    'Splicing Defects': (1.5, 6.5),
    'ABCB7 ↓': (1, 5),
    'ALAS2 ↓': (2, 5),
    'Mitochondrial Iron': (1.5, 4),
    'GATA1/KLF1 ↓': (1.5, 3),

    # ASXL1通路
    'PRC2 Disruption': (5, 6.5),
    'H3K27me3 Loss': (5, 5),

    # JAK2通路
    'JH2 Destabilization': (8, 6.5),
    'p-STAT5 ↑': (7.5, 5.5),
    'Partial Kinase': (8.5, 5),

    # CBL通路
    'TKB Domain Mut': (11, 6.5),
    'RAS/MAPK ↑': (10.5, 5.5),
    'JAK2 Ubiquitination': (11.5, 5),

    # 交叉作用
    'Epigenetic Repression': (3.5, 4.5),
    'Signaling Crosstalk': (9.5, 4.5),

    # 临床表型
    'Anemia': (3, 1),
    'Thrombocytosis': (9, 1),
    'Platelet Decline': (11, 1)
}

# 创建连接关系
edges = [
    # SF3B1通路
    ('SF3B1', 'Splicing Defects', {'color': colors['SF3B1'], 'width': 3}),
    ('Splicing Defects', 'ABCB7 ↓', {'color': colors['SF3B1'], 'width': 3}),
    ('Splicing Defects', 'ALAS2 ↓', {'color': colors['SF3B1'], 'width': 3}),
    ('ABCB7 ↓', 'Mitochondrial Iron', {'color': colors['mitochondria'], 'width': 3, 'style': 'dashed'}),
    ('ALAS2 ↓', 'Mitochondrial Iron', {'color': colors['mitochondria'], 'width': 3, 'style': 'dashed'}),
    ('Mitochondrial Iron', 'GATA1/KLF1 ↓', {'color': colors['erythroid'], 'width': 3}),
    ('GATA1/KLF1 ↓', 'Anemia', {'color': colors['clinical'], 'width': 3}),

    # ASXL1通路
    ('ASXL1', 'PRC2 Disruption', {'color': colors['ASXL1'], 'width': 3}),
    ('PRC2 Disruption', 'H3K27me3 Loss', {'color': colors['ASXL1'], 'width': 3}),
    ('H3K27me3 Loss', 'Epigenetic Repression', {'color': colors['ASXL1'], 'width': 3}),
    ('Epigenetic Repression', 'GATA1/KLF1 ↓', {'color': colors['erythroid'], 'width': 3, 'style': 'dashed'}),
    ('Epigenetic Repression', 'Anemia', {'color': colors['clinical'], 'width': 2}),

    # JAK2通路
    ('JAK2', 'JH2 Destabilization', {'color': colors['JAK2'], 'width': 3}),
    ('JH2 Destabilization', 'p-STAT5 ↑', {'color': colors['JAK2'], 'width': 3}),
    ('JH2 Destabilization', 'Partial Kinase', {'color': colors['JAK2'], 'width': 3}),
    ('p-STAT5 ↑', 'Signaling Crosstalk', {'color': colors['JAK2'], 'width': 3}),
    ('Partial Kinase', 'Signaling Crosstalk', {'color': colors['JAK2'], 'width': 3}),
    ('Signaling Crosstalk', 'Thrombocytosis', {'color': colors['megakaryocyte'], 'width': 3}),

    # CBL通路
    ('CBL', 'TKB Domain Mut', {'color': colors['CBL'], 'width': 3}),
    ('TKB Domain Mut', 'RAS/MAPK ↑', {'color': colors['CBL'], 'width': 3}),
    ('TKB Domain Mut', 'JAK2 Ubiquitination', {'color': colors['CBL'], 'width': 3}),
    ('RAS/MAPK ↑', 'Signaling Crosstalk', {'color': colors['CBL'], 'width': 3}),
    ('JAK2 Ubiquitination', 'Signaling Crosstalk', {'color': colors['CBL'], 'width': 3, 'style': 'dashed'}),
    ('Signaling Crosstalk', 'Platelet Decline', {'color': colors['clinical'], 'width': 3, 'style': 'dashed'}),

    # 交叉作用
    ('SF3B1', 'Epigenetic Repression', {'color': colors['SF3B1'], 'width': 2, 'style': 'dotted'}),
    ('ASXL1', 'Mitochondrial Iron', {'color': colors['ASXL1'], 'width': 2, 'style': 'dotted'}),
    ('JAK2', 'JAK2 Ubiquitination', {'color': '#95a5a6', 'width': 2, 'style': 'dotted'}),
]

# 绘制连接线
for edge in edges:
    start, end, attr = edge
    style = attr.get('style', 'solid')
    ax.annotate("",
                xy=node_positions[end],
                xycoords='data',
                xytext=node_positions[start],
                textcoords='data',
                arrowprops=dict(
                    arrowstyle="->",
                    color=attr['color'],
                    linewidth=attr['width'],
                    linestyle=style,
                    alpha=0.8,
                    shrinkA=15,
                    shrinkB=15,
                    connectionstyle="arc3,rad=0.1"
                ))

# 绘制节点
for node, pos in node_positions.items():
    # 突变基因 - 矩形
    if node in ['SF3B1', 'ASXL1', 'JAK2', 'CBL']:
        color = colors[node]
        rect = Rectangle((pos[0] - 1.2, pos[1] - 0.5), 2.4, 1.0,
                         facecolor=color, edgecolor='#2c3e50', linewidth=2, alpha=0.9, zorder=10)
        ax.add_patch(rect)
        plt.text(pos[0], pos[1], node,
                 ha='center', va='center',
                 fontsize=14, fontweight='bold', color='white')

        # 添加VAF标签
        vafs = {'SF3B1': '40.5%', 'ASXL1': '19.8%', 'JAK2': '17.5%', 'CBL': '16.2%'}
        plt.text(pos[0], pos[1] - 0.7, f"VAF: {vafs[node]}",
                 ha='center', va='top',
                 fontsize=10, color='#2c3e50', fontstyle='italic')

    # 通路节点 - 椭圆形
    elif node in ['Splicing Defects', 'PRC2 Disruption', 'JH2 Destabilization', 'TKB Domain Mut']:
        # 修复KeyError：使用字典get方法并提供默认值
        edge_color = colors.get(node.split()[0], '#7f8c8d')
        ellipse = Ellipse(pos, 3.0, 1.0,
                          facecolor='white', edgecolor=edge_color,
                          linewidth=2, alpha=0.9, zorder=9)
        ax.add_patch(ellipse)
        plt.text(pos[0], pos[1], node,
                 ha='center', va='center',
                 fontsize=11, fontweight='bold', color=edge_color)

    # 下调节点 - 带向下箭头
    elif '↓' in node:
        plt.text(pos[0], pos[1], node,
                 ha='center', va='center',
                 fontsize=12, fontweight='bold', color=colors['erythroid'])
        plt.plot(pos[0], pos[1] - 0.2, 'v',
                 color=colors['erythroid'], markersize=12)

    # 上调节点 - 带向上箭头
    elif '↑' in node:
        plt.text(pos[0], pos[1], node,
                 ha='center', va='center',
                 fontsize=12, fontweight='bold', color=colors['JAK2'])
        plt.plot(pos[0], pos[1] + 0.2, '^',
                 color=colors['JAK2'], markersize=12)

    # 临床表型 - 圆角矩形
    elif node in ['Anemia', 'Thrombocytosis', 'Platelet Decline']:
        box = FancyBboxPatch((pos[0] - 1.5, pos[1] - 0.4), 3.0, 0.8,
                             boxstyle="round,pad=0.2",
                             facecolor=colors['clinical'],
                             edgecolor='#2c3e50',
                             linewidth=1.5,
                             alpha=0.8)
        ax.add_patch(box)
        plt.text(pos[0], pos[1], node,
                 ha='center', va='center',
                 fontsize=12, fontweight='bold', color='white')

        # 添加临床指标
        if node == 'Anemia':
            plt.text(pos[0], pos[1] - 0.25, "Hb: 91→101 g/L",
                     ha='center', va='top',
                     fontsize=9, color='#ecf0f1')
        elif node == 'Thrombocytosis':
            plt.text(pos[0], pos[1] - 0.25, "Platelets: 502→429×10⁹/L",
                     ha='center', va='top',
                     fontsize=9, color='#ecf0f1')

    # 其他节点
    else:
        # 修复KeyError：使用字典get方法并提供默认值
        color = colors.get(node.split()[0], '#7f8c8d')
        plt.scatter(pos[0], pos[1], s=800,
                    color='white', edgecolor=color,
                    linewidth=2, alpha=0.9, zorder=8)
        plt.text(pos[0], pos[1], node,
                 ha='center', va='center',
                 fontsize=10, fontweight='bold', color=color)

# 添加标题和注释
plt.title('Molecular Crosstalk in MDS/MPN-SF3B1-T with SF3B1/ASXL1/JAK2/CBL Quadruple Mutation',
          fontsize=16, pad=20, fontweight='bold', color='#2c3e50')

plt.text(2, 9.5, "SF3B1 p.K700E: Splicing Dysregulation",
         ha='center', fontsize=12, fontweight='bold', color=colors['SF3B1'])
plt.text(5, 9.5, "ASXL1 p.G646Wfs*12: Epigenetic Deregulation",
         ha='center', fontsize=12, fontweight='bold', color=colors['ASXL1'])
plt.text(8, 9.5, "JAK2 p.R683G: Partial Kinase Activation",
         ha='center', fontsize=12, fontweight='bold', color=colors['JAK2'])
plt.text(11, 9.5, "CBL p.R149Q: RTK Signaling Dysfunction",
         ha='center', fontsize=12, fontweight='bold', color=colors['CBL'])

# 添加图例
legend_elements = [
    plt.Line2D([0], [0], color=colors['SF3B1'], lw=3, label='SF3B1 Pathway'),
    plt.Line2D([0], [0], color=colors['ASXL1'], lw=3, label='ASXL1 Pathway'),
    plt.Line2D([0], [0], color=colors['JAK2'], lw=3, label='JAK2 Pathway'),
    plt.Line2D([0], [0], color=colors['CBL'], lw=3, label='CBL Pathway'),
    plt.Line2D([0], [0], color='gray', lw=2, linestyle='dashed', label='Inhibitory Effect'),
    plt.Line2D([0], [0], color='gray', lw=2, linestyle='dotted', label='Synergistic Interaction')
]
plt.legend(handles=legend_elements, loc='lower center',
           bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=11)

# 添加关键发现文本框
key_findings = [
    "• Dominant SF3B1 clone (VAF 40.5%) mitigates ASXL1 leukemogenicity",
    "• JAK2 p.R683G partial kinase activation (1.8× STAT5 phosphorylation)",
    "• CBL p.R149Q enables self-limiting thrombocytosis",
    "• Mutation synergy fosters hematologic stability without therapy"
]
plt.text(13, 6, "Key Findings:", fontsize=12, fontweight='bold', color='#2c3e50')
for i, finding in enumerate(key_findings):
    plt.text(13, 5 - i * 0.8, finding, fontsize=10, color='#34495e')

# 设置坐标轴范围
plt.xlim(-1, 15)
plt.ylim(0, 10)
plt.axis('off')

# 添加背景色带
ax.add_patch(Rectangle((-1, 7), 16, 3, color='#e8f4f8', alpha=0.3, zorder=0))
ax.add_patch(Rectangle((-1, 2), 16, 5, color='#f1f8e9', alpha=0.3, zorder=0))
ax.add_patch(Rectangle((-1, 0), 16, 2, color='#f9ebeb', alpha=0.3, zorder=0))

plt.tight_layout()

# 保存为PDF矢量图（Adobe Illustrator可编辑）
plt.savefig('MDS_MPN_molecular_pathways.pdf', format='pdf', bbox_inches='tight', dpi=300)
plt.show()