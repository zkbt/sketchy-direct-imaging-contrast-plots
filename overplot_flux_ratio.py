#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ZKBT sketchily modified this module on 7 May 2026 from 
# github.com/nasavbailey/DI-flux-ratio-plot 
# Please don't treat this file as authoratative in anyway.
# Go to the original source, please!!!

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams
import matplotlib.patheffects as PathEffects
from astropy.io import ascii
from astropy import units as u
import yaml
from glob import glob
from datetime import date
import os





### import YAML file of user-defined options
cfglist = glob('*yml')
if len(cfglist) > 1:
    raise Exception(('Mulitple YAML config files present: %s.\nMove all but desired config file to another folder.')%flist)
if len(cfglist) == 0:
    raise Exception('No .yml config files present. Place your .yml file in the same directory as plot_flux_ratio.py.')
with open(cfglist[0],'r') as f:
    cfg = yaml.safe_load(f)
    cfgname = cfglist[0].split('.yml')[0]

###Define path where to find data and where to save plot
datapath = './data/'

### hardcoded constants
d_tel = 2.4 * u.m

########################################################################
### Plot setup

rcParams['figure.autolayout'] = True
rcParams['font.size'] = cfg['plot_font_size']
rcParams['mathtext.fontset'] = cfg['math_font']
rcParams['lines.solid_capstyle'] = 'butt' #don't increase line length when increasing width
rcParams['patch.linewidth'] = cfg['marker_edge_width']  # make marker edge linewidths narrower for scatter

xlim = np.array([float(cfg['x0']), float(cfg['x1'])])
ylim = np.array([float(cfg['y0']), float(cfg['y1'])])

ccfs = cfg['label_font_size']
lw1 = cfg['other_linewidth']
lw2 = cfg['roman_linewidth']
lss = cfg['roman_linestyle_short']
lsm = cfg['roman_linestyle_medium']
lsl = cfg['roman_linestyle_long']

pred_img = cfg['pred_img_short'] or cfg['pred_img_medium'] or cfg['pred_img_long']
pred_spec = cfg['pred_spec_short'] or cfg['pred_spec_medium'] or cfg['pred_spec_long']
pred_wide_img = cfg['pred_wide_img_short'] or cfg['pred_wide_img_medium'] or cfg['pred_wide_img_long']




if cfg['color_by_lambda'].lower() == 'full':
    c_v = 'dodgerblue'
    c_bbvis = 'cadetblue'
    c_band3 = 'goldenrod'
    c_band4 = 'orange'
    c_yjh = 'coral'
    c_k = 'firebrick'
    c_h   = 'red'
    c_pl = 'c'


elif cfg['color_by_lambda'].lower() == 'simple':
    c_v = 'dodgerblue'
    c_bbvis = c_v
    c_band3 = 'orange'
    c_band4 = 'tomato'
    c_yjh = 'firebrick'
    c_h = c_yjh
    c_k = c_yjh
    c_pl = 'c'


elif cfg['color_by_lambda'].lower() == 'minimal':
    c_v = 'dodgerblue'
    c_bbvis = c_v
    c_band3 = c_v
    c_band4 = c_v
    c_yjh = 'firebrick'
    c_h = c_yjh
    c_k = c_yjh
    c_pl = 'c'


elif cfg['color_by_lambda'].lower() == 'none':
    ccc = 'k'
    c_v = ccc
    c_bbvis = ccc
    c_band3 = ccc
    c_band4 = ccc
    c_yjh = ccc
    c_k = ccc
    c_h   = ccc
    c_pl = ccc

else:
    raise Exception(cfg['color_by_lambda']+' is not a valid option for color_by_lambda (full/simple/none)')




# text about detection limit curves
def plot_detection_limit_text():
    plt.text(0.95*xlim[-1], ylim[0]*1.1, \
    ' Instrument curves are 5$\mathdefault{\sigma}$ post-processed detection limits.',\
    horizontalalignment='right', verticalalignment='bottom',\
    fontsize=ccfs+1, color='k', weight='bold')#, backgroundcolor='white')

########################################################################
# auto-generated caption. See README for how to comment datafiles.
# auto-generated caption
caption = '** This short caption is auto-generated. DO NOT EDIT. **\n' + \
        'Please see individual datafiles for full descriptions. \n'
# caption =  'This file was generated on %s\n'%str(date.today())
caption = 'Config file used = %s\n\n'%cfglist[0]

if cfg['color_by_lambda'].lower() != 'none':
    caption = 'Lines and points are color coded by wavelength of observation.\n\n'

def extract_short_caption(filename):
    f = open(filename,'r')
    lines = f.readlines()
    f.close()
    for l in lines:
        if '#short caption:' in l.lower():
            return '-- '+l.split('caption:')[1].strip()+'\n\n'
    # if no caption in text file
    print('\n**** WARNING **** no caption for '+filename+'\n')
    return ''


def position_text(x, y):
    xy = [np.sqrt(np.nanmax(x)*np.nanmin(x)), np.sqrt(np.nanmax(y)*np.nanmin(y))]
    return xy


#########################################################################
###### --------- instrument detection limits-----------------  ##########
#########################################################################

########################################################################
### ELT guess

def plot_ELT_contrast():
    range_x = np.array((0.03, 1))
    pessimistic_y = np.array((1E-5, 1E-8))
    optimistic_y=np.array((1E-8, 1E-9))
    plt.plot(range_x, pessimistic_y, color=c_h, linestyle='--', linewidth=lw1, alpha=0.5)
    plt.plot(range_x, optimistic_y, color=c_h, linestyle='--', linewidth=lw1, alpha=0.5)
    plt.fill_between(range_x, pessimistic_y, optimistic_y, color=c_h, alpha=0.1)

    plt.text(0.08, 3E-7, 'ELT goal', color=c_h, horizontalalignment='left',\
        verticalalignment='top', fontsize=ccfs)

    caption = '-- ELT goal: Possible range of near-IR post-processed detection limits for ' + \
                'next generation extremely large telescopes. \n\n'

#########################################################################
### HabEx "goal" detection limit

def plot_HWO_contrast():
    plt.plot([0.06, 1.65],[1e-10, 1e-10],color=c_bbvis,linestyle='--',linewidth=lw1,label='')
    plt.text(1.6,6E-11,'HWO?',color=c_bbvis,horizontalalignment='right',fontsize=ccfs)
    caption = '-- HabEx: Goal 5-sigma post-processed contrast.  '+\
                'IWA ~ 2.5 lambda/D @ 450nm; OWA ~ 32 l/D @ 1micron '+\
                '(source: B. Mennesson, personal communication)\n\n'


#########################################################################
### NIRCAM F356W detection limit

def plot_NIRCam_contrast():
    fname = datapath+'jwst_nircam_F356W.txt'
    a_JWST = ascii.read(fname)
    plt.plot(a_JWST['Rho(as)'], a_JWST['356W_contrast'], color=c_k, linewidth=lw1, label='')
    x, y = a_JWST['Rho(as)'], a_JWST['356W_contrast']
    xy = position_text(x, y)
    plt.text(xy[0],xy[1], 'JWST NIRCam', color=c_k, fontsize=ccfs, va='bottom', ha='center')
    caption = extract_short_caption(fname)



def plot_NIRSpec_contrast():
    fname = datapath+'ruffio-nirspec.csv'
    a_JWST = ascii.read(fname)

    plt.plot(a_JWST['x'], a_JWST['y'], color=c_k, linewidth=lw1, label='3-5$\mu$m')
    x, y = a_JWST['x'], a_JWST['y']
    xy = position_text(x, y)
    plt.text(xy[0],xy[1], 'JWST NIRSpec', color=c_k, fontsize=ccfs, \
        va='bottom', ha='center')

    caption = extract_short_caption(fname)


#########################################################################
### NICMOS detection limit

def plot_NICMOS_contrast():
    fname = datapath+'HST_NICMOS_Min.txt' #path+'HST_NICMOS_Median.txt'
    a_NICMOS = ascii.read(fname)
    plt.plot(a_NICMOS['Rho(as)'],a_NICMOS['F160W_contr'],color=c_h,\
        linewidth=lw1, label='1.6$\mu$m')
    
    x, y = a_NICMOS['Rho(as)'],a_NICMOS['F160W_contr']
    xy = position_text(x, y)

    plt.text(xy[0], xy[1], 'HST NICMOS',\
        color=c_h, \
        rotation=-20,fontsize=ccfs, va='bottom', ha='center')
    caption = extract_short_caption(fname)


#########################################################################
### STIS Bar5 detection limit

def plot_STIS_contrast():
    fname = datapath+'HST_STIS.txt'
    a_STIS = ascii.read(fname)
    plt.plot(a_STIS['Rho(as)'],a_STIS['KLIP_Contr'],color=c_bbvis,\
        linewidth=lw1,label='0.5$\mu$m')
    
    x, y = a_STIS['Rho(as)'],a_STIS['KLIP_Contr']
    xy = position_text(x, y)

    plt.text(xy[0], xy[1], 'HST STIS',color=c_bbvis, fontsize=ccfs, va='bottom', ha='center')
    caption = extract_short_caption(fname)


#########################################################################
### ACS detection limit

def plot_ACS_contrast():
    fname = datapath+'HST_ACS.txt'
    a_ACS = ascii.read(fname)
    x, y = a_ACS['Rho(as)'],a_ACS['F606W_contr']
    xy = position_text(x, y)

    plt.plot(a_ACS['Rho(as)'],a_ACS['F606W_contr'],color=c_v,linewidth=lw1,label='0.6$\mu$m')
    plt.text(xy[0], xy[1], 'HST ACS',color=c_v, fontsize=ccfs, va='bottom', ha='center')
    caption = extract_short_caption(fname)


#########################################################################
### MagAO detection limit


def plot_MagAO_contrast():
    fname = datapath+'magao_ip_alphacen_5sigma.txt'
    a_MagAO_ip = ascii.read(fname)
    a_MagAO_ip['ip_Contrast'] = a_MagAO_ip['ip_contr_60min']
    plt.plot(a_MagAO_ip['Rho(as)'], a_MagAO_ip['ip_Contrast'], \
        color=c_band4,linewidth=lw1,label='0.8$\mu$m')
    x, y = a_MagAO_ip['Rho(as)'], a_MagAO_ip['ip_Contrast']
    xy = position_text(x, y)
    plt.text(xy[0], xy[1], 'MagAO',color=c_band4, fontsize=ccfs,  va='bottom', ha='center')

    fname = datapath+'magao_Ys_betapic_5sigma.txt'
    a_MagAO_ys = ascii.read(fname)
    a_MagAO_ys['Ys_Contrast'] = a_MagAO_ys['Ys_contr_60min']
    plt.plot(a_MagAO_ys['Rho(as)'], a_MagAO_ys['Ys_Contrast'], \
        color=c_yjh,linewidth=lw1,label='1-2$\mu$m')
    x, y = a_MagAO_ys['Rho(as)'], a_MagAO_ys['Ys_Contrast']
    xy = position_text(x, y)
    plt.text(xy[0], xy[1], 'MagAO',color=c_yjh, fontsize=ccfs,  va='bottom', ha='center')



#########################################################################
### SPHERE detection limit

def plot_SPHERE_contrast():
    fname = datapath+'SPHERE_Vigan.txt'
    a_SPHERE = ascii.read(fname)
    a_SPHERE['Contrast'] = 10**(-0.4*a_SPHERE['delta'])

    # manually split into IFS and IRDIS, at 0.7", as per documentation.
    plt.plot(a_SPHERE['Rho(as)'], a_SPHERE['Contrast'], color=c_yjh, linewidth=lw1, label='1-2$\mu$m')
    x, y = a_SPHERE['Rho(as)'], a_SPHERE['Contrast']
    xy = position_text(x, y)
    plt.text(xy[0], xy[1], 'SPHERE', color=c_k, fontsize=ccfs, va='bottom', ha='center')


#########################################################################
### GPI H-band

def plot_GPI_contrast():
    fname = datapath+'GPI_Sirius_Ltype.txt'
    a_GPI = ascii.read(fname)
    plt.plot(a_GPI['Rho(as)'],a_GPI['H_contr_60min_Ltype'],color=c_h,linewidth=lw1,label='1-2$\mu$m')
    x, y = a_GPI['Rho(as)'],a_GPI['H_contr_60min_Ltype']
    xy = position_text(x, y)
    plt.text(xy[0], xy[1], 'GPI', color=c_k, fontsize=ccfs, va='bottom', ha='center')

    
#########################################################################
### GRAVITY detection limit

def plot_GRAVITY_contrast():
    fname = datapath+'GRAVITY_pourre.txt'
    a_GRAV = ascii.read(fname)
    plt.plot(a_GRAV['Separation[mas]']/1e3,a_GRAV['K_band_contrast'],color=c_k,linewidth=lw1,label='2$\mu$m')
    x, y = a_GRAV['Separation[mas]']/1e3,a_GRAV['K_band_contrast']
    xy = position_text(x, y)
    plt.text(xy[0], xy[1], 'GRAVITY', color=c_k, fontsize=ccfs, va='bottom', ha='center')



def plot_KPIC_contrast():
    fname = datapath+'kpic.csv'
    a = ascii.read(fname)
    x, y = a['separation']/1e3, a['contrast']
    plt.plot(x, y, color=c_k, linewidth=lw1, label='1-2$\mu$m')
    xy = position_text(x, y)
    plt.text(xy[0],xy[1], 'KPIC', color=c_k, fontsize=ccfs, va='bottom', ha='center')


#########################################################################
### Roman


## predictions
if cfg['cons_mode'] is True:
    cons_mode = '_cons'
else:
    cons_mode = '_opti'
## Updating the figure's filename
cfgname = cfgname+cons_mode

def plot_Roman_img_contrast():
    fname = datapath+'Roman_pred_imaging_short'+cons_mode+'.txt'
    dat = ascii.read(fname)
    dat['lambda'].unit = u.nm
    dat['contr_snr5'] = dat['contr']*5/dat['SNR']
    dat['Rho(as)'] = dat['l/D'] * (dat['lambda'] / d_tel).decompose()*206265
    plt.plot(dat['Rho(as)'], dat['contr_snr5'], color=c_v, linewidth=lw1, label='')
    x, y = dat['Rho(as)'], dat['contr_snr5']
    xy = position_text(x, y)
    plt.text(xy[0], xy[1], 'Roman CorGI', color=c_v, fontsize=ccfs, va='bottom', ha='center')

def plot_Roman_spec_short_contrast():
    fname = datapath+'Roman_pred_spec_short'+cons_mode+'.txt'
    dat = ascii.read(fname)
    dat['lambda'].unit = u.nm
    dat['Rho(as)'] = dat['l/D'] * (dat['lambda'] / d_tel).decompose()*206265
    dat['contr_snr5'] = dat['contr']*5/dat['SNR']
    plt.plot(dat['Rho(as)'], dat['contr_snr5'], color=c_band3, linewidth=lw1, label='')
    x, y = dat['Rho(as)'], dat['contr_snr5']
    xy = position_text(x, y)
    plt.text(xy[0], xy[1], 'Roman CorGI', color=c_band3, fontsize=ccfs, va='bottom', ha='center')


def plot_Roman_wide_short_contrast():
    fname = datapath+'Roman_pred_wideFOVimaging_short'+cons_mode+'.txt'
    dat = ascii.read(fname)
    dat['lambda'].unit = u.nm
    dat['contr_snr5'] = dat['contr']*5/dat['SNR']
    dat['Rho(as)'] = dat['l/D'] * (dat['lambda'] / d_tel).decompose()*206265
    plt.plot(dat['Rho(as)'], dat['contr_snr5'], color=c_band4, linewidth=lw1, label='')
    x, y = dat['Rho(as)'], dat['contr_snr5']
    xy = position_text(x, y)
    plt.text(xy[0], xy[1], 'Roman CorGI', color=c_band4, fontsize=ccfs, va='bottom', ha='center')

## L1 requirement TTR 5

def plot_Roman_req_contrast():
    fname = datapath+'Roman_req_TTR5.txt'
    dat = ascii.read(fname)
    dat['lambda'].unit = u.nm
    dat['Rho(as)'] = dat['l/D'] * (dat['lambda'] / d_tel).decompose()*206265
    plt.plot(dat['Rho(as)'], dat['contr'], color=c_v, linewidth=lw1, label='')
    x, y = dat['Rho(as)'], dat['contr']
    xy = position_text(x, y)
    #plt.text(xy[0], xy[1], 'L1', color=c_band4, fontsize=ccfs, va='bottom', ha='center')

    caption = extract_short_caption(fname)



#########################################################################
###### -------------------- planets -------------------------  ##########
#########################################################################

#########################################################################
### Self luminous directly imaged planets

def plot_self_luminous_planets(H=True, B1=False, B3=False):
    fname = datapath+'DIplanets.txt'
    a_DI = ascii.read(fname)
    a_DI['B1_contr'] = 10**(a_DI['B1_delta']/-2.5)
    a_DI['B3_contr'] = 10**(a_DI['B3_delta']/-2.5)
    a_DI['H_contr'] = 10**(a_DI['H_delta']/-2.5)
    alpha_di = 1 # Windows machines have trouble with alpha<1 in PDF format
    caption = extract_short_caption(fname)

    if H:
        plt.scatter(a_DI['Rho(as)'],a_DI['H_contr'],color=c_h, edgecolor='k', \
            alpha=alpha_di, marker='s', s=cfg['di_markersize']-15, zorder=2,\
            label='Young Self-Luminous\nExoplanets')

    if B3:
        plt.scatter(a_DI['Rho(as)'],a_DI['B3_contr'],color=c_band3, edgecolor='k', \
            marker='d', alpha=alpha_di, s=cfg['di_markersize'], zorder=2, \
            label='self-luminous, Band 3 predicted')
        if not cfg['DI_B1_pred']:
            for ct, rho in enumerate(a_DI['Rho(as)']):
                plt.plot([rho,rho], [a_DI[ct]['B3_contr'], a_DI[ct]['H_contr']], \
                color='lightgray', linewidth=1, linestyle=':', zorder=1)

    if B1:
        for ct, rho in enumerate(a_DI['Rho(as)']):
            plt.plot([rho,rho], [a_DI[ct]['B1_contr'], a_DI[ct]['H_contr']], \
                color='lightgray', linewidth=1, linestyle=':', zorder=1)
        plt.scatter(a_DI['Rho(as)'],a_DI['B1_contr'],color=c_v, edgecolor='k', \
            marker='o', alpha=alpha_di, s=cfg['di_markersize'], zorder=2, \
            label='self-luminous, Band 1 predicted')




def plot_color_legend():

    if cfg['color_by_lambda'].lower() == 'full':
        c_v = 'dodgerblue'
        c_bbvis = 'cadetblue'
        c_band3 = 'goldenrod'
        c_band4 = 'orange'
        c_yjh = 'coral'
        c_k = 'firebrick'
        c_h   = 'red'
        c_pl = 'c'

        ax2 = plt.twinx()

        if cfg['ACS'] or cfg['req_img'] or cfg['old_L2req_img'] or cfg['DI_B1_pred']:
            ax2.plot([1,1],[1,1],color=c_v,linewidth=lw1+2, label='< 650 nm')
        if cfg['STIS']:
            ax2.plot([1,1],[1,1],color=c_bbvis,linewidth=lw1+2, label='broadband\nvisible')
        if cfg['old_L2req_spec'] or pred_spec or cfg['DI_B3_pred']:
            ax2.plot([1,1],[1,1],color=c_band3,linewidth=lw1+2, label='Band 3')
        if cfg['old_L2req_wide_img']:
            ax2.plot([1,1],[1,1],color=c_band4,linewidth=lw1+2, label='Band 4')
        if cfg['SPHERE']:
            ax2.plot([1,1],[1,1],color=c_yjh,linewidth=lw1+2, label='YJH-band')
        if cfg['GPI'] or cfg['NICMOS'] or cfg['DI_H']:
            ax2.plot([1,1],[1,1],color=c_h,linewidth=lw1+2, label='H-band')
        if cfg['SPHERE'] or cfg['NIRCAM'] or cfg['GRAVITY']:
            ax2.plot([1,1],[1,1],color=c_k,linewidth=lw1+2, label='K-band')

    elif cfg['color_by_lambda'].lower() == 'simple':
        c_v = 'dodgerblue'
        c_bbvis = c_v
        c_band3 = 'orange'
        c_band4 = 'tomato'
        c_yjh = 'firebrick'
        c_h = c_yjh
        c_k = c_yjh
        c_pl = 'c'

        ax2 = plt.twinx()
        if cfg['HABEX'] or cfg['ACS'] or cfg['STIS'] or cfg['DI_B1_pred']:
            ax2.plot([1,1],[1,1],color=c_v,linewidth=lw1+2, label='< 650 nm')
        if cfg['DI_B3_pred'] or cfg['old_L2req_spec'] or pred_spec:
            ax2.plot([1,1],[1,1],color=c_band3,linewidth=lw1+2, label='650 - 800nm')
        if cfg['old_L2req_wide_img'] or pred_wide_img:
            ax2.plot([1,1],[1,1],color=c_band4,linewidth=lw1+2, label='800 - 1000nm')
        if cfg['GPI'] or cfg['SPHERE'] or cfg['NIRCAM'] or cfg['NICMOS'] or cfg['DI_H'] or cfg['GRAVITY']:
            ax2.plot([1,1],[1,1],color=c_h,linewidth=lw1+2, label='> 1000 nm')


    elif cfg['color_by_lambda'].lower() == 'minimal':
        c_v = 'dodgerblue'
        c_bbvis = c_v
        c_band3 = c_v
        c_band4 = c_v
        c_yjh = 'firebrick'
        c_h = c_yjh
        c_k = c_yjh
        c_pl = 'c'

        ax2 = plt.twinx()
        if cfg['HABEX'] or cfg['ACS'] or cfg['STIS'] or cfg['DI_B1_pred'] or \
        cfg['DI_B3_pred'] or cfg['old_L2req_spec'] or pred_spec or  cfg['old_L2req_wide_img']:
            ax2.plot([1,1],[1,1],color=c_band4,linewidth=lw1+2, label='< 1000 nm')
        if cfg['GPI'] or cfg['SPHERE'] or cfg['NIRCAM'] or cfg['NICMOS'] or cfg['GRAVITY']:
            ax2.plot([1,1],[1,1],color=c_h,linewidth=lw1+2, label='> 1000 nm')


    elif cfg['color_by_lambda'].lower() == 'none':
        ccc = 'k'
        c_v = ccc
        c_bbvis = ccc
        c_band3 = ccc
        c_band4 = ccc
        c_yjh = ccc
        c_k = ccc
        c_h   = ccc
        c_pl = ccc

    else:
        raise Exception(cfg['color_by_lambda']+' is not a valid option for color_by_lambda (full/simple/none)')

    second_legend = ax2.legend(loc=thisloc, fontsize=cfg['legend_font_size'], title='Wavelength ($\lambda_0$)')
    second_legend.get_title().set_fontsize(8)
    #ax2.set_yscale('log')
    #ax2.set_xscale('log')
    ax2.set_yticklabels([])
    ax2.yaxis.set_ticks_position('none')

