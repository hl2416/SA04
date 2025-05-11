import os
import sys
import csv

# function that reads in a file name argument for getting the required info from the file and printing it in the terminal as well as exporting it into a csv file
def parseLog(fileName):
	log = []
	ip = ""
	dupeIP = -1
	logNum = 0
	count = 1
	f = ""
	
	# opens the file name that was read in from the argument
	f = open(fileName, "r")
	line = f.readline().strip()
	
	# continues reading line by line as long as it isn't empty
	while line:
		# grabs the line
		line = f.readline().strip()
		# checks to see if the line has the string "Failed password for" for failed login attempts
		if "Failed password for" in line:
			# sets the ip address for this line using substring
			ip = line[line.find("from ") + len("from "):line.rfind(" port")]
			# if the list log is empty, it will create a new list with the start of the count and ip address to append to log
			if not log:
				FLA = []
				FLA.append(count)
				FLA.append(ip)
				log.append(FLA)
			# if the list log is not empty
			else:
				# checks to see if there is already a list in log with the same ip address and saves the index of the list
				for i in range(0, len(log)):
					if ip == log[i][1]:
						dupeIP = 1
						logNum = i
				# if there is a dupe, that list's count will only be incremented by 1
				if dupeIP == 1:
					log[logNum][0] = log[logNum][0] + 1
					dupeIP = -1
				# if this is a new ip address, creates a new list with a new count and the ip address which is then appended into log
				else:
					FLA = []
					FLA.append(count)
					FLA.append(ip)
					log.append(FLA)
	# reverse sorts log according to count
	sLog = sorted(log, key=lambda x: x[0], reverse=True)
	# header for terminal output
	print("Count,IP,Location")
	
	# opens a new csv file to write the output into
	with open("SA04Output.csv", "w") as output:
		wFLA = csv.writer(output, delimiter=",")
		
		# writes the first row of csv file with the headers
		wFLA.writerow(["Count","IP Address","Location"])
		# iterates through all the lists in slog which is the sorted log list
		for j in range(0, len(sLog)):
			# only prints and writes the info from the list if the count is greater than 10
			if sLog[j][0] > 10:
				# gets the output of geoiplookup as the country
				country = os.popen("geoiplookup " + sLog[j][1]).read().strip()
				# prints the count, ip address, and the country found in geoiplookup in the terminal
				print(str(sLog[j][0]) + "," + sLog[j][1] + "," + country[country.find(", ") + len(", "):])
				# writes the count, ip address, and the country into the csv file
				wFLA.writerow([sLog[j][0],sLog[j][1],country[country.find(", ") + len(", "):]])

# checks to see if there is an argument for the file
if len(sys.argv) < 2:
	print("Please enter a file")
	exit(1)
# tries to open the file name from the argument and prints an error message if it could not be opened
try:
	f = open(sys.argv[1], "r")
except IOError:
	print("Cannot open a log file: " + sys.argv[1])
	exit(1)
# calls the function above when the file name is valid
parseLog(sys.argv[1])
