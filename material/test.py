import sys, platform, os
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import integrate
import copy

###############################################################################
# EFTCAMB MOD START: update the tutorial imports to target the standalone H-EFTCAMB package.
# import H-EFTCAMB:
###############################################################################

#here = os.path.dirname(os.path.abspath(__file__))
here = './'
eftcamb_path = os.path.realpath(os.path.join(os.getcwd(), here))
sys.path.insert(0, eftcamb_path)
import eftcamb
eftcamb.set_feedback_level(10)
from eftcamb import model, initialpower
from eftcamb.baseconfig import CAMBError
# EFTCAMB MOD END

###############################################################################
# EFTCAMB MOD START: run the tutorial GR-limit calculation through eftcamb.
# run H-EFTCAMB in the GR limit:
###############################################################################

# set parameters:
pars_LCDM = eftcamb.set_params(As=2.12605e-9,
                            ns=0.96,
                            H0=67.,
                            ombh2=0.022445,
                            omch2=0.120557,
                            mnu=0.06,
                            tau=0.079)
pars_LCDM.NonLinear = eftcamb.model.NonLinear_none
# compute the spectra:
results_LCDM = eftcamb.get_results(pars_LCDM)
# EFTCAMB MOD END
# get the power spectrum:
LCDM_TT_spectrum = copy.deepcopy(results_LCDM.get_cmb_power_spectra(pars_LCDM, CMB_unit='muK')['total'][:,0])
LCDM_ell = np.arange(LCDM_TT_spectrum.shape[0])

###############################################################################
# EFTCAMB MOD START: run the modified-gravity tutorial calculation through eftcamb.
# run EFTCAMB:
###############################################################################

eftcamb_params = {'EFTflag':1,
                  'PureEFTmodel':1,
                  'PureEFTmodelOmega':1,
                  'EFTOmega0':1.0,
                  'feedback_level':10}

pars_EFT = eftcamb.set_params(As=2.12605e-9,
                           ns=0.96,
                           H0=67.,
                           ombh2=0.022445,
                           omch2=0.120557,
                           mnu=0.06,
                           tau=0.079,
                           **eftcamb_params)
pars_EFT.NonLinear = eftcamb.model.NonLinear_none
# compute the spectra:
results_EFT = eftcamb.get_results(pars_EFT)
# EFTCAMB MOD END
# get the power spectrum:
EFT_TT_spectrum = copy.deepcopy(results_EFT.get_cmb_power_spectra(pars_EFT, CMB_unit='muK')['total'][:,0])
EFT_ell = np.arange(EFT_TT_spectrum.shape[0])

# standard test:
print('***********************************************************************')
eta = np.linspace(1, 400, 300)
ks = [0.02,0.1]
ev = results_EFT.get_time_evolution(ks, eta, ['delta_baryon','delta_photon'])
_, axs= plt.subplots(1,2, figsize=(12,5))
for i, ax in enumerate(axs):
    ax.plot(eta,ev[i,:, 0])
    ax.plot(eta,ev[i,:, 1])
    ax.set_title('$k= %s$'%ks[i])
    ax.set_xlabel(r'$\eta/\rm{Mpc}$');
plt.legend([r'$\Delta_b$', r'$\Delta_\gamma$'], loc = 'upper left');
plt.show()
plt.close('all')

# test EFTCAMB a bit:
print('***********************************************************************')
x = np.logspace(-8,0,1000)
vars, val = pars_EFT.EFTCAMB.get_scale_evolution(results_EFT, [0.01,0.1,1.0], x )

plt.plot( val[0,:]['a'], np.abs(val[0,:]['sigma']) )
plt.plot( val[1,:]['a'], np.abs(val[1,:]['sigma']) )
plt.plot( val[2,:]['a'], np.abs(val[2,:]['sigma']) )
plt.xscale('log')
plt.yscale('log')
plt.show()
plt.close('all')

# test EFTCAMB a bit:
print('***********************************************************************')
k = np.logspace(-6,0,100)
a = np.array([1.0])

vars, val = pars_EFT.EFTCAMB.get_scale_evolution(results_EFT, k, a)
vars_ref, val_ref = pars_LCDM.EFTCAMB.get_scale_evolution(results_LCDM, k, a)

plt.plot( val[:, 0]['k'], np.abs(val[:, 0]['mu']) )
plt.plot( val_ref[:, 0]['k'], np.abs(val_ref[:, 0]['mu']) )
plt.xscale('log')
plt.yscale('log')
plt.show()
plt.close('all')

plt.plot( val[:, 0]['k'], np.abs(val[:, 0]['gamma']) )
plt.plot( val_ref[:, 0]['k'], np.abs(val_ref[:, 0]['gamma']) )
plt.xscale('log')
plt.yscale('log')
plt.show()
plt.close('all')

plt.plot( val[:, 0]['k'], np.abs(val[:, 0]['sigma_eft']) )
plt.plot( val_ref[:, 0]['k'], np.abs(val_ref[:, 0]['sigma_eft']) )
plt.xscale('log')
plt.yscale('log')
plt.show()
plt.close('all')


print('***********************************************************************')
print(pars_EFT.EFTCAMB)
print('***********************************************************************')
pars_EFT.EFTCAMB.feedback()
print('***********************************************************************')
print(pars_EFT.EFTCAMB.num_params())
print('***********************************************************************')
print(pars_EFT.EFTCAMB.param_names())
print('***********************************************************************')
print(pars_EFT.EFTCAMB.param_labels())

print('***********************************************************************')
print(pars_EFT.EFTCAMB.param_values())

print('***********************************************************************')
print(pars_EFT.EFTCAMB.model_name())
pars_EFT.EFTCAMB.set_model_name('test model')
print(pars_EFT.EFTCAMB.model_name())


print('***********************************************************************')
# test parameter cache a bit:
print(pars_EFT.EFTCAMB_parameter_cache)

print('***********************************************************************')
print(pars_EFT.EFTCAMB.read_parameters())

###############################################################################
# compare the results:
###############################################################################

plt.plot(LCDM_ell[2:], LCDM_TT_spectrum[2:], label='LCDM')
plt.plot(EFT_ell[2:], EFT_TT_spectrum[2:], label='EFT test')
plt.xscale('log')
plt.legend()
plt.show()
plt.close('all')

###############################################################################
# example stability plot:
###############################################################################

# EFTCAMB MOD START: use eftcamb while scanning stability in the tutorial.
eftcamb.set_feedback_level(0)

par = np.linspace(-0.5,0.5,100)
stability_result = []
for ind, par_val in enumerate(par):
    eftcamb_params = {'EFTflag':1,
                      'PureEFTmodel':1,
                      'PureEFTmodelOmega':1,
                      'EFTOmega0':par_val,
                      'feedback_level':0}
    pars = eftcamb.set_params(lmax=2500,
                           As=2.12605e-9,
                           ns=0.96,
                           H0=67.,
                           ombh2=0.022445,
                           omch2=0.12055785610846023,
                           mnu=0.06,
                           tau=0.079,
                           **eftcamb_params)
    # to get just the stability try setting the parameters and intercept:
    try:
        results = eftcamb.get_background(pars)
        stability_result.append(1.)
    except CAMBError:
        stability_result.append(0.)
# EFTCAMB MOD END

stability_result = np.array(stability_result)

plt.plot(par, stability_result)
plt.xlabel('Omega 0')
plt.ylabel('Stability')
plt.show()
plt.close('all')

pass
