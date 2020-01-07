## Title of Database: SPAM E-mail Database

Link: https://archive.ics.uci.edu/ml/datasets/Spambase

##### Number of Instances: 4601
##### Number of Attributes: 57

##### Class Distribution:
	Spam		1813	(39.4%)
	Non-Spam	2788	(60.6%)

#### Attribute information:
	48 	continuous real [0,100] attributes of type word_freq_WORD 
		= percentage of words in the e-mail that match WORD,
		i.e. 100 * (number of times the WORD appears in the e-mail) / 
		total number of words in e-mail.  A "word" in this case is any 
		string of alphanumeric characters bounded by non-alphanumeric 
		characters or end-of-string.
	6 	continuous real [0,100] attributes of type char_freq_CHAR
		= percentage of characters in the e-mail that match CHAR,
		i.e. 100 * (number of CHAR occurences) / total characters in e-mail
	1	continuous real [1,...] attribute of type capital_run_length_average
		average length of uninterrupted sequences of capital letters
	1	continuous integer [1,...] attribute of type capital_run_length_longest
		= length of longest uninterrupted sequence of capital letters
	1	continuous integer [1,...] attribute of type capital_run_length_total
		= sum of length of uninterrupted sequences of capital letters
		= total number of capital letters in the e-mail
	1	nominal {0,1} class attribute of type spam
		= denotes whether the e-mail was considered spam (1) or not (0), 
		i.e. unsolicited commercial e-mail.  
						
##### Missing Attribute Values: none