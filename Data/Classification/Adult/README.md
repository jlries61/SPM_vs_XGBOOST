## Title of Database: Adult

Link: https://archive.ics.uci.edu/ml/datasets/Adult

This data was extracted from the census bureau database found at (http://www.census.gov/ftp/pub/DES/www/welcome.html)

* 48842 instances, mix of continuous and discrete    (train=32561, test=16281)
* 45222 if instances with unknown values are removed (train=30162, test=15060)
* Duplicate or conflicting instances : 6
* Class probabilities:
  * Probability for the label '>50K'  : 23.93% / 24.78% (without unknowns)
  * Probability for the label '<=50K' : 76.07% / 75.22% (without unknowns)

Prediction task is to determine whether a person makes over 50K a year.

In the files ("class"):
- >50K = 1
- <=50K = 0

##### Number of Instances: 32561 (train), 16281 (test)
##### Number of Attributes: 14
#### Attribute information:
	1.	age:			continuous.
	2.	workclass:		Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, 
						Local-gov, State-gov, Without-pay, Never-worked.
	3.	fnlwgt:			continuous.
	4.	education: 		Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, 
						Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 
						5th-6th, Preschool.
	5.	education-num:	continuous.
	6.	marital-status:	Married-civ-spouse, Divorced, Never-married, Separated, Widowed, 
						Married-spouse-absent, Married-AF-spouse.
	7.	occupation:		Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, 
						Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, 
						Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, 
						Armed-Forces.
	8.	relationship:	Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
	9.	race:			White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
	10.	sex:			Female, Male.
	11.	capital-gain:	continuous.
	12.	capital-loss:	continuous.
	13.	hours-per-week:	continuous.
	14.	native-country:	United-States, Cambodia, England, Puerto-Rico, Canada, Germany, 
						Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, 
						Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, 
						Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, 
						Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, 
						Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, 
						Holand-Netherlands.