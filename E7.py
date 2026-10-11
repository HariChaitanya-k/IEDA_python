# =====================================================================
# EC2L104 - Introduction to EDA Tools
# Reads a CSV file of MOSFET output characteristics exported from the
# simulator, plots I_D vs V_DS for every gate voltage
#====================================================================
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
       i_d=group['I_D (mA)']*1e-3 # convert mA to A
       plt.plot(vds,i_d,marker='o',linewidth=2,label=f'$V_{{GS}}$={vgs} V')

plt.title('MOSFET Output Characteristics')
plt.xlabel('$V_{DS}$ (V)')
plt.ylabel('$I_D$ (A)')
plt.legend(title='Gate Voltage',title_fontsize='11',loc='upper left',fontsize='10')
plt.grid(True,linestyle='--',alpha=0.6)
plt.tight_layout()
plt.savefig('I_d_vs_V_ds.png',dpi=350)

plt.show()