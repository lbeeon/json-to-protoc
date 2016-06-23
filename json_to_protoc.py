import os
import json
import time
import re

def get_protoc(json_data, doc_stack):
	ret = ''
	seed = 0
	for key in json_data:
		seed += 1
		if isinstance(json_data[key], bool):
			ret += "  required bool {} = {};\n".format(key, seed)
			continue

		if isinstance(json_data[key], str) or isinstance(json_data[key], unicode) :
			ret += "  required string {} = {};\n".format(key, seed)
			continue

		if isinstance(json_data[key], int):
			ret += "  required int64 {} = {};\n".format(key, seed)
			continue

		if isinstance(json_data[key], float):
			ret += "  required double {} = {};\n".format(key, seed)
			continue

		if isinstance(json_data[key], dict):
			ret += "  required {} {} = {};\n".format(key.title(), key, seed)
			doc_stack.append({"key":key, "json":json.dumps(json_data[key])})
		
		if isinstance(json_data[key], list):
			if len(json_data[key]) == 0: #default int array
				ret += "  repeated int64 {} = {};\n".format(key, seed)
				continue
			else:
				if isinstance(json_data[key][0], bool):
					ret += "  repeated bool {} = {};\n".format(key, seed)
					continue
				elif isinstance(json_data[key][0], int):
					ret += "  repeated int64 {} = {};\n".format(key, seed)
					continue
				elif isinstance(json_data[key][0], float):
					ret += "  repeated double {} = {};\n".format(key, seed)
					continue
				elif isinstance(json_data[key][0], str) or isinstance(json_data[key][0], unicode):
					ret += "  repeated string {} = {};\n".format(key, seed)
					continue
				elif isinstance(json_data[key][0], dict):
					ret += "  repeated {} {} = {};\n".format(key.title(), key, seed)
					doc_stack.append({"key":key, "json":json.dumps(json_data[key][0])})
					continue
	return ret

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def remove_comments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
    return string
		
if __name__ == '__main__':
	#json_data = '{"id":"4930635cf5d843eabc74ef8bb6ff7a29","product_id":"f71407577bb6479993bd09fcd9413039","retail_price":351.09736607491345,"type":{"color":"Turquoise","size":"M"}}'
	#json_data = '{"timestampValue":{"seconds":1480291200},"variants":[{"id":"4930635cf5d843eabc74ef8bb6ff7a29","product_id":"f71407577bb6479993bd09fcd9413039","retail_price":351.09736607491345,"type":{"color":"Turquoise","size":"M"}},{"id":"18f4f000403b439b99e3397ab90bf83a","product_id":"85779bec89c14bc78f3a56103a87854b","retail_price":882.9315997833187,"type":{"color":"Pink","size":"M"}}]}'
	# ret = 'message User{ \n'
	# doc_stack = list()
	# obj = json.loads(json_data)
	# ret += get_protoc(obj, doc_stack) + '}\n\n' 
	# while len(doc_stack) > 0:
	# 	obj = doc_stack.pop()
	# 	ret += 'message {} {{\n'.format(obj["key"])
	# 	obj = json.loads(obj["json"])
	# 	ret += get_protoc(obj, doc_stack) + '}\n\n'
	# print ret

	dir_path = './json_file'
	out_path = './protoc_file/'
	for filename in listdir_fullpath(dir_path):
		if filename.endswith(".json"):
			with open(filename) as data_file:
				basename = os.path.basename(filename)
				output_name = os.path.splitext(basename)[0]+'.protoc'
				doc_stack = list()
				data = str(data_file.read())
				print basename
				data = remove_comments(data)
				#print data
				data = json.loads(data)
				result ='message {} {{\n'.format(os.path.splitext(basename)[0])
				result += get_protoc(data, doc_stack) + '}\n\n'
				while len(doc_stack) >0:
					data = doc_stack.pop()
					result += 'message {} {{\n'.format(data["key"].title())
					data = json.loads(data["json"])
					result += get_protoc(data, doc_stack) + '}\n\n'
				output_name = os.path.splitext(basename)[0]+'.protoc' 
				f = open(out_path + output_name, 'w')
				f.write(result)
				f.close()
			
