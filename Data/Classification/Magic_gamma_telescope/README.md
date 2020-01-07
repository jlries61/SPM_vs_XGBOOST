## Title of Database: MAGIC gamma telescope data 2004

Link: https://archive.ics.uci.edu/ml/datasets/MAGIC+Gamma+Telescope

The data are MC generated (see below) to simulate registration of high energy
gamma particles in a ground-based atmospheric Cherenkov gamma telescope using the
imaging technique.
	
##### Number of Instances: 19020
##### Number of Attributes: 10

##### Attribute information:
	1.	fLength:	continuous	major axis of ellipse [mm]
	2.	fWidth:		continuous	minor axis of ellipse [mm] 
	3.	fSize:		continuous	10-log of sum of content of all pixels [in #phot]
	4.	fConc:		continuous	ratio of sum of two highest pixels over fSize  [ratio]
	5.	fConc1:		continuous	ratio of highest pixel over fSize  [ratio]
	6.	fAsym:		continuous	distance from highest pixel to center, projected onto major axis [mm]
	7.	fM3Long:	continuous	3rd root of third moment along major axis  [mm] 
	8.	fM3Trans:	continuous	3rd root of third moment along minor axis  [mm]
	9.	fAlpha:		continuous	angle of major axis with vector to origin [deg]
	10.	fDist:		continuous	distance from origin to center of ellipse [mm]
	11.	class:		g,h			gamma (signal), hadron (background)

##### Missing Attribute Values: None

##### Class Distribution:
	g = gamma (signal) (0 in csv):			12332
	h = hadron (background) (1 in csv):		6688