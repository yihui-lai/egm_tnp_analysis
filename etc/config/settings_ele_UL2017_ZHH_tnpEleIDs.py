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
    'WHH_Trigger' : '(passHltEle32DoubleEGWPTightGsf == 1 && passEGL1SingleEGOr==1)', #emulate HLT_Ele32_WPTight_Gsf 
    'passingWHH_ID_ISO': '(passingMVA94Xwp80isoV2==1 && el_relIso03_dB < 0.06)',
    #ZHH trigger + ID
    'ZHH_Trigger_leg1' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)', 
    'ZHH_Trigger_leg2' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'passingZHH_ID_ISO': '(passingMVA94Xwp90isoV2==1 && el_relIso03_dB < 0.15)',
    }

baseOutDir = 'results/UL2017/tnpEleID_UL2017/'

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'tnpEleIDs'

samplesDef = {
    'data'   : tnpSamples.UL2017['data_Run2017B'].clone(),
    'mcNom'  : tnpSamples.UL2017['DY_madgraph'].clone(),
    'mcAlt'  : tnpSamples.UL2017['DY_amcatnloext'].clone(),
    'tagSel' : tnpSamples.UL2017['DY_madgraph'].clone(),
}

## can add data sample easily
samplesDef['data'].add_sample( tnpSamples.UL2017['data_Run2017C'] )
samplesDef['data'].add_sample( tnpSamples.UL2017['data_Run2017D'] )
samplesDef['data'].add_sample( tnpSamples.UL2017['data_Run2017E'] )
samplesDef['data'].add_sample( tnpSamples.UL2017['data_Run2017F'] )

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

## set MC weight, can use several pileup rw for different data taking periods
weightName = 'weights_2017_runBCDEF.totWeight'
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree('/afs/cern.ch/work/y/yilai/TNP/CMSSW_10_6_8/src/egm_tnp_analysis/PU/IDISO/UL17/DY_madgraph_ele.pu.puTree.root')
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree('/afs/cern.ch/work/y/yilai/TNP/CMSSW_10_6_8/src/egm_tnp_analysis/PU/IDISO/UL17/DY_amcatnloext_ele.pu.puTree.root')
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree('/afs/cern.ch/work/y/yilai/TNP/CMSSW_10_6_8/src/egm_tnp_analysis/PU/IDISO/UL17/DY_madgraph_ele.pu.puTree.root')


#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
   { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.2,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.2, 2.5] },
   { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 15, 20, 25,30,35,40,50,70,100,500] },

]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0'

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
#LS: we removed the met cuts cause JEC not ready for UL2017
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

# 4
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-1.0,-5.0,5.0]","sigmaF[2.9,0.5,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,20.,80.]","betaF[0.035,0.01,0.08]","gammaF[0.03, -2, 2]","peakF[90.0]",
    ]



tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]

# 15
tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,0.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.1,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,20.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,20.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]
#16
tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,0.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.1,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,20.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,40.,75.]","betaF[0.04,0.001,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]
#67
tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.1,6.0]","alphaF[2.0,0.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.1,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,20.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,40.,75.]","betaF[0.04,0.001,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]

#84
tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,0.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[2.2,2,10.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.1,6.0]","alphaF[2.0,0.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.2,2,10.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,20.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,40.,75.]","betaF[0.04,0.001,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]


tnpParAltSigFit_addGaus = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[1,0.7,6.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[1.5,0.5,6.0]","sosF[1,0.1,5.0]",
    "meanGF[95.0,90.0,100.0]","sigmaGF[15,5.0,125.0]",
    "acmsP[60.,50.,175.]","betaP[0.04,0.01,0.16]","gammaP[0.1, 0.00, 1]","peakP[90.0]",
    "acmsF[60.,50.,185.]","betaF[0.04,0.01,0.16]","gammaF[0.1, 0.00, 1]","peakF[90.0]",
    ]

#51
tnpParAltSigFit_addGaus = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[1.2,0.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[1,0.7,6.0]","alphaF[1.2,0.2,3.5]",'nF[3,-5,5]',"sigmaF_2[1.5,0.5,6.0]","sosF[1,0.1,5.0]",
    "meanGF[80.0,50.0,90.0]","sigmaGF[15,5.0,125.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.16]","gammaP[0.1, 0.00, 1]","peakP[90.0]",
    "acmsF[60.,20.,85.]","betaF[0.04,0.01,0.16]","gammaF[0.1, 0.00, 1]","peakF[90.0]",
    ]

#51
tnpParAltSigFit_addGaus = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[1.2,0.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[1,0.7,6.0]","alphaF[1.2,0.2,3.5]",'nF[3,-5,5]',"sigmaF_2[1.5,0.5,6.0]","sosF[1,0.1,5.0]",
    "meanGF[80.0,50.0,90.0]","sigmaGF[15,5.0,125.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.16]","gammaP[0.1, 0.00, 1]","peakP[90.0]",
    "acmsF[60.,20.,85.]","betaF[0.04,0.01,0.16]","gammaF[0.1, 0.00, 1]","peakF[90.0]",
    ]


#87
tnpParAltSigFit_addGaus = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.1,4.0]","alphaP[1.2,0.2,3.5]" ,'nP[3,-5,10]',"sigmaP_2[1.5,0.5,15.0]","sosP[1,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[1,0.7,6.0]","alphaF[1.2,0.2,3.5]",'nF[3,-5,5]',"sigmaF_2[1.5,0.5,6.0]","sosF[1,0.1,5.0]",
    "meanGF[105.0,100.0,130.0]","sigmaGF[15,5.0,125.0]",
    "acmsP[60.,50.,105.]","betaP[0.04,0.01,0.16]","gammaP[0.1, 0.00, 1]","peakP[90.0]",
    "acmsF[60.,20.,105.]","betaF[0.04,0.01,0.16]","gammaF[0.1, 0.00, 1]","peakF[90.0]",
    ]
#95
tnpParAltSigFit_addGaus = [
    "meanP[1.4,-5.0,5.0]","sigmaP[1.8,0.7,6.0]","alphaP[2.2,0.2,3.5]" ,'nP[5,-5,15]',"sigmaP_2[2.8,0.5,10.0]","sosP[1,0.5,5.0]",
    "meanF[-0.9,-5.0,5.0]","sigmaF[1.5,0.1,6.0]","alphaF[1.1,0.2,3.5]",'nF[5,-5,15]',"sigmaF_2[5.9,0.5,10.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,20.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,40.,75.]","betaF[0.04,0.001,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    "meanGF[105.0,100.0,130.0]","sigmaGF[15,5.0,125.0]",
    ]


#69
#tnpParAltSigFit_addGaus = [
#    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[1.2,0.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.1,5.0]",
#    "meanF[-0.0,-5.0,5.0]","sigmaF[1,0.7,6.0]","alphaF[1.2,0.2,3.5]",'nF[3,-5,5]',"sigmaF_2[1.5,0.5,6.0]","sosF[1,0.1,5.0]",
#    "meanGF[80.0,70.0,90.0]","sigmaGF[15,5.0,125.0]",
#    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.16]","gammaP[0.1, 0.00, 1]","peakP[90.0]",
#    "acmsF[60.,20.,85.]","betaF[0.04,0.01,0.16]","gammaF[0.1, 0.00, 1]","peakF[90.0]",
#    ]


tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]
        
