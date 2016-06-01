#!/usr/bin/python
######################################################################
# Name:         ALaDyn_plot_utilities_Energy_Density.py
# Author:       F.Mira
# Date:			2016-05-25
# Purpose:      it is a module of: ALaDyn_plot_sections - plots energy density
# Source:       python
#####################################################################

### loading shell commands
import os, os.path, glob, sys, shutil, time, datetime
import numpy as np
from pylab import *
from matplotlib import colors, ticker, cm
###>>>
# home_path = os.path.expanduser('~')
# sys.path.append(os.path.join(home_path,'Codes/ALaDyn_Code/tools-ALaDyn/ALaDyn_Pythons'))
###>>>
from read_ALaDyn_bin import *
from ALaDyn_plot_utilities_1 import *
### --- ###






#- plot Sections
def plot_energy_density_sections(path,frame,EneDen_min,EneDen_max,isolines,celltocut,sliceposition_x,sliceposition_y,sliceposition_z,magnification_fig,savedata):
	s='%2.2i'%frame 				#conversion to 2-character-long-string

	
	
	file_name = 'Elenout'+s+'.bin'
	matrix3,  x,y,z = read_ALaDyn_bin(path,file_name,'grid')


	






	
	#- cut & sign
	matrix3 = np.abs( matrix3 )
	print 'EneDen_max >>', np.max([np.max(matrix3)])
	print 'EneDen_min  >>', np.min([np.min(matrix3)])









	#---cut edges---#
	if celltocut > 0:
		matrix3 = matrix3[:,celltocut:-celltocut,celltocut:-celltocut]
		y		= y[celltocut:-celltocut]
		z		= z[celltocut:-celltocut]

	p = matrix3.shape
	x2=p[0]/2+sliceposition_x; y2=p[1]/2+sliceposition_y; z2=p[2]/2+sliceposition_z;
	
	sizeX, sizeZ = figure_dimension_inch(x,y,z,magnification_fig)

	levs_lin = np.linspace(      EneDen_min ,      EneDen_max ,isolines)
	levs_log = np.logspace(log10(EneDen_min),log10(EneDen_max),isolines)


	#--------------------#
	#--- Linear plots ---#
	#--------------------#
	#- Plot Elenout -#
	fig = figure(1, figsize=(sizeX, sizeZ))
	contourf(x,y,matrix3[:,:,z2].T,levs_lin, linewidths = 0.00001)
	axis('tight')
	name_output = 'EneDen_XY_lin_'+s+'.png'
	savefig( os.path.join(path,'plots','EneDen',name_output) )
	close(fig)

	fig = figure(1, figsize=(sizeX, sizeZ))	
	contourf(x,z,matrix3[:,y2,:].T,levs_lin, linewidths = 0.00001)
	axis('tight')
	name_output = 'EneDen_XZ_lin_'+s+'.png'
	fig.savefig( os.path.join(path,'plots','EneDen',name_output) )
	close(fig)



	#--------------------#
	#---  Log plots   ---#
	#--------------------#
	#- Plot Elenout -#
	fig = figure(1, figsize=(sizeX, sizeZ))
	contourf(x,y,matrix3[:,:,z2].T, levs_log, norm=colors.LogNorm())
	axis('tight')
	name_output = 'EneDen_XY_log_'+s+'.png'
	savefig( os.path.join(path,'plots','EneDen',name_output) )
	close(fig)

	fig = figure(1, figsize=(sizeX, sizeZ))	
	contourf(x,z,matrix3[:,y2,:].T,levs_log, norm=colors.LogNorm())
	axis('tight')
	name_output = 'EneDen_XZ_log_'+s+'.png'
	fig.savefig( os.path.join(path,'plots','EneDen',name_output) )
	close(fig)

# 	fig = figure(1, figsize=(sizeZ, sizeZ))	
# 	contourf(y,z,matrix[x2,:,:].T, levs_log, norm=colors.LogNorm())
#	axis('tight')
# 	name_output = 'rho_Bunch_YZ_log_'+s+'.png'
# 	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)





    #----- Save density sections data -----#
	if (savedata == 'True'):
    	
		print 'saving EneDen data'
    	
		EneDen = matrix3
		

		p = EneDen.shape
		x2=p[0]/2+sliceposition_x; y2=p[1]/2+sliceposition_y; z2=p[2]/2+sliceposition_z;

	
		np.savetxt( os.path.join(path,'data','EneDen',('EneDen_section_'+('%2.2i'%frame)+'.dat')),EneDen[:,:,z2].T,fmt='%15.14e')
# 		np.savetxt( 'rho_section_'+('%2.2i'%frame)+'.dat' ,rho[:,:,z2].T,fmt='%15.14e')
# 		np.savetxt( 'rho_b_section_'+('%2.2i'%frame)+'.dat' ,rho_b[:,:,z2].T,fmt='%15.14e')


