import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("MOSFET_ID_VGS.csv") # columns: V_DS (V), V_GS (V), I_D (mA)

fig, ax = plt.subplots(1, 2, figsize=(11, 4.2)) # two panels side by side

# Create a dictionary or list to store extracted VT values for later use if needed
vt_results = {}

for v_ds, g in df.groupby('V_DS (V)'):
    g = g.sort_values('V_GS (V)') # ALWAYS sort the sweep axis
    vgs = g['V_GS (V)'].to_numpy()
    id_ma = g['I_D (mA)'].to_numpy()
    
    # 1. Calculate transconductance (gm)
    gm = np.gradient(id_ma, vgs)
    
    # 2. Find the point of maximum gm
    idx_max_gm = np.argmax(gm)
    
    # 3. Fit a line around the peak gm point (using a 3-point window: idx-1, idx, idx+1)
    # Ensure window doesn't go out of bounds
    start_idx = max(0, idx_max_gm - 1)
    end_idx = min(len(vgs), idx_max_gm + 2)
    fit_window = slice(start_idx, end_idx)
    
    # np.polyfit syntax: (x_data, y_data, degree=1) -> returns [slope, intercept]
    slope, intercept = np.polyfit(vgs[fit_window], id_ma[fit_window], 1)
    
    # 4. Extrapolate to find VT (where ID = 0 -> 0 = slope * VT + intercept)
    vt = -intercept / slope
    vt_results[v_ds] = vt
    
    # 5. Define an x-axis range to plot the extrapolated tangent line safely
    # From VT up to slightly past the peak gm VGS value
    vgs_extrap = np.linspace(vt, vgs[idx_max_gm] + 0.3, 50)
    id_extrap = slope * vgs_extrap + intercept

    # --- Plotting Panel 1: Transfer Characteristics + Tangent Lines ---
    # Plot the original data
    line, = ax[0].plot(vgs, id_ma, linewidth=2, label=f'$V_{{DS}}$ = {v_ds} V ($V_{{TH}}$ = {vt:.2f} V)')
    # Plot the tangent/extrapolation line matching the color of the data line
    ax[0].plot(vgs_extrap, id_extrap, linestyle=':', color=line.get_color(), linewidth=1.5)
    # Mark the VT point on the x-axis
    ax[0].plot(vt, 0, marker='x', color=line.get_color(), markersize=6)

    # --- Plotting Panel 2: Transconductance ---
    ax[1].plot(vgs, gm, linewidth=2, label=f'$V_{{DS}}$ = {v_ds} V')
    # Mark where the max gm occurs
    ax[1].plot(vgs[idx_max_gm], gm[idx_max_gm], marker='o', color=line.get_color(), markersize=5)

# Formatting charts
ax[0].set_title('Transfer characteristics & $V_{TH}$ Extraction', fontweight='bold')
ax[0].set_xlabel('$V_{GS}$ (V)'); ax[0].set_ylabel('$I_D$ (mA)')
# Ensure the x-limit catches the lowest VT value safely
ax[0].set_ylim(bottom=0) 

ax[1].set_title('Transconductance $g_m = dI_D/dV_{GS}$', fontweight='bold')
ax[1].set_xlabel('$V_{GS}$ (V)'); ax[1].set_ylabel('$g_m$ (mS)')
ax[1].set_ylim(bottom=0)

for a in ax:
    a.grid(True, linestyle='--', alpha=0.6)
    a.legend(fontsize=9)

plt.tight_layout()
plt.savefig('gm_vth.png', dpi=300) # save BEFORE show
plt.show()

# Print text summary of results
print("\nExtracted Threshold Voltages:")
for v_ds, vt in vt_results.items():
    print(f"For V_DS = {v_ds} V: V_TH = {vt:.3f} V")