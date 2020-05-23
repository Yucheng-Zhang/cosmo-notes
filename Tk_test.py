import numpy as np
import camb
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'font.size': 11})

camb_pars = camb.CAMBparams()
camb_pars.set_cosmology(H0=67.66, ombh2=0.02242, omch2=0.11933, omk=0.0,
                        TCMB=2.7255, nnu=3.046)
camb_pars.InitPower.set_params(As=2.105e-9, ns=0.9665)

camb_pars.set_accuracy(AccuracyBoost=1.0)

camb_pars.set_matter_power(redshifts=(0.0,), kmax=10, nonlinear=True,
                           accurate_massive_neutrino_transfers=False)
camb_pars.set_nonlinear_lensing(False)

camb_results = camb.get_results(camb_pars)
matter_trans = camb_results.get_matter_transfer_data()
ks = matter_trans.q  # in Mpc^{-1}
Tk_tot = matter_trans.transfer_data[camb.model.Transfer_tot-1, :, 0]

# with NonLinear_both
pars_cp = camb_pars.copy()
pars_cp.NonLinear = camb.model.NonLinear_both
results_cp = camb.get_results(pars_cp)

trans_cp = results_cp.get_matter_transfer_data()
Tk_tot_cp = trans_cp.transfer_data[camb.model.Transfer_tot-1, :, 0]

# plot
fig, (ax) = plt.subplots(1, 1, figsize=(8, 5))

ax.plot(ks, Tk_tot, label='NonLinear = '+camb_pars.NonLinear)
ax.plot(ks, Tk_tot_cp, label='NonLinear = '+pars_cp.NonLinear)

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'$k$ [Mpc$^{-1}$]')
ax.set_ylabel(r'$T(k,z=0)$')
ax.set_title(r'Total matter transfer function at $z = 0$, unnormalized')
ax.legend()

plt.show()
