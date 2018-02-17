# Table of Contents
1. [Introduction](README.md#introduction)
2. [Dependencies](README.md#Dependencies)
3. [Time Compexity](README.md#Time-Compexity)


# Introduction
This is my submission for the Insight Data Engineering challenge,

# Dependencies
The only dependency to run this is having installed Python 2.7 

# Time Compexity

The worst case time colexity if the algorithm is O(NlogN) when every record belongs to the same donor over a period of time. But in that case N would be number of times a single person contributed to same campign over time.
This happens to be the time complexity because I sort the years in which the donation has been given by a particualr individual.

In most cases the time complexity would be O(N), where N is the total number of records. This happens when the number of records is much grater than number of contributions by any particular idiviadual. 