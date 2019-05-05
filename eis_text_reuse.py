#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 12:56:38 2019

@author: raghebal-ghezi
"""

import sys
import os
import string
import codecs

DELETECHARS = ''.join([string.punctuation, string.whitespace])
LENGTH = 50

def load_text(file_name):
    # load text file and return a string of its content
    with codecs.open(file_name,"r", "latin-1") as file:
        return file.read()
    
def traverse(dir_loc):
    '''
    Walks in the directory, iterates over all files and returns a dictionary of its name 
    and a list of ngram chunks of its content
    
    Arg: location of the directory[String]
    Returns: dictionary File_name[String]:ngram_chunks[List]
    '''
    docs_contents = list() # keys are docs names: values are ngram chunks of its contents       
    files = [files for root, dirs, files in os.walk("./"+str(dir_loc))]
    for name in files[0]:
        if name.endswith(".txt"):
            docs_contents.append(name)
    return docs_contents
    
def tokenize(text, length):
    """ Tokeniz a given text and return a dict containing all start and end
    positions for each token.
    Characters defined in the global string DELETECHARS will be ignored.

    Keyword arguments:
    text   -- the text to tokenize
    length -- the length of each token
    """
    tokens = {}
    token = []

    for i in range(0, len(text)):
        if text[i] not in DELETECHARS:
            token.append((i, text[i]))
        if len(token) == length:
            ngram = ''.join([x[1].lower() for x in token])
            if ngram not in tokens:
                tokens[ngram] = []
            tokens[ngram].append((token[0][0], token[-1][0]))
            token = token[1:]

    return tokens




def compare(src_text, susp_text, tokens):
    """ Test a suspicious document for near-duplicate plagiarism with regards to
    a source document and return the number of overlapping characters.
    INPUT: src_text: String text of source document
           susp_text: String text of suspicious document
           tokens: dict containing all start and end positions for each token in suspicious
    Returns:
            number of overlapping characters between src_t and susp_t
    """

    detections = []
    source_ngram = []
    skipto = -1
    token = []
    for i in range(0, len(src_text)): 
        if i > skipto:
            if src_text[i] not in DELETECHARS:
                token.append((i, src_text[i]))
            if len(token) == LENGTH:
                ngram = ''.join([x[1].lower() for x in token]) # create ngram for the source
                source_ngram.append(ngram)
                if ngram in tokens:
                    d = ((token[0][0],token[-1][0]),
                         (tokens[ngram][0][0],
                          tokens[ngram][0][1]))
                    for t in tokens[ngram]:
                        start_src = token[0][0]
                        start_susp = t[0]
                        while (start_susp < len(susp_text) and
                               start_src < len(src_text) and
                               src_text[start_src] == susp_text[start_susp]):
                            start_susp = start_susp + 1
                            start_src = start_src + 1
                            while (start_susp < len(susp_text) and
                                   susp_text[start_susp] in DELETECHARS):
                                start_susp = start_susp + 1
                            while (start_src < len(src_text) and
                                   src_text[start_src] in DELETECHARS):
                                start_src = start_src + 1
                        if (start_src - 1) - token[0][0] > d[0][1] - d[0][0]:
                            d = ((token[0][0], start_src), (t[0], start_susp))
                    detections.append(d)
                    skipto = d[0][1]
                    if skipto < len(src_text):
                        token = [(skipto, src_text[skipto])]
                    else:
                        break
                else:
                    token = token[1:]

    sum_diff = sum([t[1][1] - t[1][0] for t in detections])

    return sum_diff


final_path = sys.argv[1]
draft_path = sys.argv[2]

final_docs = traverse(final_path) 
draft_docs = traverse(draft_path)

for i in range(1,len(final_docs)+1): 
    f = load_text(final_path+'/'+sorted(final_docs)[i-1])
    d = load_text(draft_path+'/'+sorted(draft_docs)[i-1])
    tokenized_d = tokenize(d,LENGTH)
    print(sorted(final_docs)[i-1],
          sorted(draft_docs)[i-1],
          compare(f,d,tokenized_d)/len(f))


