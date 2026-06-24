# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 13:27:11 2026

@author: USER
"""

import numpy as np
import matplotlib.pyplot as plt

materials = ["EN AC 48000 T6", "2618 T61", "4032 T6"]

criteria = [
    "Peak Temp (°C)",
    "Peak Stress (MPa)",
    "Max Deformation (mm)",
    "Min Yield SF",
    "Min Fatigue SF",]

directions = [-1, -1, -1, +1, +1]

X = np.array([
    # Temp    Stress   Deform    YieldSF  FatigueSF
    [196.95,  159.96,  0.15330,  1.3504,  1.5729],   # EN AC 48000 T6
    [190.12,  166.93,  0.16123,  1.8152,  2.1091],   # 2618 
    [191.34,  173.02,  0.14887,  1.4912,  1.8743],   # 4032
])

weights = np.ones(len(criteria)) / len(criteria)

# TOPSIS

norms = np.sqrt((X ** 2).sum(axis=0))
R = X / norms                              

V = R * weights

A_plus  = np.where(np.array(directions) == +1, V.max(axis=0), V.min(axis=0))
A_minus = np.where(np.array(directions) == +1, V.min(axis=0), V.max(axis=0))

# Euclidean distances
D_plus  = np.sqrt(((V - A_plus)  ** 2).sum(axis=1))
D_minus = np.sqrt(((V - A_minus) ** 2).sum(axis=1))

# Closeness coefficient
CC = D_minus / (D_plus + D_minus)

ranks = len(CC) - CC.argsort().argsort()   # sorting the ranks


print("\n" + "="*60)
print("  TOPSIS RESULTS — Aluminium Piston Alloy Selection")
print("="*60)

print(f"\n{'Material':<15} {'D+':<10} {'D-':<10} {'CC Score':<12} {'Rank'}")
print("-"*55)
for i, mat in enumerate(materials):
    print(f"{mat:<15} {D_plus[i]:<10.5f} {D_minus[i]:<10.5f} "
          f"{CC[i]:<12.5f} {int(ranks[i])}")

print("\nFinal Ranking:")
order = np.argsort(-CC)
for pos, idx in enumerate(order):
    print(f"  Rank {pos+1}: {materials[idx]}  (CC = {CC[idx]:.4f})")

print("\nNote: AC8A as-cast excluded — yield SF = 0.96 < 1.0 (yield failure)")
print("="*60)



print("\nNormalised Decision Matrix (R):")
header = f"{'Criterion':<25}" + "".join(f"{m:<14}" for m in materials)
print(header)
print("-" * (25 + 14*len(materials)))
for j, crit in enumerate(criteria):
    row = f"{crit:<25}" + "".join(f"{R[i,j]:<14.5f}" for i in range(len(materials)))
    print(row)

# PLOT

fig, ax = plt.subplots(figsize=(7, 5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Sorted by CC score 
order      = np.argsort(-CC)
mat_sorted = [materials[i] for i in order]
cc_sorted  = CC[order]
rank_sorted= [int(ranks[i]) for i in order]

bar_colors = ['#2c7bb6', '#abd9e9', '#d7191c']   # blue shades + red for last
bars = ax.bar(mat_sorted, cc_sorted,
              color=bar_colors, edgecolor='black',
              linewidth=0.7, width=0.5)

# showing the ranks at the bottom of the bar of the bar graph
for bar, score, rank in zip(bars, cc_sorted, rank_sorted):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.015,
            f'CC = {score:.3f}',
            ha='center', va='bottom',
            fontsize=10, fontweight='bold', color='black')
    ax.text(bar.get_x() + bar.get_width() / 2,
            0.02,
            f'Rank {rank}',
            ha='center', va='bottom',
            fontsize=9, color='white', fontweight='bold')

ax.set_ylabel('TOPSIS Closeness Coefficient (CC)', fontsize=11, color='black')
ax.set_xlabel('Alloy', fontsize=11, color='black')
ax.set_ylim(0, 1.05)
ax.tick_params(colors='black', labelsize=10)
for spine in ax.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(0.8)
ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='grey')
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig('topsis_results.png', dpi=600, bbox_inches='tight',
            facecolor='white')
plt.show()
