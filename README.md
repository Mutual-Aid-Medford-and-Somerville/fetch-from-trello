# Get Trello Tasks

Want to generate a read-out of the current MAMAS Trello tasks? Look no further!

## Setup

1. Clone this repository, then install the python dependencies required to run this script.
2. Create an `.ini` file to contain the requisite sensitive variables. The file should look like this:

	```
	[TRELLO]
	KEY = <key>
	TOKEN = <key>
	
	[MAMAS]
	TECH_TEAM = <key>
	
	[BOARDS]
	IN_PROGRESS = <key>
	FINISHED = <key>
	```

3. Run the python script with an environment variable for your `.ini` file. For example, if you called your file `config.ini`:

	```
	CONFIG=config.ini python fetch-from-python.md
	```

4. Look for the Markdown file created by the script and named in the script output!
