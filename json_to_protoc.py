import os
import json
import time
import re

def get_protoc(json_data, doc_stack, is_required):
	ret = ''
	required = "required " if is_required else "optional"
	seed = 0
	for key in json_data:
		seed += 1
		if isinstance(json_data[key], bool):
			ret += "  {}bool {} = {};\n".format(required, key, seed)
			continue

		if isinstance(json_data[key], str) or isinstance(json_data[key], unicode) :
			ret += "  {}string {} = {};\n".format(required, key, seed)
			continue

		if isinstance(json_data[key], int):
			ret += "  {}int64 {} = {};\n".format(required, key, seed)
			continue

		if isinstance(json_data[key], float):
			ret += "  {}double {} = {};\n".format(required, key, seed)
			continue

		if isinstance(json_data[key], dict):
			ret += "  {}{} {} = {};\n".format(required, capitalize(key), key, seed)
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
					ret += "  repeated {} {} = {};\n".format(capitalize(key), key, seed)
					doc_stack.append({"key":key, "json":json.dumps(json_data[key][0])})
					continue
	return ret

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def remove_comments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
    return string
	
def capitalize(string):
	return string[0].upper() + string[1:]
		
if __name__ == '__main__':
	template = 'syntax = "proto3"\n\n'
	template += 'package {{package name}}\n\n'
	
	# template += 'import "github.com/gogo/protobuf/gogoproto/gogo.proto";\n\n'
	# template += 'option (gogoproto.equal_all) = true;\n'
	# template += 'option (gogoproto.verbose_equal_all) = true;\n'
	# template += 'option (gogoproto.goproto_stringer_all) = false;\n'
	# template += 'option (gogoproto.stringer_all) =  true;\n'
	# template += 'option (gogoproto.populate_all) = true;\n'
	# template += 'option (gogoproto.testgen_all) = true;\n'
	# template += 'option (gogoproto.benchgen_all) = true;\n'
	# template += 'option (gogoproto.marshaler_all) = true;\n'
	# template += 'option (gogoproto.sizer_all) = true;\n'
	# template += 'option (gogoproto.unmarshaler_all) = true;\n\n\n'
	
	is_required = raw_input('All field required? (defalut==required) (1 => True, 2 => False\n')
	is_required = False if is_required == "2" else True
	dir_path = './json/'
	out_path = './protoc/'
		
	for filename in listdir_fullpath(dir_path):
		if filename.endswith(".json"):
			with open(filename) as data_file:
				basename = os.path.basename(filename)
				output_name = os.path.splitext(basename)[0]+'.protoc'
				doc_stack = list()
				data = str(data_file.read())
				data = remove_comments(data)
				data = json.loads(data)
				result ='message {} {{\n'.format(capitalize(os.path.splitext(basename)[0]))
				result += get_protoc(data, doc_stack, is_required) + '}\n\n'
				while len(doc_stack) >0:
					data = doc_stack.pop()
					result += 'message {} {{\n'.format(capitalize(data["key"]))
					data = json.loads(data["json"])
					result += get_protoc(data, doc_stack, is_required) + '}\n\n'
				output_name = os.path.splitext(basename)[0]+'.protoc' 
				if not os.path.exists(out_path):
				    os.makedirs(out_path)
				f = open(out_path + output_name, 'w')
				f.write(template)
				f.write(result)
				f.close()
			
