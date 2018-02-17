from __future__ import division
import os
import sys
import math

def record_is_valid(cmte_id, name, zipcode, transaction_date, transaction_amt, other):
    if len(cmte_id) == 0 or len(name) == 0 or len(zipcode) < 5 or len(transaction_date)!=8 \
    or len(transaction_amt) == 0 or len(other) > 0:
        return False
    return True
    
def update_namezipdict(name, zipcode, namezipdict, transaction_date):
    repeat = 0
    year = int(transaction_date[4:])
    zipcode = zipcode[:5]
    if (name,zipcode) in namezipdict:
        years = namezipdict[(name,zipcode)]
        if years[0] < year:
            repeat = 1
        years.append(year)
        years = sorted(years)
        namezipdict[(name,zipcode)] = years
    else:
        namezipdict[(name,zipcode)] = [year]
    
    
    return repeat, namezipdict


def update_percentiledict(cmte_id, zipcode, percentiledict, year, transaction_amt):
    transaction_amt = float(transaction_amt)
    if transaction_amt%1 >= 0.5:
        transaction_amt = int(transaction_amt) + 1
    else:
        transaction_amt = int(transaction_amt)
        
    
    if (cmte_id, year, zipcode) in percentiledict:
        amounts = percentiledict[(cmte_id, year, zipcode)]
        amounts.append(transaction_amt)
        amounts = sorted(amounts)
        percentiledict[(cmte_id, year, zipcode)] = amounts
    
    else:
        percentiledict[(cmte_id, year, zipcode)] = [transaction_amt]
    
    return percentiledict
        
def update_repeatamtdict(cmte_id, zipcode, repeatamtdict, year, transaction_amt):
    if (cmte_id, year, zipcode) in repeatamtdict:
        amount = repeatamtdict[(cmte_id, year, zipcode)]
        amount += float(transaction_amt)
        repeatamtdict[(cmte_id, year, zipcode)] = amount
    
    else:
        repeatamtdict[(cmte_id, year, zipcode)] = float(transaction_amt)
    
    return repeatamtdict

def update_repeatcountdict(cmte_id, zipcode, repeatcountdict, year):
    if (cmte_id, year, zipcode) in repeatcountdict:
        repeatcountdict[(cmte_id, year, zipcode)] += 1
    
    else:
        repeatcountdict[(cmte_id, year, zipcode)] = 1
    
    return repeatcountdict
    
    
        
def main(input_file,percentile_file, output_file):
    
    namezipdict = {}
    percentiledict = {}
    repeatamtdict = {}
    repeatcountdict = {}
    unvalid_record_count = 0
    
    
    for line in percentile_file:
        percentile = line
    
    for line in input_file:
        vals = line.split('|')
        if len(vals) == 21:
            cmte_id = vals[0]
            name = vals[7]
            zipcode = vals[10]
            transaction_date = vals[13]
            transaction_amt = vals[14]
            if int(transaction_amt) > 0:
                
                other = vals[15]
                if record_is_valid(cmte_id, name, zipcode, transaction_date, transaction_amt,\
                                                                                other)== True:
                    repeat, namezipdict = update_namezipdict(name, zipcode, namezipdict,\
                                                                         transaction_date)
                    if repeat == 1:
                        year = int(transaction_date[4:])
                        zipcode = zipcode[:5]
                        percentiledict = update_percentiledict(cmte_id, zipcode, percentiledict,\
                                                                        year, transaction_amt)
                        amount_list = percentiledict[(cmte_id, year, zipcode)]
                        index = int(math.ceil((int(percentile)/100) * len(amount_list))) - 1
                        
                        percentile_amt = amount_list[index]
                        repeatamtdict = update_repeatamtdict(cmte_id, zipcode, repeatamtdict, \
                                                                         year, transaction_amt)
                        repeat_amount = repeatamtdict[(cmte_id, year, zipcode)]
                        repeatcountdict = update_repeatcountdict(cmte_id, zipcode, \
                                                                 repeatcountdict, year)
                        repeat_count = repeatcountdict[(cmte_id, year, zipcode)]
                        output_str = cmte_id +"|"+zipcode+"|"+str(year)+"|"+str(percentile_amt)\
                                            +"|"+str(int(repeat_amount))+"|"+str(repeat_count)+"\n"
                        output_file.write(output_str)
                    
            else:
                unvalid_record_count += 1
    
    print "There number of unvalid records was:", unvalid_record_count                 
    return                      


if __name__ == '__main__':
    input_file = open(sys.argv[1], 'r')
    percentile_file = open (sys.argv[2], 'r')
    output_file = open (sys.argv[3], 'w')
    main(input_file,percentile_file, output_file)
    input_file.close()
    percentile_file.close()
    output_file.close()
