## Title of Database: Leo Breiman's twonorm example

Link: http://www.dcc.fc.up.pt/~ltorgo/Regression/DataSets.html

Classification of 2 overlapping normal distributions.

This is an implementation of Leo Breiman's twonorm example [1]. 
It is a 20 dimensional, 2 class classification example. Each class is 
drawn from a multivariate normal distribution with unit variance. 
Class 1 has mean (a,a,..a) while Class 2 has mean (-a,-a,..-a). 
Where a = 2/sqrt(20). Breiman reports the theoretical expected 
misclassification rate as 2.3%. He used 300 training examples 
with CART and found an error of 22.1%.

(1) Breiman L. Bias, variance and arcing classifiers. Tec. Report 460, Statistics department. University of california. April 1996.

* Origin: artificial
* Usage: historical
* Order: uninformative

##### Variable to Predict: last column
##### Number of Instances: 7400
##### Number of Attributes: 20

#### Attribute information:
	1.	I1		u	[-Inf,Inf]	Input 1
	2.	I2		u	[-Inf,Inf]	Input 2
	3.	I3		u	[-Inf,Inf]	Input 3
	4.	I4		u	[-Inf,Inf]	Input 4
	5.	I5		u	[-Inf,Inf]	Input 5
	6.	I6		u	[-Inf,Inf]	Input 6
	7.	I7		u	[-Inf,Inf]	Input 7
	8.	I8		u	[-Inf,Inf]	Input 8
	9.	I9		u	[-Inf,Inf]	Input 9
	10.	I10		u	[-Inf,Inf]	Input 10
	11.	I11		u	[-Inf,Inf]	Input 11
	12.	I12		u	[-Inf,Inf]	Input 12
	13.	I13		u	[-Inf,Inf]	Input 13
	14.	I14		u	[-Inf,Inf]	Input 14
	15.	I15		u	[-Inf,Inf]	Input 15
	16.	I16		u	[-Inf,Inf]	Input 16
	17.	I17		u	[-Inf,Inf]	Input 17
	18.	I18		u	[-Inf,Inf]	Input 18
	19.	I19		u	[-Inf,Inf]	Input 19
	20.	I20		u	[-Inf,Inf]	Input 20
	21.	class	u	0 1			Class (0 1)