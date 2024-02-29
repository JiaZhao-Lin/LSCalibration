# %%
## Import
import ROOT
import numpy as np
import pandas as pd


# %%
## Configuration

post_fix_x = 'HIPhysicsRawPrime10_PromptRecoX1'
post_fix_y = 'HIPhysicsRawPrime10_PromptRecoY1'
inFileDir_x = f'../gather/outFiles/gathered_9206Prompt_PixVertex_{post_fix_x}.root'
inFileDir_y = f'../gather/outFiles/gathered_9206Prompt_PixVertex_{post_fix_y}.root'
csv_name_x = '../csv/outFiles/df_x_Sep_LSC_x_acq_selected.csv'
csv_name_y = '../csv/outFiles/df_y_Sep_LSC_y_acq_selected.csv'

# = Read files ================================================================
inFile_x = ROOT.TFile(inFileDir_x, 'READ')
inFile_y = ROOT.TFile(inFileDir_y, 'READ')
df_x = pd.read_csv(csv_name_x)
df_y = pd.read_csv(csv_name_y)

# = Create a dictionary to save the histograms ================================
hists_x = { key.GetName(): inFile_x.Get(key.GetName()) for key in inFile_x.GetListOfKeys() }
hists_y = { key.GetName(): inFile_y.Get(key.GetName()) for key in inFile_y.GetListOfKeys() }


# = Func =======================================================================
def draw_Latex(x, y, text, textFont=42, textSize=0.048, colorIndex=1, textAngle=0):

	latex = ROOT.TLatex(x, y, text )
	latex.SetNDC()
	latex.SetTextFont(textFont)
	latex.SetTextSize(textSize)
	latex.SetTextColor(colorIndex)
	latex.SetTextAngle(textAngle)
	latex.Draw("same")

	return latex

def draw_Latex_CMS_internal_header(x1=0.13, y1=0.94, x2=0.64, y2=0.94, textFont=42, textSize=0.05, colorIndex=1, textAngle=0):
	
	latex = draw_Latex(x1, y1, "#bf{CMS} #it{Internal}", textFont, textSize, colorIndex, textAngle)
	# latex_list.append( draw_Latex(x2, y2, "PbPb 1.52 nb^{-1} (5.02 TeV)", textFont, textSize, colorIndex, textAngle) )
	# latex_list.append( draw_Latex(x2, y2, "PbPb (5.36 TeV)", textFont, textSize, colorIndex, textAngle) )

	return latex



# %%
## Plotting

heap_list = list()
ROOT.gStyle.SetOptStat(0)

def plot_vertices(hists):
	means = list()
	means_error = list()

	nStep = 18

	for i in range(nStep):
		if i%9 == 0:
			c = ROOT.TCanvas(f'c{i}', f'c{i}', 1200, 900)
			c.Draw()
			c.Divide(3,3)
			heap_list.append(c)

		c.cd(i%9+1)
		hist_name = f'step{i}_ts_hist'
		hist = hists[hist_name].Clone()
		hist.SetTitle(';Vertex Position [#mum];Counts')
		heap_list.append(hist)
		hist.Draw()

		func_name = f'step{i}_ts_func'
		func = hists[func_name]
		func.SetLineWidth(1)
		func.Draw('same')

		heap_list.append( draw_Latex_CMS_internal_header() )
		heap_list.append( draw_Latex(0.15, 0.8, f'Step {i}') )
		heap_list.append( draw_Latex(0.15, 0.7, f'N = {hist.GetEntries()}') )
		heap_list.append( draw_Latex(0.15, 0.6, f'Mean = {hist.GetMean():.2f} #pm {hist.GetMeanError():.2f}') )
		heap_list.append( draw_Latex(0.15, 0.5, f'Fit = {func.GetParameter(1):.2f} #pm {func.GetParError(1):.2f}') )

		means.append( func.GetParameter(1) )
		means_error.append( func.GetParError(1) )

	steps = np.array([float(i) for i in range(nStep)])
	c1 = ROOT.TCanvas()
	ge = ROOT.TGraphErrors(len(means), steps, np.array(means), 0, np.array(means_error))
	heap_list.append(ge)
	ge.SetTitle(';Step;Vertex Position [#mum]')
	ge.SetMarkerStyle(20)
	ge.Draw('APE')
	c1.Draw()
	heap_list.append(c1)

	heap_list.append( draw_Latex_CMS_internal_header(x1=0.2) )

	return means, means_error

means_x, means_error_x = plot_vertices(hists_x)
means_y, means_error_y = plot_vertices(hists_y)


# %%

heap_list = list()
ROOT.gStyle.SetOptFit(0)

def plot_nominal( B1_pos, B2_pos , means, post_fix):

	#drop the first and last step
	B1_pos = B1_pos[1:-1]
	B2_pos = B2_pos[1:-1]
	print(B1_pos)
	print(B2_pos)

	B_nominal = (B1_pos + B2_pos)/2. * 1e3
	B_nominal_fwd = B_nominal[:9]
	B_nominal_bwd = B_nominal[9:]

	means_fwd = means[:9]
	means_bwd = means[9:]

	steps_fwd = np.array([float(i) for i in range(9)])
	steps_bwd = np.array([float(i) for i in range(9, 18)])

	c1 = ROOT.TCanvas()
	c1.Draw()

	ge_fwd = ROOT.TGraph(len(steps_fwd), B_nominal_fwd, np.array(means_fwd))
	ge_fwd.SetTitle(';Nominal Position [#mum];Vertex Position [#mum]')
	ge_fwd.SetMarkerStyle(20)
	ge_fwd.SetMarkerColor(2)
	ge_fwd.Draw('AP')

	ge_bwd = ROOT.TGraph(len(steps_bwd), B_nominal_bwd, np.array(means_bwd))
	ge_bwd.SetMarkerStyle(20)
	ge_bwd.SetMarkerColor(4)
	ge_bwd.Draw('SAMEP')

	f1_fwd = ROOT.TF1('f1_fwd', 'pol1', -100, 100)
	f1_fwd.SetLineColor(2)
	heap_list.append(f1_fwd)
	ge_fwd.Fit(f1_fwd, '')

	f1_bwd = ROOT.TF1('f1_bwd', 'pol1', -100, 100)
	f1_bwd.SetLineColor(4)
	heap_list.append(f1_bwd)
	ge_bwd.Fit(f1_bwd, '')

	heap_list.append( draw_Latex(0.15, 0.25, post_fix, textSize=0.04) )
	heap_list.append( draw_Latex(0.6, 0.80, f'Forward: {f1_fwd.GetParameter(0):.2f} + {f1_fwd.GetParameter(1):.2f}x', textSize=0.04, colorIndex=2) )
	heap_list.append( draw_Latex(0.6, 0.75, f'Backward: {f1_bwd.GetParameter(0):.2f} + {f1_bwd.GetParameter(1):.2f}x', textSize=0.04, colorIndex=4) )
	heap_list.append( draw_Latex_CMS_internal_header(x1=0.20))

	heap_list.append(ge_fwd)
	heap_list.append(ge_bwd)
	heap_list.append(c1)

plot_nominal(df_x['Set_Nominal_Displacement_B1_xingPlane'].values, df_x['Set_Nominal_Displacement_B2_xingPlane'].values, means_x, post_fix_x)
plot_nominal(df_y['Set_Nominal_Displacement_B1_sepPlane'].values, df_y['Set_Nominal_Displacement_B2_sepPlane'].values, means_y, post_fix_y)