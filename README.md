# Open Space

# Deploy script (MacOS only)

Sometimes it's useful to deploy the same app to multiple Microbits whilst having each Microbit know its internal ID. To achieve this:

1. Create your `hello.py` (name doesn't matter) that has a specific placeholder. Here's an example:

	```python
	from microbit import *

	WORKER_ID=0 # <- placeholder, the line must contain "WORKER_ID=0"

	display.show(WORKER_ID)
	```
2. Run `deploy.py`:
	
	```
	$ python deploy.py hello.py
	uflash hello.pyDELETE_ME1.py "/Volumes/MICROBIT 1"
	uflash hello.pyDELETE_ME0.py "/Volumes/MICROBIT"
	uflash hello.pyDELETE_ME3.py "/Volumes/MICROBIT 3"
	uflash hello.pyDELETE_ME2.py "/Volumes/MICROBIT 2"
	```

	Here I have 4 Microbits connected - all of them were picked up by the script, different versions of the program were created and in which the placeholder was replaced with respective ID of the device (from 0 to 4).

The script outputs the commands you can just run and everything will be flashed to the devices according to their IDs.