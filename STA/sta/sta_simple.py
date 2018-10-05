#!/usr/bin/env python
#============================================================
# STA FAST CHAIN
# SPIKE TRIGGERED AVERAGE (STA) ALGORITHM FAST VERSION
# Do STA for a list of Unit Cells.
# AASTUDILLO ABRIL 2014
# 29 ABRIL2014
#
# This script use as stimuli ensemble a mat file containing
# the stimuli in its true dimensions 20x20 px.
#============================================================

#============================================================
# Package import section:
#============================================================
import sys  # system lib
import os  # operative system lib
import random  # Random number methods
import time         # System timer options
import argparse  # A|rgument parsing
from multiprocessing import Pool, freeze_support  # Parallel powa!

import matplotlib  # Graph and plot library
matplotlib.use("Agg")  # For save images without show it in windows (for server use)
import matplotlib.cm as cm        # plot lib
import matplotlib.pyplot as plt       # plot lib (for figures)

#-----------------------------------------------------------
# Methods, Signal processing, etc:
#-----------------------------------------------------------
from scipy.io import loadmat, savemat
import scipy.misc as scim  # Scientific python package for image basic process
import numpy as np  # Numerical methods lib

#=============================================
# Inputs
#=============================================
parser = argparse.ArgumentParser(
    prog='sta.py',
    description='Performs STA from a stimuli ensemble',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
parser.add_argument(
    '--startUnit',
    help='From which units should be processed',
    type=int,
    default=0,
    required=False,
    )
parser.add_argument(
    '--endUnit',
    help='Up to which units should be processed',
    type=int,
    default=2,
    required=False,
    )
parser.add_argument(
    '--outputFolder',
    help='Output folder',
    type=str,
    default='.',
    required=False,
    )
parser.add_argument(
    '--sourceFolder',
    help='Folder with the files containing the timestamps for each unit',
    type=str,
    default='.',
    required=True,
    )
parser.add_argument(
    '--syncFile',
    help='SET THE NAME OF THE STIMULUS SYNCHRONY ANALYSIS FILE \
    IT CONTAINS THEINITIAL AND FINAL TIME STAMPS OF EACH FRAME',
    type=str,
    default='.',
    required=True,
    )
parser.add_argument(
    '--samplingRate',
    help='ADQUISITION SAMPLING RATE FOR THE RECORDS',
    type=np.float,
    default=20000.0,
    required=False,
    )
parser.add_argument(
    '--preFrame',
    help='NUMBER OF FRAMES BEFORE AND AFTER A SPIKE TO ANALISE',
    type=int,
    default=30,
    required=False,
    )
parser.add_argument(
    '--postFrame',
    help='number of frames posterior to each spike for STA windows',
    type=int,
    default=0,
    required=False,
    )
parser.add_argument(
    '--stimMini',
    help='Stimuli matrix from *.mat or *.hdf5',
    type=str,
    required=True,
    )
parser.add_argument(
    '--numberProcesses',
    help='Number of processes to spawn',
    type=int,
    default=1,
    choices=[1, 2, 3, 4, 5, 6],
    required=False,
    )
args = parser.parse_args()


# =============================================
# GET SPIKE TIME FILE NAMES
# =============================================

# Source folder of the files with the timestamps
sourceFolder = args.sourceFolder
# Check for trailing / on the folder
if sourceFolder[-1] != '/':
    sourceFolder+='/'

# FOLDER NAME TO SAVE RESULTS
outputFolder = args.outputFolder
if outputFolder[-1] != '/':
    outputFolder += '/'

# SET THE NAME OF THE STIMULUS SYNCHRONY ANALYSIS FILE
# IT CONTAINS THE INITIAL AND FINAL TIME STAMPS OF EACH FRAME
syncFile = args.syncFile

# SPIKE TIME STAMPS FOLDER FOR LOAD SPIKE TRAINS
timefolder = sourceFolder

# SET THE ADQUISITION SAMPLING RATE OF THE RECORDS
samplingRate = args.samplingRate  # Hz

# SET THE NUMBER OF FRAMES BEFORE AND AFTER A SPIKE TO ANALIZE:
# number of frames previous to each spike for STA windows
preFrame = args.preFrame
# number of frames posterior to each spike for STA windows
postFrame = args.postFrame

inicio_fin_frame = np.loadtxt(syncFile).T
vector_inicio_frame = inicio_fin_frame[0]
vector_fin_frame = inicio_fin_frame[1]
start_sync = vector_inicio_frame[0]
end_sync = vector_fin_frame[-1]
bins_stim = np.concatenate((vector_inicio_frame, vector_fin_frame[-1:]))
lenSyncFile = len(vector_fin_frame)

# load image mat file stim_mini
stimMini = args.stimMini
if stimMini.lower().endswith('.mat'):
    try:
        ensemble = loadmat(stimMini)
        estimulos = ensemble['stim']
    except NotImplementedError:
        import h5py
        with h5py.File(stimMini, 'r') as hf:
            shape_nstim = (hf['stim'].shape)
            estimulos = np.zeros(shape_nstim, dtype=np.float)
            hf['stim'].read_direct(estimulos, np.s_[...])
        estimulos = np.transpose(estimulos, np.arange(estimulos.ndim)[::-1])
    except ValueError as verror:
        verror('There are problems with {} file'.format(stimMini))
    xSize, ySize, nchannels, lenEstimulos = estimulos.shape
    estim = np.zeros((xSize, ySize, lenEstimulos), dtype=np.float)
    for ke in range(lenEstimulos):
        rgb = estimulos[:, :, :, ke]
        gray = np.dot(rgb[..., :3], [0.299, 0.587, 0.144])
        estim[:, :, ke] = gray
    estim = np.asarray(estim)
elif stimMini.lower().endswith('.hdf5'):
    import h5py
    with h5py.File(stimMini, 'r') as hf:
        estimulos = np.zeros(hf['checkerboard'].shape, dtype=np.float)
        estimulos = hf['checkerboard'][...]
    estimulos = np.transpose(estimulos, (2, 3, 1, 0))
    xSize, ySize, nchannels, lenEstimulos = estimulos.shape
    estim = np.zeros((xSize, ySize, lenEstimulos), dtype=np.float)
    for ke in range(lenEstimulos):
        rgb = estimulos[:, :, :, ke]
        gray = np.dot(rgb[..., :3], [0.299, 0.587, 0.144])
        estim[:, :, ke] = gray
    estim = np.asarray(estim)
else:
    raise ValueError('It necesary load a stim File')

xSize, ySize, lenEstimulos = estim.shape
estim_min, estim_max = estim.min(), estim.max()
estim = ((estim - estim_min) / ((estim_max - estim_min) / 2) - 1)
print 'stim min : {} stom max: {}'.format(estim.min(), estim.max())
if lenEstimulos < lenSyncFile:
    lenSyncFile = lenEstimulos


meanimagearray = np.add.reduce(estim, axis=2) // (1.0*100000)

startUnit = args.startUnit
endUnit = args.endUnit

# Dumb validation about limits
if startUnit < 0:
    assert ValueError('startUnit < 0')
if startUnit > endUnit:
    assert ValueError('startUnit can not be lesser than endUnit')

# vectores units y caracterizacion provienen de la tabla excel
# pero como no la tenemos...la primera vez se deben ignorar
unit_names = []
for unitFile in os.listdir(sourceFolder):
        unit_names.append(unitFile.rsplit('.', 1)[0])
recoveredUnits = len(unit_names)
if endUnit > recoveredUnits:
    endUnit = recoveredUnits

try:
    os.mkdir(outputFolder)
except OSError:
    pass


def compute_sta(valid_frames, spike_in_frames):
    '''Complute the spike trigger average for a unit.

    Parameters
    ----------
    valid_frames : array
        Index list of valid frame in stim
    spike_in_frames : array
        List of amoung of spikes in each valid frame
    '''
    sta = np.zeros((xSize, ySize, preFrame+postFrame))
    # Valid frames consider itself as reference
    for kframe, nspikes in zip(valid_frames+1, spike_in_frames):
        sta += nspikes*estim[:, :, kframe-preFrame:kframe+postFrame]
    sta /= spike_in_frames.sum()
    return sta


def pool_sta(args):
    start_unit, end_unit = args
    for kunit in range(start_unit, end_unit):
        unit_name = unit_names[kunit]
        print 'Analysing Unit ', unit_name
        # Get spike time stamps from file
        rastercelulatxtfile = timefolder + unit_name + '.txt'
        timestamps = np.loadtxt(rastercelulatxtfile) * samplingRate

        timestamp_filter = timestamps > start_sync
        vector_spikes = timestamps[timestamp_filter]
        timestamp_filter = vector_spikes < end_sync
        vector_spikes = vector_spikes[timestamp_filter]
        nspikes_in_frame, _ = np.histogram(vector_spikes, bins=bins_stim)
        valid_frames = np.where(nspikes_in_frame > 0)[0]
        filter_valid_fame = (valid_frames >= preFrame) & \
                            (valid_frames < lenEstimulos - postFrame)
        valid_frames = valid_frames[filter_valid_fame]

        if valid_frames.any():
            sta_array = compute_sta(valid_frames,
                                    nspikes_in_frame[valid_frames]
                                    )
            unit_output_folder = str(unit_name)+'_lineal/'
            try:
                os.mkdir(outputFolder+unit_output_folder)
            except OSError:
                pass
            finalfolder_lin = outputFolder+unit_output_folder
            output_file = finalfolder_lin+'sta_array_'+str(unit_name)+'.mat'
            savemat(output_file,
                    mdict={'STA_array': sta_array},
                    oned_as='column',
                    )
            plot_sta(sta_array, unit_name)


def plot_sta(sta_array, unit_name):
    nrow = (preFrame+postFrame)/6+1
    fig = plt.figure(figsize=(6, nrow))
    max_abs_amp = np.max([np.abs(sta_array.max()), np.abs(sta_array.max())])
    v_min, v_max = -max_abs_amp, max_abs_amp
    for kplot in range(preFrame+postFrame):
        ax = fig.add_subplot(nrow, 6, kplot+1)
        # ax.pcolor(sta_array[:,:,kplot],vmin = 0,vmax = 255, cmap=cm.plasma)
        ax.pcolor(sta_array[:, :, kplot], vmin=v_min, vmax=v_max, cmap='jet')
        ax.set_xlim([0, xSize])
        ax.set_ylim([0, ySize])
        ax.set_aspect(1)
        # ax.axis('off')
    output_name_sta = '{}STA-{}_.png'.format(outputFolder, unit_name)
    plt.savefig(output_name_sta, bbox_inches='tight')
    plt.close()


def main():
    number_units = endUnit-startUnit
    number_processes = args.numberProcesses
    units_per_process = number_units//number_processes+1
    p = Pool(processes=number_processes)

    range_for_processes = []
    for kstart in range(startUnit, endUnit, units_per_process):
        if kstart+units_per_process < endUnit:
            range_for_processes.append((kstart, kstart+units_per_process))
        else:
            range_for_processes.append((kstart, endUnit))
    print range_for_processes
    p.map(pool_sta, range_for_processes)


if __name__=="__main__":
    freeze_support()
    main()
