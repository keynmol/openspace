import glob
import re
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('program')
parser.add_argument('--offset', type=int, default=0)

(args, params) = parser.parse_known_args()


def create_parameters_map(unparsed):
	return dict([(re.sub("--", "", i), k) for i,k in zip(unparsed[0::2], unparsed[1::2])])

def get_devices():
	return glob.glob("/Volumes/MICROBIT*")

def id_devices(devices, offset):
	def extract(d):
		match = re.match(r'.*MICROBIT(\s*\d*)', d)
		ze_match = match.group(1).strip()
		if ze_match == "":
			return offset
		else:
			return offset + int(ze_match)

	return dict([(str(extract(d)), d) for d in devices])

def set_program_parameters(code_lines, parameters):
	new_code_lines = []
	parameters_handled = dict([p, None] for p in parameters.keys())
	
	for l in code_lines:
		new_line = l
		for name, value in parameters.items():
			placeholder = "{}=\"\"".format(name)
			if placeholder in new_line:
				new_value = re.sub('"', '\"', value)
				new_line = re.sub(placeholder, '{}="{}"'.format(name, new_value), l)
				parameters_handled[name] = '"{}"'.format(new_value)
		new_code_lines.append(new_line)

	return (new_code_lines, parameters_handled)


def create_program_version(source_file, parameters):
	result_file_name = source_file + "DELETE_ME" + str(id) + ".py"
	handled_parameters = None
	with open(source_file, "r") as f_read:
		with open(result_file_name, "w") as f_write:
			original_lines = f_read.readlines()
			(modified_lines, handled_parameters) = set_program_parameters(original_lines, parameters)

			for l in modified_lines:
				f_write.write(l)
	return (result_file_name, handled_parameters)

device_mapping = id_devices(get_devices(), args.offset)

for id, device in device_mapping.items():
	parameters = create_parameters_map(params)
	parameters.update({"WORKER_ID":str(id)})
	
	(file_name, handled) = create_program_version(args.program, parameters)
	command = "uflash {0} \"{1}\"".format(file_name, device)

	print(command)

for name, value in handled.items():
	if not value:
		print("# WARNING: parameter {} was not found in source file".format(name))
	else:
		print("# Parameter {} was successfuly replaced with {}".format(name, value))

