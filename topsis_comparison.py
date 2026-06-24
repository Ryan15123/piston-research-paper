# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 13:28:00 2026

@author: USER
"""

import numpy as np
import matplotlib.pyplot as plt

materials_sorted = ["2618 T61", "4032 T6", "EN AC 48000 T6"]
cc_equal   = np.array([0.8219, 0.4442, 0.1838])
cc_entropy = np.array([0.9844, 0.4222, 0.0157])
ranks      = [1, 2, 3]
#entropy cc values were obtained by applying shannon entropy weights formulas instead of equal weights to the topsis code

x = np.arange(len(materials_sorted))
width = 0.35

fig, ax = plt.subplots(figsize=(7, 5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

bars_equal  = ax.bar(x - width/2, cc_equal, width,
                  label='Equal Weights',
                  color='#888888', edgecolor='black', linewidth=0.7)
bars_entropy = ax.bar(x + width/2, cc_entropy, width,
                  label='Entropy Weights',
                  color='#222222', edgecolor='black', linewidth=0.7)

for bar, score in zip(bars_equal, cc_equal):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.012,
            f'{score:.3f}', ha='center', va='bottom',
            fontsize=9, color='black')

for bar, score, rank in zip(bars_entropy, cc_entropy, ranks):
    offset = 0.05 if score < 0.08 else 0.012
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + offset,
            f'{score:.3f}', ha='center', va='bottom',
            fontsize=9, color='black')

ax.set_ylabel('Closeness Coefficient (CC)', fontsize=12)
ax.set_xlabel('Alloy', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(materials_sorted, fontsize=10)
ax.set_ylim(0, 1.1)
ax.legend(fontsize=10, framealpha=0.9, edgecolor='grey')
ax.yaxis.grid(True, linestyle='--', alpha=0.4, color='grey')
ax.set_axisbelow(True)
ax.tick_params(axis='y', labelsize=10)
for spine in ax.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(0.8)

plt.tight_layout()
plt.savefig('comparison.png',
            dpi=600, bbox_inches='tight', facecolor='white')
print("Done.")