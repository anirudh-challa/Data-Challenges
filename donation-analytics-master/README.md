# Table of Contents
1. [Introduction](README.md#introduction)
2. [Dependencies](README.md#Dependencies)
3. [Dependencies](README.md#Running-the-Solution)
4. [Time Compexity](README.md#Time-Compexity)
5. [Approach](README.md#Approach)
6. [Testing](README.md#Testing) 
7. [Assumptions](README.md#Assumptions) 

# Introduction
This is my submission for the Insight Data Engineering challenge.

# Dependencies
The only dependency to run this is having installed Python 2.7.

#Running the Solution
The easiest way to run the code for a new set of inputs is to change the input files in ./input/
The all you have to do is to run the run.sh file 

# Time Compexity
In worst case time complexity would be O(N), where N is the total number of records. This is assuming that the number of records is much grater than number of contributions by any particular indiviadual. 

# Approach
The high level overview is that we parse the the input file and make sure that the input fits the criteria in the problem statement. Once, we have clean data for the fields we are interested in the real solution begins.

First, we know that we should keep track of repeated donors. We are looking for a solution that minimizes the time complexity. The data structure which is most useful for insertaion, searching and deletion mostly in constant time is the Hash map. But here for the same (Name, zipcode) combination there would be mutiple entries as the same donor could have already contributed to multiple campigns. We also know that the input need not be in chronological order. So to keep track of the earliest year in which a campign contribution is made and compare it with the current year to see if the person would be counted as repeated we sort. This should not affect the time complexity as the number entries for each user would at the maximum be only in the 10s. 

Next, once we realize that we have already come accross a particular contributor we must output the required line in the repeated_donors.txt. To do this we need to keep track of the given %tile of repeated donor contribution, total money given by repeated donors and the number of repeated donors for a particular campign, from a particular zipcode and a given year. It is clear from this that the unique item is the commbination of campign id, zip code and year. So we create 3 hash maps with this as the key and the values would be all the campign contributions from repeated donors, total amout from the repeated donors and the count for the three other fields respectively. This enable us to easily retrieve and edit these values as we "stream" more data.

# Testing
I initailly ran the inisght test suite and once I got the correct result for that I moved on to testing it for larger data from FEC data after 2015. The largest dataset I tested for is 400,000 entries and it ran on my Mac within a second. 

I also wrote a sample unit test in (/.src/test.py) for a function that checks whether the input is valid for us to process the important fields from a given row. Ideally, I should have written unit tests for all the functions but that would have taken a lot longer.

#Assumptions
1) Time granularity is year: We do not care if a contributor donated earlier in the same year i.e. if a person contributes twice in the same year he/she will not be counted as a repeated donor the second time. The granulaity for being repeated is set to the year.
2) Sorting operations: Sorting the data for a particular key will really not affect the time complexity since we will not have many values for the same key of (campign id, zip code, year), if not the time complexity would be    O(Nxmlogm) where m is the maximum number of entries for a particular key. But assuming N>>m gives us O(N).
3) Refunds do not count: That we do not count refunds from a campign to count someone as a repeated repeated donor even though the donor is involved in another transaction when they get a refund from a particular campign that they have donated to.
