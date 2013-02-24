# ifndef __BINNING_CPP
# define __BINNING_CPP
# include "leggi_binario_ALaDyn_fortran.h"

_Binnaggio :: _Binnaggio(float * particelle, int npart, int ndim, parametri * parametri, float ** data_binned, std::string binx, std::string biny)
{
	int binnare_su_x, binnare_su_y;
	int whichbin_x, whichbin_y;

	if (binx == "x") binnare_su_x = 0;
	else if (binx == "y") binnare_su_x = 1;
	else if (binx == "z") binnare_su_x = 2;
	else if (binx == "px") binnare_su_x = 3;
	else if (binx == "py") binnare_su_x = 4;
	else if (binx == "pz") binnare_su_x = 5;
	else if (binx == "gamma") binnare_su_x = 6;
	else if (binx == "theta") binnare_su_x = 7;
	else if (binx == "E") binnare_su_x = 8;
	else printf("variabile x non riconosciuta\n");

	if (biny == "x") binnare_su_y = 0;
	else if (biny == "y") binnare_su_y = 1;
	else if (biny == "z") binnare_su_y = 2;
	else if (biny == "px") binnare_su_y = 3;
	else if (biny == "py") binnare_su_y = 4;
	else if (biny == "pz") binnare_su_y = 5;
	else if (biny == "gamma") binnare_su_y = 6;
	else if (biny == "theta") binnare_su_y = 7;
	else if (biny == "E") binnare_su_y = 8;
	else printf("variabile y non riconosciuta\n");

	float x, y, z, px, py, pz, gamma, theta, E;
	float dato_da_binnare_x, dato_da_binnare_y;
	for (int i = 0; i < npart; i++)
	{
		x=*(particelle+i*(2*ndim+parametri->p[WEIGHT]));
		y=*(particelle+i*(2*ndim+parametri->p[WEIGHT])+1);
		z=*(particelle+i*(2*ndim+parametri->p[WEIGHT])+2);
		px=*(particelle+i*(2*ndim+parametri->p[WEIGHT])+3);
		py=*(particelle+i*(2*ndim+parametri->p[WEIGHT])+4);
		pz=*(particelle+i*(2*ndim+parametri->p[WEIGHT])+5);
		gamma=(float)(sqrt(1.+px*px+py*py+pz*pz)-1.);			//gamma
		theta=(float)(atan2(sqrt(py*py+pz*pz),px)*180./M_PI);	//theta nb: py e pz sono quelli trasversi in ALaDyn!
		E=(float)(gamma*parametri->massa_particella_MeV);								//energia
		if (binnare_su_x < 6) dato_da_binnare_x = *(particelle+i*(2*ndim+parametri->p[WEIGHT])+binnare_su_x);
		else if (binnare_su_x == 6) dato_da_binnare_x = gamma;
		else if (binnare_su_x == 7) dato_da_binnare_x = theta;
		else if (binnare_su_x == 8) dato_da_binnare_x = E;
		if (binnare_su_y < 6) dato_da_binnare_y = *(particelle+i*(2*ndim+parametri->p[WEIGHT])+binnare_su_y);
		else if (binnare_su_y == 6) dato_da_binnare_y = gamma;
		else if (binnare_su_y == 7) dato_da_binnare_y = theta;
		else if (binnare_su_y == 8) dato_da_binnare_y = E;



		if (dato_da_binnare_x < parametri->minimi[binnare_su_x])
		{
			whichbin_x = 0;
		}
		else if (dato_da_binnare_x > parametri->massimi[binnare_su_x])
		{
			whichbin_x = parametri->nbin_x + 2;
		}
		else
		{
			whichbin_x = (int) (((x - parametri->minimi[binnare_su_x]) / parametri->dimmi_dim(binnare_su_x)) +1.0);
		}
		if (px < parametri->pxmin)
		{
			whichbin_y = 0;
		}
		else if (px > parametri->pxmax)
		{
			whichbin_y = parametri->nbin_px + 2;
		}
		else
		{
			whichbin_y = (int) (((px - parametri->pxmin) / parametri->dimmi_dimpx()) +1.0);
		}
		if (WEIGHT) data_binned[whichbin_x][whichbin_y] += *(particelle+i*(2*ndim+parametri->p[WEIGHT])+6);
		else		data_binned[whichbin_x][whichbin_y] += 1.0;
	}
}

_Binnaggio :: _Binnaggio(float * particelle, int npart, int ndim, parametri * parametri, float * data_binned, std::string binx)
{
	int binnare_su_x;
	int whichbin_x;

	if (binx == "x") binnare_su_x = 0;
	else if (binx == "y") binnare_su_x = 1;
	else if (binx == "z") binnare_su_x = 2;
	else if (binx == "px") binnare_su_x = 3;
	else if (binx == "py") binnare_su_x = 4;
	else if (binx == "pz") binnare_su_x = 5;
	else if (binx == "gamma") binnare_su_x = 6;
	else if (binx == "theta") binnare_su_x = 7;
	else if (binx == "E") binnare_su_x = 8;
	else printf("variabile x non riconosciuta\n");

	float x, y, z, px, py, pz, gamma, theta, E;
	float dato_da_binnare_x;
	for (int i = 0; i < npart; i++)
	{
		x=*(particelle+i*(2*ndim+parametri->p[WEIGHT]));
		y=*(particelle+i*(2*ndim+parametri->p[WEIGHT])+1);
		z=*(particelle+i*(2*ndim+parametri->p[WEIGHT])+2);
		px=*(particelle+i*(2*ndim+parametri->p[WEIGHT])+3);
		py=*(particelle+i*(2*ndim+parametri->p[WEIGHT])+4);
		pz=*(particelle+i*(2*ndim+parametri->p[WEIGHT])+5);
		gamma=(float)(sqrt(1.+px*px+py*py+pz*pz)-1.);			//gamma
		theta=(float)(atan2(sqrt(py*py+pz*pz),px)*180./M_PI);	//theta nb: py e pz sono quelli trasversi in ALaDyn!
		E=(float)(gamma*parametri->massa_particella_MeV);		//energia
		if (binnare_su_x < 6) dato_da_binnare_x = *(particelle+i*(2*ndim+parametri->p[WEIGHT])+binnare_su_x);
		else if (binnare_su_x == 6) dato_da_binnare_x = gamma;
		else if (binnare_su_x == 7) dato_da_binnare_x = theta;
		else if (binnare_su_x == 8) dato_da_binnare_x = E;

		if (dato_da_binnare_x < parametri->minimi[binnare_su_x])
		{
			whichbin_x = 0;
		}
		else if (dato_da_binnare_x > parametri->massimi[binnare_su_x])
		{
			whichbin_x = parametri->nbin_x + 2;
		}
		else
		{
			whichbin_x = (int) (((x - parametri->minimi[binnare_su_x]) / parametri->dimmi_dim(binnare_su_x)) +1.0);
		}
		if (WEIGHT) data_binned[whichbin_x] += *(particelle+i*(2*ndim+parametri->p[WEIGHT])+6);
		else		data_binned[whichbin_x] += 1.0;
	}
}

#endif

