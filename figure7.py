import sys
import os
from matplotlib.cm import ScalarMappable
import pandas as pd

sys.path.append(os.path.dirname(__file__))

from utils import *


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': FONT_SIZE})
plt.rcParams["figure.figsize"] = (6, 4)
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

fig, axs = plt.subplots(1, 4, figsize=(16,3))

idf = pd.read_csv(RESULTS_DIR + f"/figure7_cascade.csv")
adf = pd.read_csv(RESULTS_DIR + f"/figure7_raspberrypi.csv")

idf["Speed-up vs Dense"] = idf[f"time median|MKL_Dense"] / idf[f"time median|Sp. Reg."]
idf["Speed-up vs Sparse"] = idf[f"time median|MKL_Sparse"] / idf[f"time median|Sp. Reg."]
idf = idf[idf["Speed-up vs Dense"] > 0.0]
idf = idf[idf["Speed-up vs Dense"] < 10]
idf = idf[idf["Speed-up vs Sparse"] > 0.0]
idf = idf[idf["Speed-up vs Sparse"] < 10]

adf["Speed-up vs Dense"] = adf[f"time median|ARMCL"] / adf[f"time median|Sp. Reg."]
adf["Speed-up vs Sparse"] = adf[f"time median|XNN"] / adf[f"time median|Sp. Reg."]
adf = adf[adf["Speed-up vs Dense"] > 0.0]
adf = adf[adf["Speed-up vs Dense"] < 10]
idf = idf[idf["Speed-up vs Sparse"] > 0.0]
idf = idf[idf["Speed-up vs Sparse"] < 10]

adf = adf.sort_values(by=['sparsity'], ascending=True)
idf = idf.sort_values(by=['sparsity'], ascending=True)

idf = idf[(idf['sparsity'] >= 0.6) & (idf['sparsity'] <= 0.95)]
adf = adf[(adf['sparsity'] >= 0.6) & (adf['sparsity'] <= 0.95)]

adf['flops'] = adf['gflops'] * 1e9
idf['flops'] = idf['gflops'] * 1e9

ax = axs[0]
idf.plot(kind='scatter', x='flops', y='Speed-up vs Sparse', c='sparsity', colormap='cividis', alpha=0.5, s=1, ax=ax, colorbar=False)
ax.set_xscale('log')
ax.set_ylim(0, 8)
ax.set_ylabel('Speedup', fontsize=14)
ax.axhline(y=1.0, color='r', linestyle='-')
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.set_title(f'Versus MKL SpMM (CSR)', fontsize=16, pad=15)
ax.set_xlabel('Problem Size (FLOPs)', fontsize=14)

ax = axs[1]
idf.plot(kind='scatter', x='flops', y='Speed-up vs Dense', c='sparsity', colormap='cividis', alpha=0.5, s=1, ax=ax, colorbar=False)
ax.set_xscale('log')
ax.set_ylim(0, 8)
ax.set_ylabel(None)
ax.axhline(y=1.0, color='r', linestyle='-')
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.set_title(f'Versus MKL SGEMM', fontsize=16, pad=15)
ax.set_xlabel('Problem Size (FLOPs)', fontsize=14)

ax = axs[2]
adf.plot(kind='scatter', x='flops', y='Speed-up vs Sparse', c='sparsity', colormap='cividis', alpha=0.5, s=1, ax=ax, colorbar=False)
ax.set_xscale('log')
ax.set_ylim(0, 8)
ax.set_ylabel(None)
ax.axhline(y=1.0, color='r', linestyle='-')
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.set_title(f'Versus XNN SpMM', fontsize=16, pad=15)
ax.set_xlabel('Problem Size (FLOPs)', fontsize=14)

ax = axs[3]
s = adf.plot(kind='scatter', x='flops', y='Speed-up vs Dense', c='sparsity', colormap='cividis', alpha=0.5, s=1, ax=ax, colorbar=False)
ax.set_xscale('log')
ax.set_ylim(0, 8)
ax.set_ylabel(None)
ax.axhline(y=1.0, color='r', linestyle='-')
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.set_title(f'Versus ARMCL SGEMM', fontsize=16, pad=15)
ax.set_xlabel('Problem Size (FLOPs)', fontsize=14)


cmap = plt.get_cmap("cividis")
norm = plt.Normalize(60, 95)
sm =  ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])
cbar = fig.colorbar(sm, ax=axs, pad=0.02)
cbar.set_label("Sparsity", labelpad=6, y=0.45)
savefig(f'figure7.pdf')