import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file_path="MOSFET_ID_VDS.csv"
df=pd.read_csv(file_path)
try:
   df = pd.read_csv(file_path)
   print("CSV file successfully loaded!")
   print(df.columns) # ALWAYS check the exact column names
except FileNotFoundError: 
   print(f"Error: Could not find '{file_path}'. Check the path and try again.")
   exit()

plt.figure(figsize=(10,6))

for vgs,group in df.groupby('V_GS (V)'):
         vds=group['V_DS (V)']
         i_d=group['I_D (mA)'] # convert mA to A
         did_dvds=np.gradient(i_d,vds)
         plt.plot(vds,did_dvds,marker='o',linewidth=2,label=f'$V_{{GS}}$={vgs} V')
         highest_group = df[df['V_GS (V)'] == df['V_GS (V)'].max()].sort_values('V_DS (V)')
         g_d_sat = np.gradient(highest_group['I_D (mA)'], highest_group['V_DS (V)'])[-1]
         r_o = 1 / g_d_sat
print(f"Resistance r_o in saturation: {r_o:.2f} kΩ")
plt.title('conductance ($g_d$) vs $V_{DS}$')
plt.xlabel('$V_{DS}$ (V)')
plt.ylabel('$g_d$ (mS)')
plt.legend(title='Gate Voltage',title_fontsize='11',loc='upper left',fontsize='10')
plt.grid(True,linestyle='--',alpha=0.6)
plt.tight_layout()
plt.savefig('g_d_vs_V_ds.png',dpi=350)
plt.show()
                 