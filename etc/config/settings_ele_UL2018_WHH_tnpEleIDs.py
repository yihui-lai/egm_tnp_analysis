#############################################################
########## General settings
#############################################################
# flag to be Tested
#cutpass80 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.967083,0.929117,0.726311)
#cutpass90 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.913286,0.805013,0.358969)

# flag to be Tested
flags = {
#    'passingVeto94XV2'    : '(passingVeto94XV2   == 1)',
#    'passingLoose94XV2'   : '(passingLoose94XV2  == 1)',
#    'passingMedium94XV2'  : '(passingMedium94XV2 == 1)',
#    'passingTight94XV2'   : '(passingTight94XV2  == 1)',
#    'passingMVA94Xwp80noisoV2' : '(passingMVA94Xwp80noisoV2 == 1)',
#    'passingMVA94Xwp90noisoV2' : '(passingMVA94Xwp90noisoV2 == 1)',
#    'passingMVA94XwpLisoV2'    : '(passingMVA94XwpLisoV2 == 1)',
#    'passingMVA94XwpLnoisoV2'  : '(passingMVA94XwpLnoisoV2 == 1)',
#    'passingMVA94XwpHZZisoV2'  : '(passingMVA94XwpHZZisoV2 == 1)',

    #WHH trigger + ID
    'WHH_Trigger' : '(passHltEle32WPTightGsf == 1)',
    'passingWHH_ID_ISO': '(passingMVA94Xwp80isoV2==1 && el_relIso03_dB < 0.06)',
    #ZHH trigger + ID
    'ZHH_Trigger_leg1' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'ZHH_Trigger_leg2' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'passingZHH_ID_ISO': '(passingMVA94Xwp90isoV2==1 && el_relIso03_dB < 0.15)',
    }

baseOutDir = 'results/UL2018/tnpEleID_UL2018/'

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'tnpEleIDs'

samplesDef = {
    'data'   : tnpSamples.UL2018['data_Run2018A'].clone(),
    'mcNom'  : tnpSamples.UL2018['DY_madgraph'].clone(),
    'mcAlt'  : tnpSamples.UL2018['DY_amcatnloext'].clone(),
    'tagSel' : tnpSamples.UL2018['DY_madgraph'].clone(),
}

## can add data sample easily
samplesDef['data'].add_sample( tnpSamples.UL2018['data_Run2018B'] )
samplesDef['data'].add_sample( tnpSamples.UL2018['data_Run2018C'] )
samplesDef['data'].add_sample( tnpSamples.UL2018['data_Run2018D'] )

## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
samplesDef['data' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_madgraph')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 37') #canceled non trig MVA cut

## set MC weight, simple way (use tree weight) 
#weightName = 'totWeight'
#if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
#if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
#/afs/cern.ch/work/y/yilai/TNP/CMSSW_10_6_8/src/egm_tnp_analysis/PU/IDISO

## set MC weight, can use several pileup rw for different data taking periods
weightName = 'weights_2018_runABCD.totWeight'
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree('/afs/cern.ch/work/y/yilai/TNP/CMSSW_10_6_8/src/egm_tnp_analysis/PU/IDISO/UL18/DY_madgraph_ele.pu.puTree.root')
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree('/afs/cern.ch/work/y/yilai/TNP/CMSSW_10_6_8/src/egm_tnp_analysis/PU/IDISO/UL18/DY_amcatnloext_ele.pu.puTree.root')
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree('/afs/cern.ch/work/y/yilai/TNP/CMSSW_10_6_8/src/egm_tnp_analysis/PU/IDISO/UL18/DY_madgraph_ele.pu.puTree.root')


#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
   #{ 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
   #{ 'var' : 'el_pt' , 'type': 'float', 'bins': [10,20,35,50,100,200,500] },
   { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.2,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.2, 2.5] },
   { 'var' : 'el_pt' , 'type': 'float', 'bins': [20,25,30,35,40,50,70,100,500] },
    #{ 'var' : 'el_sc_eta' , 'type': 'float', 'bins':[-0.8, 0.0, 0.8]},
    #{ 'var' : 'el_pt' , 'type': 'float', 'bins': [19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,50,70,100,500]},

]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0'

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
#LS: we removed the met cuts cause JEC not ready for UL2018
#additionalCuts = { 
#    0 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    1 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    2 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    3 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    4 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    5 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    6 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    7 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    8 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    9 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45'
#}
additionalCuts = { 
    0 : 'tag_Ele_trigMVA > 0.92 ',
    1 : 'tag_Ele_trigMVA > 0.92 ',
    2 : 'tag_Ele_trigMVA > 0.92 ',
    3 : 'tag_Ele_trigMVA > 0.92 ',
    4 : 'tag_Ele_trigMVA > 0.92 ',
    5 : 'tag_Ele_trigMVA > 0.92 ',
    6 : 'tag_Ele_trigMVA > 0.92 ',
    7 : 'tag_Ele_trigMVA > 0.92 ',
    8 : 'tag_Ele_trigMVA > 0.92 ',
    9 : 'tag_Ele_trigMVA > 0.92 '
}

#### or remove any additional cut (default)
additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
    ]

#01
#tnpParNomFit = [
#    "meanP[0.049,-5.0,5.0]","sigmaP[1.3,0.5,5.0]",
#    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
#    "acmsP[60.,50.,100.]","betaP[0.027,-0.01,0.08]","gammaP[0.035, -2, 2]","peakP[90.0]",
#    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
#    ]
##08
#tnpParNomFit = [
#    "meanP[-1.0,-5.0,5.0]","sigmaP[2.0,0.5,5.0]",
#    "meanF[-0.2,-5.0,5.0]","sigmaF[2.7,0.5,5.0]",
#    "acmsP[60.,30.,90.]","betaP[0.01,-0.01,0.08]","gammaP[0.07, -2, 2]","peakP[90.0]",
#    "acmsF[60.,30.,90.]","betaF[0.01,-0.01,0.08]","gammaF[0.03, -2, 2]","peakF[90.0]",
#    ]
## 11
#tnpParNomFit = [
#    "meanP[-0.6,-5.0,5.0]","sigmaP[1.3,0.5,5.0]",
#    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
#    "acmsP[74.,50.,90.]","betaP[0.005,-0.03,0.08]","gammaP[0.04, -2, 2]","peakP[90.0]",
#    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
#    ]
#
#00
#tnpParNomFit = [
#    "meanP[-0.1,-5.0,5.0]","sigmaP[1.4,0.5,5.0]",
#    "meanF[-0.5,-5.0,5.0]","sigmaF[1.9,0.5,5.0]",
#    "acmsP[60.,50.,80.]","betaP[0.12,0.01,0.16]","gammaP[0.07, -4, 4]","peakP[90.0]",
#    "acmsF[60.,50.,80.]","betaF[0.025,0.01,0.08]","gammaF[0.05, -2, 2]","peakF[90.0]",
#    ]
#
##44
#tnpParNomFit = [
#    "meanP[0.05,-5.0,5.0]","sigmaP[1.3,0.5,5.0]",
#    "meanF[0.425,-5.0,5.0]","sigmaF[1.6,0.5,5.0]",
#    "acmsP[60.,50.,80.]","betaP[0.027,0.01,0.16]","gammaP[0.02, -4, 4]","peakP[90.0]",
#    "acmsF[60.,50.,80.]","betaF[0.025,0.01,0.08]","gammaF[0.05, -2, 2]","peakF[90.0]",
#    ]
##63
#tnpParNomFit = [
#    "meanP[-0.02,-5.0,5.0]","sigmaP[1.02,0.5,5.0]",
#    "meanF[-0.14,-5.0,5.0]","sigmaF[1.2,0.5,5.0]",
#    "acmsP[90.,45.,100.]","betaP[0.03,0.01,0.16]","gammaP[0.01, -4, 4]","peakP[90.0]",
#    "acmsF[90.,45.,100.]","betaF[0.05,0.01,0.12]","gammaF[0.02, -2, 2]","peakF[90.0]",
#    ]
##70
#tnpParNomFit = [
#    "meanP[0.1,-5.0,5.0]","sigmaP[0.98,0.5,5.0]",
#    "meanF[0.123,-5.0,5.0]","sigmaF[1.5,0.5,5.0]",
#    "acmsP[110.,105.,140.]","betaP[0.08,0.25,0.6]","gammaP[0.3, -4, 4]","peakP[90.0]",
#    "acmsF[80.,45.,90.]","betaF[0.00,0.0001,0.12]","gammaF[-0.02, -2, 2]","peakF[90.0]",
#    ]
##60
##tnpParNomFit = [
##    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
##    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
##    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
##    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
##    ]
##72
tnpParNomFit = [
    "meanP[-0.15,-5.0,5.0]","sigmaP[1.8,0.5,5.0]",
    "meanF[1.23,-5.0,5.0]","sigmaF[1.5,0.5,5.0]",
    "acmsP[60.,45.,90.]","betaP[0.17,0.01,0.26]","gammaP[1.9, -4, 4]","peakP[90.0]",
    "acmsF[60.,45.,90.]","betaF[0.01,0.0001,0.12]","gammaF[-0.02, -2, 2]","peakF[90.0]",
    ]
tnpParNomFit = [
    "meanP[-0.15,-5.0,5.0]","sigmaP[1.8,0.5,1.8]",
    "meanF[1.23,-5.0,5.0]","sigmaF[1.5,0.5,1.8]",
    "acmsP[60.,45.,70.]","betaP[0.17,0.01,0.26]","gammaP[1.9, -4, 4]","peakP[90.0]",
    "acmsF[60.,45.,70.]","betaF[0.01,0.0001,0.12]","gammaF[-0.02, -2, 2]","peakF[90.0]",
    ]

#68
#tnpParNomFit = [
#    "meanP[-0.2,-5.0,5.0]","sigmaP[1.4,0.5,5.0]",
#    "meanF[-0.4,-5.0,5.0]","sigmaF[1.5,0.5,5.0]",
#    "acmsP[80.,50.,90.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
#    "acmsF[50.,30.,80.]","betaF[0.01,-0.03,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
#    ]
#73
#tnpParNomFit = [
#    "meanP[0.2,-5.0,5.0]","sigmaP[1.5,0.5,5.0]",
#    "meanF[1.0,-5.0,5.0]","sigmaF[2.2,0.5,5.0]",
#    "acmsP[60.,45.,90.]","betaP[0.07,0.01,0.26]","gammaP[0.03, -4, 4]","peakP[90.0]",
#    "acmsF[60.,45.,90.]","betaF[0.01,0.0001,0.12]","gammaF[-0.01, -2, 2]","peakF[90.0]",
#    ]


tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]

# mc 60
#tnpParAltSigFit = [
#    "meanP[-1.5,-5.0,5.0]","sigmaP[0.7,0.1,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[5,-5,10]',"sigmaP_2[5,0.5,16.0]","sosP[1,0.5,5.0]",
#    "meanF[1.0,-5.0,5.0]","sigmaF[0.8,0.1,15.0]","alphaF[3.0,1.2,5.5]",'nF[4.5,-5,10]',"sigmaF_2[6.0,0.5,16.0]","sosF[1,0.5,5.0]",
#    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
#    ]
# mc 62
#tnpParAltSigFit = [
#    "meanP[-1.5,-5.0,5.0]","sigmaP[0.7,0.1,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[10,5,20]',"sigmaP_2[5,0.5,16.0]","sosP[1,0.5,5.0]",
#    "meanF[1.0,-5.0,5.0]","sigmaF[0.8,0.1,15.0]","alphaF[3.0,1.2,5.5]",'nF[1.4,-5,10]',"sigmaF_2[3.5,0.5,25.0]","sosF[1,0.5,5.0]",
#    "acmsP[60.,50.,95.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#    "acmsF[60.,50.,95.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
#    ]
## mc 63
#tnpParAltSigFit = [
#    "meanP[-1.5,-5.0,5.0]","sigmaP[0.7,0.1,6.0]","alphaP[2.0,0.2,13.5]" ,'nP[10.2,5,20]',"sigmaP_2[5,0.5,16.0]","sosP[1,0.5,5.0]",
#    "meanF[1.0,-5.0,5.0]","sigmaF[0.8,0.1,15.0]","alphaF[3.0,1.2,5.5]",'nF[1.4,-5,10]',"sigmaF_2[3.5,0.5,25.0]","sosF[1,0.5,5.0]",
#    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
#    ]
## mc 64
#tnpParAltSigFit = [
#    "meanP[-1.5,-5.0,5.0]","sigmaP[0.7,0.01,6.0]","alphaP[2.0,0.1,13.5]" ,'nP[10.2,5,20]',"sigmaP_2[5,0.5,16.0]","sosP[1,0.5,5.0]",
#    "meanF[-1.0,-5.0,5.0]","sigmaF[0.8,0.01,15.0]","alphaF[3.0,0.1,15.5]",'nF[1.4,-5,10]',"sigmaF_2[3.5,0.5,25.0]","sosF[1,0.5,5.0]",
#    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
#    ]
# 72
#tnpParAltSigFit = [
#    "meanP[-1.9,-5.0,5.0]","sigmaP[0.9,0.1,6.0]","alphaP[1.2,0.2,3.5]" ,'nP[5,-5,10]',"sigmaP_2[5,0.5,6.0]","sosP[1,0.5,5.0]",
#    "meanF[-0.8,-5.0,5.0]","sigmaF[0.7,0.1,5.0]","alphaF[3.0,0.2,5.5]",'nF[0,-5,10]',"sigmaF_2[6.0,0.5,6.0]","sosF[1,0.5,5.0]",
#    "acmsP[60.,50.,85.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#    "acmsF[60.,50.,85.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
#    ]
## 82
#tnpParAltSigFit = [
#    "meanP[-1.9,-5.0,5.0]","sigmaP[0.9,0.1,6.0]","alphaP[1.2,0.2,3.5]" ,'nP[5,-5,10]',"sigmaP_2[5,0.5,6.0]","sosP[1,0.5,5.0]",
#    "meanF[-0.8,-5.0,5.0]","sigmaF[0.9,0.1,5.0]","alphaF[1.2,0.2,3.5]",'nF[5,2,8]',"sigmaF_2[2.1,0.5,4.0]","sosF[1,0.5,5.0]",
#    "acmsP[60.,50.,85.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#    "acmsF[60.,50.,85.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
#    ]
#88
#tnpParAltSigFit = [
#    "meanP[0.4,0,5.0]","sigmaP[0.8,0.1,6.0]","alphaP[3.5,1.2,5.5]" ,'nP[5,-5,8]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
#    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
#    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
#    ]

# 39
tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,30.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]
#47
tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,30.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[80.,50.,85.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]

# 60
tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.01,6.0]","alphaP[3.0,1.2,4.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.01,3.0]","alphaF[1.6,1.2,4.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[0.1,0.,13.0]",
    "acmsP[60.,30.,75.]","betaP[0.004,0.001,0.006]","gammaP[-0.5, -2, -0.1]","peakP[90.0]",
    "acmsF[80.,50.,75.]","betaF[0.004,0.001,0.006]","gammaF[0.5, 0.1, 1]","peakF[90.0]",
    ]
tnpParAltSigFit = [
    "meanP[0.73,0.72,0.74]","sigmaP[1.2,1.19,1.21]","alphaP[1.47,1.4,2]" ,'nP[3,0.2,5]',"sigmaP_2[2.3,1,6.0]","sosP[0,0.,0.0]",
    "meanF[-1.16,-1.2,-1.1]","sigmaF[0.966,0.96,0.97]","alphaF[1.5,1.4,1.6]",'nF[3,0.2,5]',"sigmaF_2[6.0,5,6.0]","sosF[0.0,0.,0.0]",
    "acmsP[60.,30.,75.]","betaP[0.004,0.001,0.006]","gammaP[-0.5, -2, -0.1]","peakP[90.0]",
    "acmsF[80.,50.,75.]","betaF[0.004,0.001,0.006]","gammaF[0.5, 0.1, 1]","peakF[90.0]",
    ]
tnpParAltSigFit = [
    "meanP[0.72,0.71,0.73]","sigmaP[1.2,1.19,1.21]","alphaP[1.47,1.4,2]" ,'nP[3,0.2,5]',"sigmaP_2[2.3,1,6.0]","sosP[0,0.,0.0]",
    "meanF[-1.16,-1.2,-1.1]","sigmaF[0.966,0.96,0.97]","alphaF[1.5,1.4,1.6]",'nF[3,0.2,5]',"sigmaF_2[1.0,2,1.0]","sosF[0.0,0.,0.0]",
    "acmsP[90.,80.,105.]","betaP[0.04,0.001,0.6]","gammaP[0.1, 0.1, 0.1]","peakP[90.0]",
    "acmsF[90.,80.,95.]","betaF[0.04,0.001,0.6]","gammaF[0.05, 0.05, 0.05]","peakF[90.0]",
    ]
tnpParAltSigFit = [
    "meanP[-0.5,-0.5,-0.5]","sigmaP[2.3,2.3,2.3]","alphaP[1.75,1.75,1.75]" ,'nP[0.78,0.78,0.78]',"sigmaP_2[1.01,1.01,1.01]","sosP[1.11,1.11,1.11]",
    "meanF[-0.134,-0.135,-0.133]","sigmaF[1.95,1.95,1.95]","alphaF[1.49,1.49,1.49]",'nF[0.947,0.947,0.947]',"sigmaF_2[1.32,1.32,1.32]","sosF[1.195,1.195,1.195]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]
# 61
#tnpParAltSigFit = [
#    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.01,4.0]","alphaP[3.0,1.2,4.5]" ,'nP[1,-5,1]',"sigmaP_2[3,2,6.0]","sosP[1,0.01,5.0]",
#    "acmsP[60.,30.,75.]","betaP[0.004,0.001,0.006]","gammaP[-0.2, -5, -0.01]","peakP[90.0]",
#    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.01,3.0]","alphaF[1.6,1.2,4.5]",'nF[1,-5,1]',"sigmaF_2[2.0,0.5,6.0]","sosF[0.1,0.01,5.0]",
#    "acmsF[80.,50.,75.]","betaF[0.004,0.001,0.006]","gammaF[-0.2, -5, -0.01]","peakF[90.0]",
#    ]
##64
#tnpParAltSigFit = [
#    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.01,2.0]","alphaP[3.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,8.0]","sosP[1,0.1,5.0]",
#    "meanF[-0.0,-5.0,5.0]","sigmaF[0.7,0.01,2.0]","alphaF[1.6,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,8.0]","sosF[1,0.1,5.0]",
#    "acmsP[90.,30.,105.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.05, 1]","peakP[90.0]",
#    "acmsF[90.,50.,105.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.05, 1]","peakF[90.0]",
#    ]
##65
#tnpParAltSigFit = [
#    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.01,2.0]","alphaP[3.0,1.2,3.5]" ,'nP[1,-5,1]',"sigmaP_2[1.5,0.5,8.0]","sosP[1,0.1,5.0]",
#    "meanF[-0.0,-5.0,5.0]","sigmaF[0.7,0.01,2.0]","alphaF[1.6,1.2,3.5]",'nF[1,-5,1]',"sigmaF_2[2.0,0.5,8.0]","sosF[1,0.1,5.0]",
#    "acmsP[100.,96.,115.]","betaP[0.04,0.001,0.06]","gammaP[0.1, 0.01, 1]","peakP[90.0]",
#    "acmsF[100.,96.,115.]","betaF[0.04,0.001,0.06]","gammaF[0.1, 0.01, 1]","peakF[90.0]",
#    ]

tnpParAltSigFit = [
    "meanP[-2.0,-10,-2.0]","sigmaP[1.4,0.5,2]","alphaP[1.45,0.4,2]" ,'nP[-0.,-0.90,0.9]',"sigmaP_2[1.81,0.80,3.2]","sosP[0, -0.2,0.2]",
    "acmsP[60.,50.,75.]","betaP[0.004,0.001,0.006]","gammaP[0.2, 0.1, 3]","peakP[90.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.01,3.0]","alphaF[1.6,1.2,4.5]",'nF[0,-2,2]',"sigmaF_2[2.0,0.5,6.0]","sosF[0.1,0.2,0.2]",
    "acmsF[60.,50.,75.]","betaF[0.004,0.001,0.006]","gammaF[0.5, 0.1, 1]","peakF[90.0]",

    ]


tnpParAltSigFit_addGaus = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[1,0.7,6.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[1.5,0.5,6.0]","sosF[1,0.1,5.0]",
    "meanGF[95.0,90.0,100.0]","sigmaGF[15,5.0,125.0]",
    "acmsP[60.,50.,175.]","betaP[0.04,0.01,0.16]","gammaP[0.1, 0.00, 1]","peakP[90.0]",
    "acmsF[60.,50.,185.]","betaF[0.04,0.01,0.16]","gammaF[0.1, 0.00, 1]","peakF[90.0]",
    ]

# 03
tnpParAltSigFit_addGaus = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[1,0.7,6.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[1.5,0.5,6.0]","sosF[1,0.1,5.0]",
    "meanGF[68.0,60.0,75.0]","sigmaGF[15,5.0,125.0]",
    "acmsP[60.,50.,175.]","betaP[0.04,0.01,0.16]","gammaP[0.1, 0.00, 1]","peakP[90.0]",
    "acmsF[60.,50.,185.]","betaF[0.04,0.01,0.16]","gammaF[0.1, 0.00, 1]","peakF[90.0]",
    ]
# 36
tnpParAltSigFit_addGaus = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[1,0.7,6.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[1.5,0.5,6.0]","sosF[1,0.1,5.0]",
    "meanGF[80.0,78.0,88.0]","sigmaGF[15,5.0,125.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.16]","gammaP[0.1, 0.00, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.16]","gammaF[0.1, 0.00, 1]","peakF[90.0]",
    ]
#61
tnpParAltSigFit_addGaus = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[1,-5,1]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[1,0.7,6.0]","alphaF[2.0,1.2,3.5]",'nF[1,-5,1]',"sigmaF_2[1.5,0.5,6.0]","sosF[1,0.1,5.0]",
    "meanGF[104.0,96.0,120.0]","sigmaGF[10,5.0,125.0]",
    "acmsP[60.,50.,95.]","betaP[0.04,0.01,0.16]","gammaP[0.1, 0.00, 1]","peakP[90.0]",
    "acmsF[60.,50.,95.]","betaF[0.04,0.01,0.16]","gammaF[0.1, 0.00, 1]","peakF[90.0]",
    ]

#tnpParAltSigFit_addGaus = [
#    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,0.5,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
#    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,6.0]","alphaF[2.0,0.5,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
#    "meanGF[80.0,70.0,100.0]","sigmaGF[15,5.0,125.0]",
#    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#    "acmsF[60.,50.,85.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
#    ]
         
tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]
        
