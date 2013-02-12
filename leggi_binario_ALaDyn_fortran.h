#ifndef __LEGGI_ALADYN_FORTRAN
#define __LEGGI_ALADYN_FORTRAN

#define _USE_MATH_DEFINES

#include<cstdio>
#include<iostream>
#include<cstdlib>
#include<cmath>
#include<cstring>
#include<string>
#include<fstream>
#include<sstream>
#include<iomanip>
#include<cstdarg>
#ifndef _WIN32
#include <strings.h>
#else
int    strcasecmp(const char* s1, const char* s2)
{
    for (;;) {
        int c1 = tolower( *((unsigned char*) s1++));
        int c2 = tolower( *((unsigned char*) s2++));

        if ((c1 != c2) || (c1 == '\0')) {
            return( c1 - c2);
        }
    }
}
#endif


// #define ENABLE_DEBUG


#define MAX(x,y) ((x)>(y)?(x):(y))
#define MIN(x,y) ((x)<(y)?(x):(y))
#define TRUE 1
#define FALSE 0

#define C						2.99792458e+10		// cm / s
#define ME_G					9.10938291E-28		// electron mass [g]
#define MP_G					1.6726231e-24		// proton mass [g]
#define MP_MEV					938.272013			// proton mass [MeV/c^2]
#define ME_MEV					0.510998928			// electron mass [MeV/c^2]
// #define CHARGE				4.80320425e-10		// statC	commentata perche' Turchetti la usa un po' diversa
#define CHARGE					4.803262e-10		// statC    valore usato da Turchetti; nb: e' impreciso negli ultimi due decimali
#define FROM_TESLA_TO_GAUSS		1.0e+4
// #define DA_ERG_A_MEV			6.2415097523028e+5	// conversione Servizi
#define DA_ERG_A_MEV			6.241509744512e+5	// conversione Sinigardi
#define FROM_VOLT_TO_STATVOLT	3.335640951982e-3	// 1 statvolt = 299.792458 volts.

#define NUMERO_MASSIMO	1.0e30
#define MAX_LENGTH_FILENAME 200

#pragma warning(disable : 593)

#define NPARAMETRI	8
#define WEIGHT		0
#define FUNZIONE	1
#define SWAP		2
#define OUT_BINARY	3
#define OUT_ASCII	4
#define	FIND_MINMAX	5
#define DO_BINNING	6
#define OUT_PARAMS	7



# define __0X00 0x1
# define __0X01 0x2
# define __0X02 0x4
# define __0X03 0x8
# define __0X04 0x10
# define __0X05 0x20
# define __0X06 0x40
# define __0X07 0x80
# define __0X08 0x100
# define __0X09 0x200
# define __0X10 0x400
# define __0X11 0x800
# define __0X12 0x1000
# define __0X13 0x2000
# define __0X14 0x4000
# define __0X15 0x8000
# define __0X16 0x10000
# define __0X17 0x20000
# define __0X18 0x40000
# define __0X19 0x80000
# define __0X20 0x100000
# define __0X21 0x200000
# define __0X22 0x400000
# define __0X23 0x800000
# define __0X24 0x1000000
# define __0X25 0x2000000
# define __0X26 0x4000000
# define __0X27 0x8000000
# define __0X28 0x10000000
# define __0X29 0x20000000
# define __0X30 0x40000000
# define __0X31 0x80000000
# ifndef NUM_FILTRI
# define NUM_FILTRI 14
# endif

namespace cost
 {unsigned int xmin = __0X00;
  unsigned int ymin = __0X01;
  unsigned int zmin = __0X02;
  unsigned int pxmin = __0X03;
  unsigned int pymin = __0X04;
  unsigned int pzmin = __0X05;
  unsigned int xmax = __0X06;
  unsigned int ymax = __0X07;
  unsigned int zmax = __0X08;
  unsigned int pxmax = __0X09;
  unsigned int pymax = __0X10;
  unsigned int pzmax = __0X11;
  unsigned int emin = __0X12;
  unsigned int emax = __0X13;
  unsigned int tutte[]=
   {xmin, ymin, zmin, pxmin, pymin, pzmin, xmax, ymax, zmax, pxmax, pymax, pzmax, emin, emax};
// varie ed eventuali
  }


struct parametri
 {
	int nbin_x, nbin_y, nbin_z, nbin_px, nbin_py, nbin_pz, nbin_E, nbin_theta, nbin_gamma;
	int p[NPARAMETRI];
	char support_label[MAX_LENGTH_FILENAME];
	float xmin, xmax, pxmin, pxmax, ymin, ymax, pymin, pymax, zmin, zmax, pzmin, pzmax, Emin, Emax, gammamin, gammamax, thetamin, thetamax;
	parametri();
	/* costruttore parametrico 1D */
	parametri(float, float, float, float, int, int);
	float dimmi_dimx();
	float dimmi_dimy();
	float dimmi_dimz();
	float dimmi_dimpx();
	float dimmi_dimpy();
	float dimmi_dimpz();
	float dimmi_dimgamma();
	float dimmi_dimtheta();
	float dimmi_dimE();
	void leggi_da_file(const char *);
	void leggi_interattivo();
	void leggi_da_shell(int, char *[]);
	bool check_parametri();
};

struct _Filtro
 {
  enum class _Nomi : int
   {xmin, ymin, zmin, xmax, ymax, zmax,
    pxmin, pymin, pzmin, pxmax, pymax, pzmax,
    emin, emax} nomi;
static float * costruisci_filtro(const char *, ...);
static void individua_filtro(char *, float, float *&);
static const unsigned int cost[];
static unsigned int maschera_interna;
struct _flag_filtri
 {unsigned meno_xmin:1;
  unsigned meno_ymin:1;
  unsigned meno_zmin:1;
  unsigned piu_xmax:1;
  unsigned piu_ymax:1;
  unsigned piu_zmax:1;
  unsigned meno_pxmin:1;
  unsigned meno_pymin:1;
  unsigned meno_pzmin:1;
  unsigned piu_pxmax:1;
  unsigned piu_pymax:1;
  unsigned piu_pzmax:1;
  unsigned meno_ener:1;
  unsigned piu_ener:1;
  _flag_filtri operator=(int o)
   {meno_xmin = meno_ymin = meno_zmin =
    meno_pxmin = meno_pymin = meno_pzmin =
    piu_xmax = piu_ymax = piu_zmax =
    piu_pxmax = piu_pymax = piu_pzmax =
    meno_ener = piu_ener = 0;
    return *this;}
// varie ed eventuali
   } flag_filtri;
  static const char * descr[];
  _Filtro(float *, unsigned int [], float *, unsigned int = 0);
};

int leggi_campi(char * , parametri );
int leggi_particelle(char * , parametri);
void swap_endian_s(short* ,int );
void swap_endian_i(int* ,int );
void swap_endian_f(float* , int );

#endif
