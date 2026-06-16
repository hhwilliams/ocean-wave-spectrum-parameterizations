from matplotlib import pyplot as plt
from matplotlib import pylab as pl
import numpy as np
import pandas as pd
# from matplotlib import cm

import cmcrameri.cm as cmc
from matplotlib import rcParams

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.io import loadmat
from matplotlib.colors import LogNorm

from statData import StatData

nu = 1.8e-5


def make_statlist(caseids, ids, case_info):
    time_window = [0,10]
    dirname = ''

    statlist = {}
    for id, case in zip(ids, caseids):
            casename = case.split('/')[0]
            cinf = case_info.loc[casename]
            stat_params = cinf.to_dict()
            fname = dirname+casename+'.txt'
            statlist[id] = StatData(fname, ustar=stat_params['ustar_mean'])
            # statlist[id] = StatData.PVstat(id, case, params=stat_params, dirname=dirname, 
            #                             time_index=1, time_window=time_window,
            #                             save_mean=False, read_save=True)
    
    return statlist


def plot_velocity(stats, ids, colors, linestyles=['-'], axs=[], 
                  labels=True, xlabel=True):
    if len(axs) == 0:
        fig, axs = plt.subplots(1,2,facecolor='w', dpi=180.0, 
                                tight_layout=True, figsize=(8,4))

    if len(linestyles) < len(ids):
        linestyles = [linestyles[0] for i in range(len(ids))]

    for i in range(len(ids)):
        id = ids[i]
        u = stats[id].data['U']
        y = stats[id].data['ym']

        for axi in range(2):
            axs[axi].plot(u, y, lw=2, color=colors[i], ls=linestyles[i], 
                        label=id, zorder=1)
        
        # * viscous scaling
        ustar = stats[id].ustar
        H = 1000

        axs[2].plot(y[1:]/H, u[1:]/ustar, marker='.', ls=linestyles[i],
                    color=colors[i], label=id, zorder=1)
        
        # * some info
        print(ids[i])
        # print('U_bulk: {:.1f}'.format(stats[id].bulk_vel()))
        # print('U(1000): {:.1f}\n'.format(stats[id].Uz(1000)))
        print('U(150): {:.1f}'.format(stats[id].Uz(150)))
        print('U(20): {:.1f}'.format(stats[id].Uz(20)))
        print('U(10): {:.1f}\n'.format(stats[id].Uz(10)))


    axs[0].axhline(150, color='gainsboro', zorder=0)#, label='Example Turbine Hub')
    axs[2].axvline(150/H, color='gainsboro', zorder=0)

    # axs[0].axhline(20, color='gainsboro', zorder=0)
    axs[1].axhline(20, color='gainsboro', zorder=0)
    axs[2].axvline(20/H, color='gainsboro', zorder=0)

    # axs[0].axhspan(30, 270, color='gainsboro', label='Example Turbine Rotor', zorder=0)
    # axs[1].axvspan(30/H, 270/H, color='gainsboro', zorder=0)

    axs[0].set_ylim((0,1000))
    # axs[0].set_xlim((10,18))
    axs[0].set_xlim((10,27))

    axs[1].set_ylim((1,100))
    axs[1].set_xlim((2,21))

    for axi in range(2):
        if xlabel:
            axs[axi].set_xlabel('U (m/s)')
        axs[axi].set_ylabel('z (m)')

    if labels:
        axs[0].legend(loc='upper left', labelspacing=0.7)

    if xlabel:
        axs[2].set_xlabel(r'$z/H$')

    axs[2].set_ylabel(r'$\langle \overline{u}\rangle/u_\ast$')
    axs[2].set_xscale('log')
    axs[2].set_xlim((1e-3, 1))

    # return fig, axs


def plot_reynolds(stats, ids, colors, linestyles=['-'], fig=None, axs=None, labels=True):
    if not fig:
        fig, axs = plt.subplots(2, 3, facecolor='w', dpi=180, constrained_layout=True,
                                figsize=(10,6), sharey=True)

    plot_ids = ['up_up','vp_vp','wp_wp','up_vp','up_wp','vp_wp']
    plot_labels = [r"$\langle u'u'\rangle$", r"$\langle v'v'\rangle$",
                r"$\langle w'w'\rangle$", r"$\langle u'v'\rangle$",
                r"$\langle u'w'\rangle$", r"$\langle v'w'\rangle$"]


    for j in range(len(plot_ids)):
        axi = int(j/3)
        axj = j%3

        ax = axs[axi,axj]

        for i in range(len(ids)):
            id = ids[i]

            if labels:
                ax.plot(stats[id].data[plot_ids[j]],stats[id].data['ym'],
                        lw=1.2, color=colors[i], ls=linestyles[i], label=id)
            else:
                ax.plot(stats[id].data[plot_ids[j]],stats[id].data['ym'],
                    lw=1.2, color=colors[i], ls=linestyles[i])
            
        ax.axhline(150, color='gainsboro', label='Example Turbine Hub', zorder=0)
        # ax.axhspan(30, 270, color='gainsboro', label='Example Turbine Rotor', zorder=0)

        if axj == 0:   
            ax.set_ylabel(r'$y$')
        ax.set_title(plot_labels[j])
        
        ax.set_ylim((0,1000))

    axs[0,0].legend()



def plot_upvp(stats, ids, colors, ax=False, labels=True, xlabel=True,
              linestyles=['-']):
    if not ax:
        fig, ax = plt.subplots(1,1, facecolor='w', dpi=180, figsize=(5.2,4.6))

    if len(linestyles) < len(ids):
        linestyles = [linestyles[0] for i in range(len(ids))]

    for i in range(len(ids)):
        id = ids[i]
        ax.plot(stats[id].data['up_vp'], stats[id].data['y'],
                lw=2, color=colors[i], linestyle=linestyles[i], label=id)

    # ax.axhline(150, color='gainsboro', zorder=0)
    ax.axhline(150, color='gainsboro', label='Example Turbine Hub', zorder=0)
    # ax.axhspan(30, 270, color='gainsboro', label='Example Turbine Rotor', zorder=0)
    
    if xlabel:
        ax.set_xlabel(r"$\langle u'w' \rangle$ (m$^2$/s$^2$)")
    ax.set_ylabel(r'$z$ (m)')
    
    ax.set_ylim((0,1000))

    if labels:
        ax.legend()


def plot_tke(stats, ids, colors, ax=False, labels=True, xlabel=True,
              linestyles=['-']):
    if not ax:
        fig, ax = plt.subplots(1,1, facecolor='w', dpi=180, figsize=(5.2,4.6))

    if len(linestyles) < len(ids):
        linestyles = [linestyles[0] for i in range(len(ids))]

    for i in range(len(ids)):
        id = ids[i]

        ax.plot(stats[id].data['tke'], stats[id].data['y'],
                lw=2, color=colors[i], linestyle=linestyles[i], label=id)

        print('TKE(150) for '+id.replace("\n","").ljust(30)+': {:.2f}'.format(stats[id].Uz(150, val='tke')))
        print('TKE(20) for '+id.replace("\n","").ljust(30)+': {:.2f}\n'.format(stats[id].Uz(20, val='tke')))


    # ax.axhline(150, color='gainsboro', zorder=0)
    ax.axhline(150, color='gainsboro', label='Example Turbine Hub Height', zorder=0)
    # ax.axhspan(30, 270, color='gainsboro', label='Example Turbine Rotor', zorder=0)
    
    if xlabel:
        ax.set_xlabel(r"$TKE$ (m$^2$/s$^2$)")
    ax.set_ylabel(r'$z$ (m)')
    
    ax.set_ylim((0,1000))

    if labels:
        ax.legend()


def coare_plot_starter(figsize, colormode='light', Romero_colorby='none', Romero_cmap='none'):

    if colormode == 'light':
        ed_color = 'silver'
        ed_alpha = 0.75
        coare_color = 'k'
    elif colormode == 'dark':
        ed_color = '#3a1124'
        ed_alpha = 0.4
        coare_color = 'silver'


    # * COARE 3.5 formula
    ncoare = 500
    u10_coare = np.linspace(1,21,ncoare)
    ustar_coare = np.empty(ncoare)

    for i in range(ncoare):
        if u10_coare[i] < 4:
            ustar_coare[i] = 0.03 * u10_coare[i]
        elif u10_coare[i] < 9.6:
            ustar_coare[i] = 0.035 * u10_coare[i] - 0.005*4
        else:
            # ustar_coare[i] = 0.058 * u10_coare[i] - 0.24 # Andreas et al. (2012)
            ustar_coare[i] = 0.062 * u10_coare[i] - 0.28

    fig, ax = plt.subplots(1,1,facecolor='w', dpi=180.0,tight_layout=True, figsize=figsize)

    # * Edson
    ed = loadmat('experimental_data/TauDataEdson.mat')
    plt.scatter(ed['U10Nalex'], np.sqrt(ed['TAUalex']/1.2), s=6, marker='x', 
                color=ed_color, alpha=ed_alpha, lw=0.3,
                label='Edson et al. 2013', zorder=1)
    

    # * Romero data (GOTEX)
    rom = pd.read_csv('experimental_data/romero_summary.csv', header=0, sep=' ',index_col=False)
    rom['hs'] = 4*np.sqrt(rom['eta_sq'])
    rom['kphs'] = rom['hs']*rom['kp']

    if Romero_colorby == 'none':
        ax.scatter(rom['U10'],rom['ustar'],c='black',
                   s=5,label='GOTEX',zorder=2)
    elif Romero_colorby == 'hs':
        rsc = ax.scatter(rom['U10'],rom['ustar'],c=rom['hs'],
                            cmap=Romero_cmap, vmin=0, vmax=4,
                            s=5,label='GOTEX',zorder=2)
        plt.colorbar(rsc, label=r'Romero $H_s$')
    elif Romero_colorby == 'kphs':
        rsc = ax.scatter(rom['U10'],rom['ustar'],c=rom['kphs'],
                            cmap=Romero_cmap, vmin=0, vmax=0.3,
                            s=5,label='GOTEX',zorder=2)
        plt.colorbar(rsc, label=r'$k_pH_s$')


    # * COARE 3.5 line
    plt.plot(u10_coare,ustar_coare,
            color=coare_color,
            lw=2,label='COARE 3.5', zorder=2)

    ax.set_xlabel(r'$U_{10}$ (m/s)')
    ax.set_ylabel(r'$u_*$ (m/s)')

    ax.legend()

    ax.set_xlim((0,21.0))
    ax.set_ylim((0,1.2))
    
    # ax.set_xlim((0,24.0))
    # ax.set_ylim((0,1.4))

    return fig, ax

    

def plot_charnock(ax, color='k', ls='-', lw=1.5, label='Charnock 1955'):
    ch_ustars = np.linspace(1e-3,0.9, 500)
    charnock_U10s = ch_ustars / 0.4 * np.log(10*9.81 / 0.011 / ch_ustars**2)

    ax.plot(charnock_U10s, ch_ustars, 
            color=color, ls=ls, lw=lw, label=label)
    


def plot_coare(ax, color='k', ls='-', lw=1.5, label='COARE 3.5'):
    # * COARE 3.5 formula
    ncoare = 500
    u10_coare = np.linspace(1,20,ncoare)
    ustar_coare = np.empty(ncoare)

    for i in range(ncoare):
        if u10_coare[i] < 4:
            ustar_coare[i] = 0.03 * u10_coare[i]
        elif u10_coare[i] < 9.6:
            ustar_coare[i] = 0.035 * u10_coare[i] - 0.005*4
        else:
            # ustar_coare[i] = 0.058 * u10_coare[i] - 0.24 # Andreas et al. (2012)
            ustar_coare[i] = 0.062 * u10_coare[i] - 0.28

    ax.plot(u10_coare,ustar_coare,
            color=color, ls=ls, lw=lw, label=label,
              zorder=2)
    

def plot_ncar(ax, color='k', ls='--', lw=1.5, label = 'Large et al. 2004'):
    nu10 = 500
    u10 = np.linspace(1,21,nu10)

    # * NCAR formulation
    ncard = 0.0027 / u10 + 0.000142 + 0.0000764 * u10
    ustar_ncar = np.sqrt(ncard) * u10

    ax.plot(u10, ustar_ncar,
            color=color, ls=ls, lw=lw, label=label,
            zorder=2)


def z0(U10, ustar):
    kappa = 0.4
    z0 = 10 / np.exp(U10*kappa/ustar)
    return z0



def coare_color_by_z0(ax_in, xlim, ylim):
    res = 1000
    u10s = np.linspace(xlim[0],xlim[1],res)
    ustars = np.linspace(ylim[0]+0.01,ylim[1],res)

    X, Y = np.meshgrid(u10s, ustars)
    Z = z0(X,Y)
    # levels = np.logspace(np.log10(Z.min()), np.log10(Z.max()), 10)
    levels = np.logspace(-8,1,10)
    # levels = np.logspace(-10,1,12)

    if not ax_in:
        fig, ax = plt.subplots(1,1, facecolor='w', dpi=180.0,tight_layout=True,figsize=(6,5))
        plt.xlabel(r'$U_{10}$ (m/s)')
        plt.ylabel(r'$u_*$ (m/s)')
    else:
        ax = ax_in

    cmap = cmc.lapaz_r
    # cmap = cmc.glasgow_r

    contours = ax.contour(X, Y, Z, levels=levels, norm=LogNorm(), cmap=cmap, zorder=0)
    cf = ax.contourf(X, Y, Z, levels=levels, norm=LogNorm(), cmap=cmap, zorder=0)
    # ax.clabel(contours, inline=True, fontsize=10, fmt="%.1e", colors='black')
    # fig.colorbar(cf, label=r"$z_0$", ticks=levels)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    if not ax_in:
        return fig, ax

    # plt.xlabel(r'$U_{10}$ (m/s)')
    # plt.ylabel(r'$u_*$ (m/s)')