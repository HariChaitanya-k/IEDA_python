import numpy as np
import matplotlib.pyplot as plt

# ---------------- constants & given data ----------------
q, k, T = 1.602e-19, 1.381e-23, 300
eps0 = 8.854e-14                      # F/cm
eps_si, eps_ox = 11.7*eps0, 3.9*eps0
ni, Eg, chi = 1.0e10, 1.12, 4.05      # cm^-3, eV, eV (Si)
tox, NA, QF = 10e-7, 1e16, 1e12       # cm, cm^-3, cm^-2
W, L = 4e-4, 0.18e-4                  # cm
mu_n, phi_m = 400, 4.1                # cm^2/Vs, eV (Al gate)

# ---------------- derived parameters ----------------
Vt   = k*T/q
Cox  = eps_ox/tox                                    # F/cm^2
phiF = Vt*np.log(NA/ni)
phi  = 2*phiF                                        # surface potential (PHI)
phi_ms = phi_m - (chi + Eg/2 + phiF)
Vfb  = phi_ms - q*QF/Cox
gamma = np.sqrt(2*q*eps_si*NA)/Cox                   # body factor
VTO  = Vfb + phi + gamma*np.sqrt(phi)                # VSB = 0
KP   = mu_n*Cox                                      # A/V^2
print(f"Cox={Cox:.3e} F/cm2  phiF={phiF:.3f} V  Vfb={Vfb:.3f} V  "
      f"gamma={gamma:.3f} V^0.5  VTO={VTO:.3f} V  KP={KP:.3e} A/V2")

# ---------------- Level 1 ----------------
def level1(vgs, vds, lam=0.0):
    vov = vgs - VTO
    beta = KP*W/L
    if vov <= 0:
        return np.zeros_like(vds)
    return np.where(vds < vov,
                    beta*(vov*vds - vds**2/2)*(1+lam*vds),   # triode
                    0.5*beta*vov**2*(1+lam*vds))             # saturation

# ---------------- Level 3 (semi-empirical) ----------------
# Level-3 parameters (not given in the question -> typical assumed values, edit if needed)
THETA = 0.1      # mobility degradation (1/V)
ETA   = 0.1      # static feedback (DIBL)
KAPPA = 0.01     # saturation-field factor
VMAX  = 1e7      # carrier saturation velocity (cm/s)

def level3(vgs, vds):
    sigma = ETA*8.15e-22/(Cox*L**3)
    vth = Vfb + phi - sigma*vds + gamma*np.sqrt(phi)
    vgst = np.maximum(vgs - vth, 0)
    fb = 1 + gamma/(4*np.sqrt(phi))
    mu_eff = mu_n/(1 + THETA*vgst)                   # mobility degradation
    beta = mu_eff*Cox*W/L
    vsat = vgst/fb
    vc = VMAX*L/mu_eff
    vdsat = vsat + vc - np.sqrt(vsat**2 + vc**2)     # velocity-saturated Vdsat
    vde = np.minimum(vds, vdsat)
    ids = beta*(vgst - (1+fb)/2*vde)*vde
    ids = ids/(1 + vde/vc)                           # velocity saturation
    dL = np.sqrt(KAPPA*2*eps_si/(q*NA)*np.maximum(vds - vdsat, 0))
    dL = np.minimum(dL, 0.5*L)                       # channel length modulation
    ids = np.where(vds > vdsat, ids/(1 - dL/L), ids)
    return np.where(vgst > 0, ids, 0)

# ---------------- plotting ----------------
vds = np.linspace(0, 4, 401)
for name, fn, fname in [("SPICE Level 1", lambda g: level1(g, vds), "E12_level1.png"),
                        ("SPICE Level 3", lambda g: level3(g, vds), "E12_level3.png")]:
    plt.figure(figsize=(7, 5))
    for vgs in (1, 2, 3):
        plt.plot(vds, fn(vgs)*1e3, label=f"$V_{{GS}}$ = {vgs} V")
    plt.xlabel("$V_{DS}$ (V)"); plt.ylabel("$I_D$ (mA)")
    plt.title(f"$I_D$-$V_{{DS}}$ characteristics ({name})")
    plt.grid(True); plt.legend()
    plt.savefig(fname, dpi=350, bbox_inches="tight")   # 350 dpi PNG
plt.show()