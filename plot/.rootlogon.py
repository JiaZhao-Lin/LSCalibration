
def print_computer_info():
	import os

	# Get the computer name
	computer_name = os.uname().nodename

	# Get RAM and CPU information
	ram_info = os.popen('sysctl -n hw.memsize').read().strip()
	cpu_info = os.popen('sysctl -n machdep.cpu.brand_string').read().strip()

	print(f'{"The J Style Requested ":*<60}')
	print(f"Computer Name: {computer_name}")
	print(f"RAM: {int(ram_info) / (1024 ** 3):.2f} GB")
	print(f"CPU: {cpu_info}")
	print('*' * 60)

def globleStyle():
	import ROOT

	# ============================================================
	#  
	# Make graphs pretty
	#  
	# ============================================================
	
	ROOT.gROOT.SetBatch(True)

	ROOT.TGaxis.SetMaxDigits(3)

	font = 42

	ROOT.gStyle.SetOptFit(1111)
	ROOT.gStyle.SetOptTitle(0)
	ROOT.gStyle.SetOptDate(0)
	ROOT.gStyle.SetOptStat(0)
	ROOT.gStyle.SetStatFont(font)
	ROOT.gStyle.SetStatColor(10)
	ROOT.gStyle.SetStatH(0.18)
	ROOT.gStyle.SetStatW(0.18)
	# ROOT.gStyle.SetPalette(1,0)
	ROOT.gStyle.SetTextFont(font)
	ROOT.gStyle.SetTextSize(0.05)
	ROOT.gStyle.SetDrawBorder(0)

	# // set of X error bars and bar caps
	# ROOT.Style.SetErrorX(0)
	ROOT.gStyle.SetEndErrorSize(4)

	ROOT.gStyle.SetCanvasDefH(600)
	ROOT.gStyle.SetCanvasDefW(800)
	ROOT.gStyle.SetCanvasColor(10)
	ROOT.gStyle.SetCanvasBorderMode(0)
	ROOT.gStyle.SetCanvasBorderSize(2)
	ROOT.gStyle.SetPadColor(10)
	ROOT.gStyle.SetPadBorderMode(0)
	ROOT.gStyle.SetPadBorderSize(0)
	ROOT.gStyle.SetPadLeftMargin(0.12)
	ROOT.gStyle.SetPadRightMargin(0.05)
	ROOT.gStyle.SetPadTopMargin(0.08)
	ROOT.gStyle.SetPadBottomMargin(0.12)
	ROOT.gStyle.SetPadTickX(1)
	ROOT.gStyle.SetPadTickY(1)
	ROOT.gStyle.SetPadGridX(0)
	ROOT.gStyle.SetPadGridY(0)
	ROOT.gStyle.SetGridColor(18)
	ROOT.gStyle.SetFrameFillStyle(4000)
	ROOT.gStyle.SetFrameFillColor(10)
	ROOT.gStyle.SetFrameBorderSize(2)
	ROOT.gStyle.SetFrameBorderMode(0)
	ROOT.gStyle.SetFrameLineWidth(2)
	# ROOT.gStyle.SetFrameLineStyle(1)

	ROOT.gStyle.SetLegendBorderSize(0)
	ROOT.gStyle.SetLegendFillColor(10)
	ROOT.gStyle.SetLegendFont(font)
	ROOT.gStyle.SetLegendTextSize(0.05)

	ROOT.gStyle.SetLineColor(1)
	ROOT.gStyle.SetLineWidth(1) #affect almost everything, be careful to set it to be 
	ROOT.gStyle.SetHistLineColor(1)
	ROOT.gStyle.SetHistLineWidth(2)
	ROOT.gStyle.SetMarkerStyle(20)
	ROOT.gStyle.SetMarkerSize(1.)

	ROOT.gStyle.SetNdivisions(510,"xyz")
	ROOT.gStyle.SetTitleStyle(0)
	ROOT.gStyle.SetTitleBorderSize(0)
	ROOT.gStyle.SetTitleAlign(23) #adjust title position of histogram / graph etc
	ROOT.gStyle.SetTitleColor(1)
	ROOT.gStyle.SetTitleFont(font,"xyz")
	# ROOT.gStyle.SetTitleSize(0.056,"xyz")
	ROOT.gStyle.SetTitleSize(0.05,"xyz")
	ROOT.gStyle.SetTitleOffset(0.9,"x")
	ROOT.gStyle.SetTitleOffset(0.95,"yz")
	ROOT.gStyle.SetTickLength(0.02,"xyz")
	# ROOT.gStyle.SetLabelSize(0.045,"xyz")
	ROOT.gStyle.SetLabelSize(0.04,"xyz")
	ROOT.gStyle.SetLabelFont(font,"xyz")
	ROOT.gStyle.SetLabelOffset(0.008,"xyz")

print_computer_info()
globleStyle()