from bottle import route, run, template
from json import dumps
from bottle import response,get, request
import sys
from subprocess import call
import subprocess
import os
import re

@route('/hello')
def index():
    
    return "Hello"
    #rv = [{ "id": 1, "name": "Test Item 1" }, { "id": 2, "name": "Test Item 2" }]
    #response.content_type = 'application/json'
    #return dumps(rv)



@get('/runquery')
def runquery():

    #const values
    cp  ='/home/william/lucene-7.2.1/queryparser/lucene-queryparser-7.2.1.jar:/home/william/lucene-7.2.1/core/lucene-core-7.2.1.jar'
    pSearchPath = 'ProtocolSearch'
    pFolder = '/data/william/pubmed/protocols/'
    lines = []

    #form params
    fileName = request.query['filename']
    number = request.query['amount']

    #add file to json object
    lines.append({"ProtocolFile" : fileName})

    #append the file name
    fileName = pFolder + fileName

    #add key word extension
    fileName += ".kwq"

    #invoke java process
    output = subprocess.check_output(["java", pSearchPath, "-protocol", fileName, "-number", number])
    output = output.decode("utf-8") 

    #print(str(output))

    #write the origial content
    lines.append({"FileContent" : open(fileName).read()})
    ranks = []
    

    for line in str(output).split(os.linesep):
        elements = line.split('\t')
 
        
        if(len(elements) == 2):
            ranks.append({"pmid": elements[0], "score" : elements[1]})


    

    lines.append({"Ranks" : ranks})
    response.content_type = 'application/json'
    return dumps(lines)


run(host='0.0.0.0', port=2000)