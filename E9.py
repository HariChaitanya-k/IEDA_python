import pandas as pd, numpy as np,  matplotlib.pyplot as plt
df=pd.read_csv("MOSFET_ID_VGS.csv")
fig, ax=plt.subplots(1,2,figsize=(11,4.2))

for v_ds, group in df.groupby('V_DS (V)'):
    v_gs=group['V_GS (V)']
    i_d=group['I_D (mA)']*1e-3
    ax[0].plot(v_gs,i_d,marker='o',linewidth=2,label=f'$V_{{DS}}$={v_ds} V')
    ax[1].plot(v_gs,np.gradient(i_d,v_gs),marker='o',linewidth=2,label=f'$V_{{DS}}$={v_ds} V')
ax[0].set_title('MOSFET Output Characteristics')
ax[0].set_xlabel('$V_{GS}$ (V)')
ax[0].set_ylabel('$I_D$ (A)')

ax[1].set_title('conductance ($g_d$) vs $V_{GS}$')
ax[1].set_xlabel('$V_{GS}$ (V)')        
ax[1].set_ylabel('$g_d$ (mS)')

for a in ax:
     a.grid(True, linestyle='--', alpha=0.6)
     a.legend(fontsize=9)
plt.tight_layout()
plt.savefig('gm_transfer.png', dpi=300) # save BEFORE show
plt.show()
