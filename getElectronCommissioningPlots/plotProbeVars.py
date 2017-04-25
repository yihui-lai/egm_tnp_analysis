import sys
sys.path.append("..")
import etc.inputs.tnpSampleDef as tnpSamples
import libPython.tnpClassUtils as tnpClasses
import ROOT as rt
from ROOT import gStyle
from ROOT import gROOT
import os

import CMS_lumi
from setTDRStyle import setTDRStyle

#treename = 'GsfElectronToSC/fitter_tree'
#treename = 'GsfElectronToPhoID/fitter_tree'
treename = 'GsfElectronToEleID/fitter_tree'

#gROOT.ProcessLine('.L CMS_lumi.C+')


CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "1 fb^{-1} (13 TeV)" 
iPos = 11
iPeriod = 0

def loopTree(sample, isMC):
    

    tree = rt.TChain(treename)
    for p in sample.path:
        print ' adding rootfile: ', p
        tree.Add(p)

    friendTreeName=''
    if not sample.puTree is None:
        print ' - Adding weight tree: %s from file %s ' % (sample.weight.split('.')[0], sample.puTree)
        friendTreeName = sample.weight.split('.')[0]
        tree.AddFriend(sample.weight.split('.')[0],sample.puTree)

    print "friendTreeName is ", friendTreeName

    histList = {}
    xTitle   = {}

#    region = ['EB','EE','all']
    region = ['EB','EE']

    histList['probe_sc_eta'] = rt.TH1F('probe_sc_eta','SC #eta',100,-2.5,2.5)
    histList['probe_sc_eta'].Sumw2()
    #b="this is %sand%s" %(a,c) 
    for reg in region:
        
        histList['probe_Ele_chIso_%s' %(reg)] = rt.TH1F('probe_Ele_chIso_%s' %(reg),'Charged isolation',20,0,5)
        histList['probe_Ele_chIso_%s' %(reg)].Sumw2()

        nbins=100
        xmin=0.005
        xmax=0.015

        if reg=='EE':
            nbins=100
            xmin=0.015
            xmax=0.035
                    
        histList['probe_Ele_sieie_%s' %(reg)] = rt.TH1F('probe_Ele_sieie_%s' %(reg),'#sigma(i#etai#eta)',nbins,xmin,xmax)
        histList['probe_Ele_sieie_%s' %(reg)].Sumw2()
        
        histList['probe_Ele_neuIso_%s' %(reg)] = rt.TH1F('probe_Ele_neuIso_%s' %(reg),'Neutral hadron isolation',20,0,5)
        histList['probe_Ele_neuIso_%s' %(reg)].Sumw2()
        
        histList['probe_Ele_phoIso_%s' %(reg)] = rt.TH1F('probe_Ele_phoIso_%s' %(reg),'Photon isolation',20,0,5)
        histList['probe_Ele_phoIso_%s' %(reg)].Sumw2()
        
        histList['probe_Ele_dEtaIn_%s' %(reg)] = rt.TH1F('probe_Ele_dEtaIn_%s' %(reg),'#Delta#eta_{in}',50,-0.04,0.04)
        histList['probe_Ele_dEtaIn_%s' %(reg)].Sumw2()
        
        histList['probe_Ele_dPhiIn_%s' %(reg)] = rt.TH1F('probe_Ele_dPhiIn_%s' %(reg),'#Delta#eta_{in}',50,-0.2,0.2)
        histList['probe_Ele_dPhiIn_%s' %(reg)].Sumw2()
        
        histList['probe_Ele_et_%s' %(reg)] = rt.TH1F('probe_Ele_et_%s' %(reg),'E_{T}',50,0,100)
        histList['probe_Ele_et_%s' %(reg)].Sumw2()

        ######xTitles
        xTitle['probe_Ele_chIso_%s' %(reg)] = 'Charged Hadron Isolation [GeV] (%s)' %(reg)
        xTitle['probe_Ele_sieie_%s' %(reg)] = '#sigma_{i#eta i#eta} (%s)' %(reg)
        xTitle['probe_Ele_neuIso_%s' %(reg)] = 'Neutral Hadron Isolation [GeV] (%s)' %(reg)
        xTitle['probe_Ele_phoIso_%s' %(reg)] = 'Photon Isolation [GeV] (%s)' %(reg)
        xTitle['probe_Ele_dEtaIn_%s' %(reg)] = '#Delta#eta_{in} (%s)' %(reg)
        xTitle['probe_Ele_dPhiIn_%s' %(reg)] = '#Delta#phi_{in} (%s)' %(reg)
        xTitle['probe_Ele_et_%s' %(reg)] = 'Probe E_{T} [GeV] (%s)' %(reg)
        
    xTitle['probe_sc_eta'] = 'Probe #eta_{sc}' 

    if(isMC):
        friendTree = tree.GetFriend(friendTreeName)

#    for ev in range(tree.GetEntries()):
    for ev in range(1,100):
        if (tree.GetEntry(ev) <= 0):
            raise Exception('TTree::GetEntry() failed')

        tag_Ele_pt          = tree.tag_Ele_pt
        tag_sc_abseta       = tree.tag_sc_abseta
        pair_mass           = tree.pair_mass
        probe_Ele_neuIso    = tree.probe_Ele_neuIso
        probe_Ele_phoIso    = tree.probe_Ele_phoIso
        probe_Ele_chIso     = tree.probe_Ele_chIso
        probe_Ele_pt        = tree.probe_Ele_pt
        probe_Ele_sieie     = tree.probe_Ele_sieie
        probe_Ele_dEtaIn    = tree.probe_Ele_dEtaIn
        probe_Ele_dPhiIn    = tree.probe_Ele_dPhiIn
        probe_Ele_et        = tree.probe_Ele_et
        probe_sc_eta        = tree.probe_sc_eta
        probe_sc_abseta     = tree.probe_sc_eta
        passingLoose80X     = tree.passingLoose80X

        ###PUweight:totWeight
        totWeight = 1


        if isMC==1:
            totWeight        = friendTree.totWeight
            
#        print 'totweight is ',totWeight

        combinedProbeIso   = (probe_Ele_neuIso+probe_Ele_phoIso+probe_Ele_chIso)/probe_Ele_pt

#        print "tag pt : mass : combinedIso ", tag_Ele_pt, " ",pair_mass, " ", combinedTagIso
        
        if not (tag_Ele_pt > 30 and tag_sc_abseta<2.1 and pair_mass>80 and pair_mass<100 and combinedProbeIso<0.1 and passingLoose80X==1 and probe_sc_abseta<2.5 and probe_Ele_et>20):
            continue
        
        #print "Selected the event "

        reg = 'EB'

        if(probe_sc_abseta > 1.479):
            reg = 'EE'
            
        histList['probe_sc_eta'].Fill(probe_sc_eta,totWeight)
        histList['probe_Ele_et_%s' %(reg)].Fill(probe_Ele_et,totWeight)
        histList['probe_Ele_sieie_%s' %(reg)].Fill(probe_Ele_sieie,totWeight)
        histList['probe_Ele_chIso_%s' %(reg)].Fill(probe_Ele_chIso,totWeight)
        histList['probe_Ele_neuIso_%s' %(reg)].Fill(probe_Ele_neuIso,totWeight)
        histList['probe_Ele_phoIso_%s' %(reg)].Fill(probe_Ele_phoIso,totWeight)
        histList['probe_Ele_dEtaIn_%s' %(reg)].Fill(probe_Ele_dEtaIn,totWeight)
        histList['probe_Ele_dPhiIn_%s' %(reg)].Fill(probe_Ele_dPhiIn,totWeight)

    for key in histList:
        print "key ,  integral ",key, histList[key].Integral()

    return histList,xTitle




######For drawing purpose
def setCanvas():
    
    W = 800
    H = 600
    H_ref = 600
    W_ref = 800
    T = 0.08*H_ref
    B = 0.12*H_ref
    L = 0.12*W_ref
    R = 0.04*W_ref
    
    setTDRStyle()
    c = rt.TCanvas('c','c',50,50,W,H)
    c.SetLeftMargin( L/W )
    c.SetRightMargin( R/W )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )
    
    
    
    pad1 = rt.TPad("pad1", "The pad 80% of the height",0.0,0.2,1.0,1.0,21)
    pad2 = rt.TPad("pad2", "The pad 20% of the height",0.0,0.001,1.0,0.25,22)
    
    pad1.SetFillColor(0)
    pad2.SetFillColor(0)
    
    pad2.SetTopMargin(0.02619172);
    pad2.SetBottomMargin(0.3102846);

    pad1.Draw()
    pad2.Draw()

    return c,pad1,pad2


def setLegend():
    leg = rt.TLegend(0.72,0.75,0.9194975,0.9154704)
    leg.SetBorderSize(0)
    leg.SetTextFont(62)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(1001)
    
    return leg


def getRatioPlot(histData,histMC, xTitle):
    hratio = histData.Clone()
        
    hratio.Divide(histData,histMC)
    hratio.GetXaxis().SetTitle(xTitle)
    
    hratio.GetXaxis().SetLabelSize(0.11)
    hratio.GetYaxis().SetLabelSize(0.11)
    hratio.GetYaxis().SetTitleSize(0.09)
    
    hratio.GetXaxis().SetLabelFont(42)
    hratio.GetXaxis().SetLabelSize(0.11)
    hratio.GetXaxis().SetTitleSize(0.035)
    hratio.GetXaxis().SetTitleFont(62)
    hratio.GetYaxis().SetTitle("#frac{Data}{MC}")
    hratio.GetYaxis().SetLabelFont(62)
    hratio.GetYaxis().SetLabelSize(0.11)
    hratio.GetYaxis().SetTitleSize(0.13)
    hratio.GetYaxis().SetTitleOffset(0.3)
    
    hratio.GetYaxis().SetNdivisions(205)
    hratio.GetXaxis().SetTitleSize(0.08)
    hratio.GetXaxis().SetLabelSize(0.13)
    hratio.GetXaxis().SetTitleSize(0.13)
    hratio.GetYaxis().SetLabelSize(0.12)
    hratio.GetYaxis().SetTitleSize(0.13)
    hratio.GetYaxis().SetTitleFont(62)
    hratio.GetZaxis().SetLabelFont(62)
    hratio.GetZaxis().SetLabelSize(0.035)
    hratio.GetZaxis().SetTitleSize(0.035)
    hratio.GetZaxis().SetTitleFont(62)
    
    hratio.GetYaxis().SetTitleOffset(0.3)
    hratio.GetYaxis().SetTitle("#frac{Data}{MC}")
    
    hratio.SetMaximum(2)
    hratio.SetMinimum(0)

    return hratio    



dataSamples = {
#    'runB'   :  tnpSamples.Moriond17_80X['data_Run2016B'].clone(),
#    'runC'   :  tnpSamples.Moriond17_80X['data_Run2016C'].clone(),
#    'runD'   :  tnpSamples.Moriond17_80X['data_Run2016D'].clone(),
    'runBCD'  :  tnpSamples.Moriond17_80X['data_Run2016B'].clone(),
}

mcSamples = {
    'runBCD'  : tnpSamples.Moriond17_80X['DY_madgraph'  ].clone(),  

}

########data
#dataSamples['runBCD'].add_sample(tnpSamples.Moriond17_80X['data_Run2016C'])
#dataSamples['runBCD'].add_sample(tnpSamples.Moriond17_80X['data_Run2016D'])
#########data

#mcSamples['runBCD'].set_puTree('eos/cms/store/group/phys_egamma/tnp/80X/pu/DY_madgraph_MCWinter17_rec_rec.pu.puTree.root')

mcSamples['runBCD'].set_puTree('root://eoscms.cern.ch//eos/cms/store/group/phys_egamma/tnp/80X/pu/DY_madgraph_MCWinter17_rec_rec.pu.puTree.root')
mcSamples['runBCD'].set_weight('weights_2016_runBCD.totWeight')
#mcSamples['runEF' ].set_weight('weights_2016_runEF.totWeight' )


epochs = [ 'runBCD' ]


for epoch in  epochs:

    ####loopTree(listOfSamples,isMC)

    histData,xTitle = loopTree(dataSamples[epoch],0) 
    histMC,xTitle   = loopTree(mcSamples[epoch],1)
    
    nE = len(histData)

    fileoutMC   = rt.TFile("histoMC_%s.root" %(epoch), "RECREATE")
    fileoutData = rt.TFile("histoData_%s.root" %(epoch), "RECREATE")

    os.system("mkdir -p plotsLinear"+epoch )
    os.system("mkdir -p plotsLog"+epoch )

    for key in histMC:

        ####save the hists first in a root file which can be used later###
        fileoutMC.cd()
        histMC[key].Write()
        
        fileoutData.cd()
        histData[key].Write()

        #####linear plots
        c,pad1,pad2 = setCanvas()


        histMC[key].SetFillColor(rt.kOrange-2)
        histMC[key].SetLineColor(rt.kOrange-2)
        
        histData[key].SetLineWidth(2)
        histData[key].SetMarkerStyle(20)
        histData[key].SetLineColor(1)

        print "Data integral ",histData[key].Integral()
        print "MC integral ",histMC[key].Integral()
        if not (histMC[key].Integral() == 0):
            scale = histData[key].Integral()/histMC[key].Integral()
        
        if(histMC[key].Integral() == 0):
               
           print "key ", key, " MC integral is 0 so not plotting"
           continue
           
        histMC[key].Scale(scale)
        
        pad1.cd()
        gStyle.SetOptStat(0)
        histMC[key].GetXaxis().SetLabelSize(0)
        histData[key].GetXaxis().SetLabelSize(0)
        histMC[key].GetYaxis().SetTitle('Events')
        histMC[key].Draw('hist')
        histData[key].Draw('same e')
        c.Update()

        #iPeriod = 2
        #iPos = 11
        CMS_lumi.CMS_lumi(pad1, iPeriod, iPos)
        pad1.Modified()
        pad1.Update()

        leg = setLegend()
        
        leg.AddEntry(histData[key],"Data","P")
        leg.AddEntry(histMC[key], "Z#rightarrow ee (MC)","f")
        leg.Draw()
        pad1.Update()

        tex = rt.TLatex(0.4,0.85,"Z#rightarrow ee")
        tex.SetNDC()
        tex.SetLineWidth(2)
#        tex.Draw()
#        pad1.Modified()


        pad2.cd()
        
        hratio = getRatioPlot(histData[key],histMC[key],xTitle[key])

        hratio.SetTitle('')
        hratio.Draw("E1")

        xlow  = histData[key].GetXaxis().GetXmin()
        xhigh = histData[key].GetXaxis().GetXmax()

        l = rt.TLine(xlow,1.,xhigh,1.)
        l.SetLineColor(2)
        l.SetLineStyle(2)
        l.SetLineWidth(2)
        l.Draw("sames")


        c.Modified()
        c.Update()
        
        pngname = "%s.png" %(key)
        print("png name is ",pngname)
        c.Print( "plotsLinear"+epoch+"/%s" %(pngname) )

        ######log plots
        c,pad1,pad2 = setCanvas()
        pad1.cd()
        pad1.SetLogy()
        histMC[key].SetMinimum(0.1)
        histData[key].SetMinimum(0.1)

        histMC[key].Draw('hist')
        histData[key].Draw('same e')
        c.Update()
        CMS_lumi.CMS_lumi(pad1, iPeriod, iPos)
        pad1.Modified()
        pad1.Update()

        leg.Draw()
        pad1.Update() 
        
        pad2.cd()
        hratio.Draw("E1")
        l.Draw("sames")

        c.Modified()
        c.Update()
        
        c.Print( "plotsLog"+epoch+"/%s" %(pngname) )

            
        ###### end of log plots
        

    fileoutMC.Write()
    fileoutData.Write()

    fileoutMC.Close()
    fileoutData.Close()
    
######end of the function        
