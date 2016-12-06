import numpy
import argparse 							#argument parsing


parser = argparse.ArgumentParser(prog='Changes_stim.py',description='changes in stim',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sourceFile',help='file name ',type=str, required=True)
parser.add_argument('--outputFolder',help='Output folder',type=str, required=True)
args = parser.parse_args()
sourcefile = args.sourceFile
outputfile = args.outputFolder+'change_stim.txt'

datos = numpy.loadtxt(sourcefile)
nline = 0
outlist = []
for kiter in datos:
	if(kiter[1]-kiter[0]>335):
		print nline, kiter[1]-kiter[0], kiter[1],kiter[0]
		outlist.append([nline, kiter[1]-kiter[0], kiter[1],kiter[0]])
	nline += 1
numpy.savetxt(outputfile,outlist,fmt='%d')

