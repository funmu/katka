# Generate NRF Calendar Data

*National Retail Federation* uses special [4-5-4calendar](https://nrf.com/resources/4-5-4-calendar) for consistent revenue reporting acrosss all retailers. 
The tool here is aimed at generating the mapping from Gregorian Calendar to NRF Calendar.

##Solution Approach##
 Start with Jan 30, 2000 as the Retail Epoch. And generate the 4-5-4 calendar output as per NRF rules.
 Uses custom python module and a python notebook to generate the output.

##Code##
 * [Python Class Library for NRF Calendar](NRFCalendar.py)
 * [Python Notebook to use the Class Library](genNRFCalendar.ipynb)

The code has more in-line documentation.

###Testing Code###
 Give it a try inside the Python Library
 

###Wish List###
 * Experience
  * Better visual representation of the generated calendar. 

##Contributors##
Murali Krishnan

