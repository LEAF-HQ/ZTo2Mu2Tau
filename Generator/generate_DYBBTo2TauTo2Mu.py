#! /usr/bin/env python

import os, sys, math
from os.path import isfile, join
import subprocess
import time
import parse
from operator import itemgetter
import importlib
from utils import *
from functions import *
from constants import *

import ROOT
from ROOT import gROOT, gStyle, gPad, TLegend, TFile, TCanvas, Double, TF1, TH2D, TGraph, TGraph2D, TGraphAsymmErrors, TLine,\
                 kBlack, kRed, kBlue, kAzure, kCyan, kGreen, kGreen, kYellow, kOrange, kMagenta, kViolet,\
                 kSolid, kDashed, kDotted
from math import sqrt, log, floor, ceil
from array import array

from preferred_configurations import *
from tdrstyle_all import *
import tdrstyle_all as TDR

from CrossSectionRunner import *
from GensimRunner import *

processes = ['DYBBTo2Tau_2TauTo2Mu'] # (new-new) 1000*1000 events each

processes_xsec = processes

# PDF CMS standard (Paolo):
# 2016 LO:       263000
# 2016 NLO:      260000 325500
# 2017/18 CP5:   303600 (5f) or 325300 (5f with 2 add. weights, CMS-default) or 325500 (4f, CMS-default)
# 2017/18 CP2:   315200 (5f)

general_settings = {
'UL17':{
    'BWCUTOFF': 15,
    'PDF':      325500 # 4-f CMS recommendation for 17 and 18 samples with CP5
    },
'UL18':{
    'BWCUTOFF': 15,
    'PDF':      325500 # 4-f CMS recommendation for 17 and 18 samples with CP5
    }
}

individual_settings = [None]


tag = ''                # tags are auto-formatted to '_XXXX'
maxindex        = 1000   # Number of samples per configuration
nevents         = 1000  # Events per sample


username       = os.environ['USER']
arch_tag       = 'slc7_amd64_gcc700'
cmssw_tag_gp   = 'CMSSW_10_6_19'
cmssw_tag_sim  = 'CMSSW_10_6_28'
# campaign       = 'UL17'
campaign       = 'UL18'
sampletype     = 'DYBBTo2Tau'


workarea       = os.path.join('/work', username)
workdir_slurm  = os.path.join(workarea, 'workdir_slurm')
mgfolder       = os.path.join(workarea, cmssw_tag_sim, 'src', 'genproductions', 'bin', 'MadGraph5_aMCatNLO')
basefolder     = os.environ['LEAFPATH']
thisgenerator  = os.path.join(basefolder, 'ZTo2Mu2Tau', 'Generator')
generatorfolder= os.environ['GENERATORPATH']
gridpackfolder = os.path.join(thisgenerator, 'gridpacks', sampletype)
cardfolder     = os.path.join(thisgenerator, 'cards', sampletype)
crosssecfolder = os.path.join(thisgenerator, 'crosssections', sampletype)
psetfolder     = os.path.join(generatorfolder, 'PSets', campaign)
T2_director      = 'gsiftp://storage01.lcg.cscs.ch/'
T2_director_root = 'root://storage01.lcg.cscs.ch/'
T3_director      = 'root://t3dcachedb03.psi.ch/'
T2_path          = os.path.join('/pnfs/lcg.cscs.ch/cms/trivcat/store/user', username)
T3_path          = os.path.join('/pnfs/psi.ch/cms/trivcat/store/user', username)



folderstructure = {
'UL17':{
    'GENSIM': {
        'pset':            psetfolder+'/pset_tautomu_01_gensim.py',
        'cmsswtag':        cmssw_tag_sim,
        'jobnametag':      'gensim',
        'outfilenamebase': 'GENSIM',
        'pathtag':         'GENSIM/' + sampletype
    },
    'DR': {
        'pset':            psetfolder+'/pset_Summer20_03_dr.py',
        'cmsswtag':        cmssw_tag_sim,
        'jobnametag':      'dr',
        'outfilenamebase': 'DR',
        'infilepathtag':   'GENSIM/' + sampletype,
        'infilenamebase':  'GENSIM',
        'pathtag':         'DR/' + sampletype
    },
    'HLT': {
        'pset':            psetfolder+'/pset_04_hlt.py',
        'cmsswtag':        'CMSSW_9_4_14_UL_patch1',
        'jobnametag':      'hlt',
        'outfilenamebase': 'HLT',
        'infilepathtag':   'DR/' + sampletype,
        'infilenamebase':  'DR',
        'pathtag':         'HLT/' + sampletype
    },
    'AOD': {
        'pset':            psetfolder+'/pset_05_aod.py',
        'cmsswtag':        cmssw_tag_sim,
        'jobnametag':      'aod',
        'outfilenamebase': 'AOD',
        'infilepathtag':   'HLT/' + sampletype,
        'infilenamebase':  'HLT',
        'pathtag':         'AOD/' + sampletype
    },
    'MINIAODv2': {
        'pset':            psetfolder+'/pset_06_miniaodv2.py',
        'cmsswtag':        'CMSSW_10_6_20',
        'jobnametag':      'miniaod',
        'outfilenamebase': 'MINIAOD',
        'infilepathtag':   'AOD/' + sampletype,
        'infilenamebase':  'AOD',
        'pathtag':         'MINIAODv2/' + sampletype
    },
    'NANOAOD': {
        'pset':            psetfolder+'/pset_07_nanoaod.py',
        'cmsswtag':        cmssw_tag_sim,
        'jobnametag':      'nanoaod',
        'outfilenamebase': 'NANOAOD',
        'infilepathtag':   'MINIAODv2/' + sampletype,
        'infilenamebase':  'MINIAOD',
        'pathtag':         'NANOAOD/' + sampletype
    }
},
'UL18':{
    'GENSIM': {
        'pset':            psetfolder+'/pset_tautomu_01_gensim.py',
        'cmsswtag':        cmssw_tag_sim,
        'jobnametag':      'gensim',
        'outfilenamebase': 'GENSIM',
        'pathtag':         'GENSIM/%s/%s' % (campaign, sampletype)
    },
    'DR': {
        'pset':            psetfolder+'/pset_Summer20_03_dr.py',
        'cmsswtag':        cmssw_tag_sim,
        'jobnametag':      'dr',
        'outfilenamebase': 'DR',
        'infilepathtag':   'GENSIM/%s/%s' % (campaign, sampletype),
        'infilenamebase':  'GENSIM',
        'pathtag':         'DR/%s/%s' % (campaign, sampletype)
    },
    'HLT': {
        'pset':            psetfolder+'/pset_04_hlt.py',
        'cmsswtag':        'CMSSW_10_2_16_UL',
        'jobnametag':      'hlt',
        'outfilenamebase': 'HLT',
        'infilepathtag':   'DR/%s/%s' % (campaign, sampletype),
        'infilenamebase':  'DR',
        'pathtag':         'HLT/%s/%s' % (campaign, sampletype)
    },
    'AOD': {
        'pset':            psetfolder+'/pset_05_aod.py',
        'cmsswtag':        cmssw_tag_sim,
        'jobnametag':      'aod',
        'outfilenamebase': 'AOD',
        'infilepathtag':   'HLT/%s/%s' % (campaign, sampletype),
        'infilenamebase':  'HLT',
        'pathtag':         'AOD/%s/%s' % (campaign, sampletype)
    },
    'MINIAODv2': {
        'pset':            psetfolder+'/pset_06_miniaodv2.py',
        'cmsswtag':        'CMSSW_10_6_20',
        'jobnametag':      'miniaod',
        'outfilenamebase': 'MINIAOD',
        'infilepathtag':   'AOD/%s/%s' % (campaign, sampletype),
        'infilenamebase':  'AOD',
        'pathtag':         'MINIAODv2/%s/%s' % (campaign, sampletype)
    },
    'NANOAOD': {
        'pset':            psetfolder+'/pset_07_nanoaod.py',
        'cmsswtag':        cmssw_tag_sim,
        'jobnametag':      'nanoaod',
        'outfilenamebase': 'NANOAOD',
        'infilepathtag':   'MINIAODv2/%s/%s' % (campaign, sampletype),
        'infilenamebase':  'MINIAOD',
        'pathtag':         'NANOAOD/%s/%s' % (campaign, sampletype)
    }
}
}

ensureDirectory(workdir_slurm)


submit = True




EventGenerator = GensimRunner(processnames=processes, tag=tag, individual_settings=individual_settings, general_settings=general_settings[campaign], workdir_slurm=workdir_slurm, workarea=workarea, basefolder=basefolder, cardfolder=cardfolder, mgfolder=mgfolder, generatorfolder=generatorfolder, gridpackfolder=gridpackfolder, arch_tag=arch_tag, cmssw_tag_gp=cmssw_tag_gp, T2_director=T2_director, T2_path=T2_path, T2_director_root=T2_director_root, T3_director=T3_director, T3_path=T3_path, campaign=campaign, folderstructure=folderstructure[campaign], maxindex=maxindex, nevents=nevents, submit=submit)
# EventGenerator.ProduceCards()
# EventGenerator.SubmitGridpacks(runtime=(5,00,00))
EventGenerator.SubmitGenerationStep(generation_step='GENSIM', ncores=2, runtime=(3,00,00), mode='new')
# EventGenerator.SubmitGenerationStep(generation_step='GENSIM', ncores=2, runtime=(3,00,00), mode='resubmit')
# EventGenerator.SubmitGenerationStep(generation_step='GENSIM', ncores=8, runtime=(3,00,00), mode='resubmit')
# EventGenerator.SubmitGenerationStep(generation_step='DR', ncores=8, runtime=(3,00,00), mode='new')
# EventGenerator.SubmitGenerationStep(generation_step='DR', ncores=8, runtime=(3,00,00), mode='resubmit')
# EventGenerator.SubmitGenerationStep(generation_step='DR', ncores=8, runtime=(10,00,00), mode='resubmit')
# EventGenerator.SubmitGenerationStep(generation_step='HLT', ncores=8, runtime=(3,00,00), mode='new')
# EventGenerator.SubmitGenerationStep(generation_step='HLT', ncores=8, runtime=(3,00,00), mode='resubmit')
# EventGenerator.RemoveSamples(generation_step='DR')
# EventGenerator.SubmitGenerationStep(generation_step='AOD', ncores=4, runtime=(2,00,00), mode='new')
# EventGenerator.SubmitGenerationStep(generation_step='AOD', ncores=4, runtime=(2,00,00), mode='resubmit')
# EventGenerator.RemoveSamples(generation_step='HLT')
# EventGenerator.SubmitGenerationStep(generation_step='MINIAODv2', ncores=2, runtime=(1,00,00), mode='new')
# EventGenerator.SubmitGenerationStep(generation_step='MINIAODv2', ncores=2, runtime=(1,00,00), mode='resubmit')




#
