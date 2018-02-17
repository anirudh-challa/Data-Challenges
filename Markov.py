import os
import random
import sys

def generate(path, p, n):
    
    p = int(p)
    n = int(n)

    text = []
    prefix = []

    

    for filename in os.listdir(path):
        filename = os.path.join(path, filename)

        with open(filename) as f:    # provide a text-file to parse
            for line in f:
                
                line = line.split(' ')
                prefix.append(line[0:int(p)])
                text += line[int(p):]

            
    
    
    markov = {}
    
    for t in text:
        markov[t] = []
    
    for i in range(len(text)-1):
        markov[text[i]].append(text[i+1])
    

    new = markov.keys() 
    
    
    sentences = ''
    i = 0
    while i <= n: 
        


        try:

            seed = random.randint(1, len(prefix)) - 1
            
            sentence_data = ''
            
            for x in prefix[seed]:
            
                sentence_data += x+' ' 
            
            seed = random.randint(1, len(text)) - 1
            current_word = text[seed]
            sentence_data += current_word+' '
            
            while '\n' in current_word!='True':
                next_index = random.randint(0, len(markov[current_word]) - 1)    # randomly pick a word from the last words list.
                next_word = markov[current_word][next_index]
                sentence_data += next_word
                current_word = next_word
            
            current_word = ''
            next_word = ''
            sentences += sentence_data+'\n'
            i += 1

        except ValueError, IndexError:
            continue

    
    return sentences

if __name__ == "__main__":
    path = sys.argv[1]
    p = sys.argv[2]
    n = sys.argv[3]
    sen = generate(path, p, n)
    print sen