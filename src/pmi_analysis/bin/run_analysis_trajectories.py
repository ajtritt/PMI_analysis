import argparse

import numpy as np
import pandas as pd
import math
import glob
import sys
import os

from pmi_analysis.analysis_trajectories import *

#################################
########### MAIN ################
#################################
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('top_dir', help='the IMP output directory')
    parser.add_argument('-a', '--analys_dir', default='analys',
                        help='the subdirectory in top_dir to save analysis output to')
    parser.add_argument('-p', '--nproc', type=int, help='the number of processes to use', default=1)

    args = parser.parse_args()

    nproc = args.nproc
    top_dir =  args.top_dir
    analys_dir = os.path.join(top_dir, args.analys_dir)

    # Check if analysis dir exists
    if not os.path.isdir(analys_dir):
        os.makedirs(analys_dir)

    # How are the trajectories dir names
    dir_head = 'run_'
    out_dirs = glob.glob(os.path.join(top_dir, dir_head + '*', 'output'))

    ################################
    # Get and organize fields for
    # analysis
    ################################
    # Read the total score, plot
    # and check for score convengence

    # Load module
    AT = AnalysisTrajectories(out_dirs,
                              dir_name=dir_head,
                              analysis_dir = analys_dir,
                              nproc=nproc)

    # Define restraints to analyze
    # XLs_cutoffs = {'DSSO':30.0}
    # AT.set_analyze_XLs_restraint(XLs_cutoffs = XLs_cutoffs)
    AT.set_analyze_Connectivity_restraint()
    AT.set_analyze_Excluded_volume_restraint()

    # Read stat files
    AT.read_stat_files()
    AT.write_models_info()
    AT.get_psi_stats()

    #AT.hdbscan_clustering(['EV_sum', 'XLs_sum'])
    AT.hdbscan_clustering(['EV_sum'])
    #AT.summarize_XLs_info()
