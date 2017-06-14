import json
keyword = 'ACE'
with open('pbabstract1.json') as data_file:    
    data = json.load(data_file)
    #pick snippets related to ACE inhibitors
    for i in range(len(data.keys())):
        try:
            if keyword in data[str(i)]:
                print data[str(i)] + '\n'
            else:
                next
        except:
            next