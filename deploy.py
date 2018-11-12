import glob
import re
import sys

PROGRAM_NAME = sys.argv[1]
OFFSET=0

try:
	off = int(sys.argv[2])
	OFFSET = off
except:
	OFFSET=0

def get_devices():
	return glob.glob("/Volumes/MICROBIT*")

def id_devices(devices):
	def extract(d):
		match = re.match(r'.*MICROBIT(\s*\d*)', d)
		ze_match = match.group(1).strip()
		if ze_match == "":
			return OFFSET
		else:
			return OFFSET + int(ze_match)

	return dict([(str(extract(d)), d) for d in devices])

def set_program_id(code_lines, id):
	new_lines = []
	for l in code_lines:
		new_line = l
		if "WORKER_ID=0" in l:
			new_line = re.sub("WORKER_ID=0", "WORKER_ID=" + str(id), l)
		new_lines.append(new_line)

	return new_lines

def create_program_version(source_file, id):
	result_file_name = source_file + "DELETE_ME" + str(id) + ".py"
	with open(source_file, "r") as f_read:
		with open(result_file_name, "w") as f_write:
			original_lines = f_read.readlines()
			modified_lines = set_program_id(original_lines, id)

			for l in modified_lines:
				f_write.write(l)
	return result_file_name

device_mapping = id_devices(get_devices())

for id, device in device_mapping.items():
	file_name = create_program_version(PROGRAM_NAME, id)
	command = "uflash {0} \"{1}\"".format(file_name, device)

	print(command)

