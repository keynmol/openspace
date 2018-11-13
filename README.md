# Open Space

# Deploy script (MacOS only)

Sometimes it's useful to deploy the same app to multiple Microbits whilst having each Microbit know its internal ID. Or you want to pass a set of parameters without actually changing the program code. 

To achieve this:

1. Create your `hello.py` (name doesn't matter) that has a specific placeholder. Here's an example:

	```python
	from microbit import *

	# Parameters definition
	WORKER_ID=""
	ACCURACY=""


	# Program starts here

	worker_id = int(WORKER_ID)
	accuracy = int(ACCURACY)

	display.show(WORKER_ID)
	```
2. Run `deploy.py`:
	
	```
	$ python deploy.py hello.py --ACCURACY 5.0
	uflash hello.pyDELETE_ME1.py "/Volumes/MICROBIT 1"
	uflash hello.pyDELETE_ME0.py "/Volumes/MICROBIT"
	uflash hello.pyDELETE_ME3.py "/Volumes/MICROBIT 3"
	uflash hello.pyDELETE_ME2.py "/Volumes/MICROBIT 2"
	# Parameter WORKER_ID was successfuly replaced with "2"
	# Parameter ACCURACY was successfuly replaced with "5.0"
	```

	Here I have 4 Microbits connected - all of them were picked up by the script, different versions of the program were created and in which the placeholder WORKER_ID was replaced with respective ID of the device (from 0 to 4) and ACCURACY was replaced with "5.0" - value specified in CLI

	Note: you can pass any extra parameters to `deploy.py`. If the name matches a placeholder in your target program, it will be replaced. If no, an error will be output.

The script outputs the commands you can just run and everything will be flashed to the devices according to their IDs.