import client
import json
import sys

if len(sys.argv) != 2:
	print "Wrong command line"
	sys.exit(0)

file_name=sys.argv[1]

print "Uploading NF template available in file" + file_name + "..."

template = open(file_name)
myClient=client.Client("http://127.0.0.1:8081")
ret = myClient.put_template("qwerty",json.dumps(json.load(template)))

print "Answer from the datastore: " + str(ret.status_code)
