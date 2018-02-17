import os
import sys
import time
import heapq
from datetime import datetime
from bisect import bisect_right, bisect_left





def dt_to_timestamp(date_time):
    """ 
    This is a function to convert the given date time format to timestamp format
    Iterating through timestamp format is easier
    """
    date_time = date_time.split()[:-1]
    timestamp = time.mktime(time.strptime(date_time[0], '%d/%b/%Y:%H:%M:%S'))
    return timestamp

def ts_to_datetime(timestamp):
    """ 
    This is a function which takes the timestamp as input and returns date time format
    The date time format is used to store entries in a dictonary to keep count
    """
    date_time = datetime.fromtimestamp(timestamp).strftime('%d/%b/%Y:%H:%M:%S -0400')
    return date_time




def period(store_ts, size):
    """ 
    This is a function to create a dictionary with the start time as the key and number of times the site was accessed in the 
    following 60 minutes period. This method take O(NlogN) to construct the dictonary.  
    """
    period_count = {}
    time_start = store_ts[0] 
    time_stop = store_ts[-1]
    size = min(size, time_stop - time_start)
    
    cur_time = store_ts[0]
    while cur_time <= store_ts[-1]:
        
        target_time = cur_time + size
        if target_time >= store_ts[-1]:
            target_index = len(store_ts) - 1
        else:
            target_index = bisect_right(store_ts, target_time) - 1
        
        cur_index = bisect_left(store_ts, cur_time)

        
        period_count[ts_to_datetime(cur_time)] = target_index - cur_index + 1
        cur_time += 1 

    return period_count



def feature1(ip_dict, n, output_file):
    '''
    This a function which takes a dictonary that contains all the ip addresses mapped to number of requests and finds the top 
    '''
    ip_heap = [(-value, key) for key, value in ip_dict.items()]
    heapq.heapify(ip_heap)
    size = min(len(ip_dict), n)
    for i in range(size):
        ip_count = heapq.heappop(ip_heap)
        output_file.write(str(ip_count[1]) + ',' + str(-ip_count[0]) + '\n')
        heapq.heapify(ip_heap)
    print "Feature 1 done"

def feature2(resource_dict, n, output_file):
    '''
    This a function which takes a dictonary that contains all the resources mapped to the bandwith and finds the top 
    '''
    resource_heap = [(-value, key) for key, value in resource_dict.items()]
    heapq.heapify(resource_heap)
    size = min(len(resource_heap), n)
    for i in range(size):
        resource_count = heapq.heappop(resource_heap)
        output_file.write(str(resource_count[1]) + '\n')
        heapq.heapify(resource_heap)
    print "Feature 2 done"
    

def feature3(period_count, n, output_file):
    '''
    This a function which takes a dictonary that contains all 60 minute periods mapped to traffic and finds the top 
    '''
    period_heap = [(-value, key) for key, value in period_count.items()]
    heapq.heapify(period_heap)
    size = min(len(period_count), n)
    for i in range(size):
        period = heapq.heappop(period_heap)
        output_file.write(str(period[1]) + ',' + str(-period[0]) + '\n')
        heapq.heapify(period_heap)       
    
    print "Feature 3 done"


def feature4(store_time, size, store_line, block_file):
    """ 
    This function takes in two arrays: store_time contains a list ip and time, store_line contains all the log information.
    It detects the anomalous logins if there are 3 or more failed attempts in 20s windows and writes them to the appropriate file.
    It takes O(N) time to do the whole operation.
    """
    block_dict = {}
    i = 0
    while i < len(store_time):
        ip = store_line[i][0]
        http_num = store_line[i][-2]
        
        if http_num == '200' and ip not in block_dict:
            i += 1
            continue
        
        elif http_num == '200' and ip in block_dict and dt_to_timestamp(block_dict[ip][0]) - dt_to_timestamp(store_time[i][0])< size:
            if block_dict[ip][1] >= 3: 
                block_file.write(' '.join(store_line[i]) + '\n')
            i += 1
            continue
        
        elif http_num == '200' and ip in block_dict and dt_to_timestamp(block_dict[ip][0]) - dt_to_timestamp(store_time[i][0]) > size:
            del block_dict[ip]
            i += 1
            continue
        
        
        elif http_num == '401' and ip not in block_dict:
            block_dict[ip] = [store_time[i][0], 1]
            i += 1
            continue
        
        elif http_num == '401' and ip in block_dict and dt_to_timestamp(block_dict[ip][0]) - dt_to_timestamp(store_time[i][0]) > size:
            del block_dict[ip]
            block_dict[ip] = [store_time[i][0], 1]
            i += 1
            continue
        
        elif http_num == '401' and ip in block_dict and dt_to_timestamp(block_dict[ip][0]) - dt_to_timestamp(store_time[i][0]) < size:
            block_num = block_dict[ip][1] + 1
            block_dict[ip][1] = block_num
            if block_num > 3:
                block_file.write(' '.join(store_line[i]) + '\n')
            i += 1
            continue

        i += 1
    print "Feature 4 done"




if __name__ == '__main__':
    
    '''This is the main function where I read the input, store them in appropriate data structures to simplify the task of 
       rest of the feature functions
    '''

    #intializing data strucutres that are goining to be used

    ip_dict = {}
    resource_dict = {}
    store_line = []
    store_time = []
    store_ts = []

    
    #intializng some variables
    
    time_count = 0
    prev_date_time = None
    
    
    input_file = open(sys.argv[1], 'r')
    hosts_file = open(sys.argv[2],'w')
    hours_file = open(sys.argv[3], 'w')
    resource_file = open(sys.argv[4], 'w')
    block_file = open(sys.argv[5], 'w')
    

   
    
    while True:
        try:
            for line in input_file:
                
                    
                words = line.split('- -')
                ip = words[0][0:-1]
                words = words[1].split('] ')
                date_time = words[0][2:]
                words = words[1].split(' ')
                resource_dest = words[1] 
                resource_size = words[4].split("\n")[0] 
                line = line.split("\n")[0]
                store_ts.append(dt_to_timestamp(date_time))
                store_line.append(line.split())
                store_time.append([date_time, ip])
                
                if ip not in ip_dict:
                    ip_dict[ip] = 1
                else:
                    ip_dict[ip] += 1
                
                if resource_dest!='/' and resource_size.isdigit():
                    if resource_dest not in resource_dict:
                        resource_dict[resource_dest] = int(resource_size)
                    else:
                        resource_dict[resource_dest] += int(resource_size)
                    
                
                            
                    
                
                    
        
                  
        except (AttributeError):
            print "AttributeError"
            pass
        
        except (IndexError):
            print "IndexError"
            pass
        
        except (UnicodeDecodeError):
            print "UnicodeDecodeError"
            pass
            
        else:
            break
            
    
    # Calling all the feature functions
    
    feature1(ip_dict, 10, hosts_file)

    feature2(resource_dict, 10, resource_file)

    period_count = period(store_ts, 3600)

    feature3(period_count, 10, hours_file)

    feature4(store_time, 20, store_line, block_file)