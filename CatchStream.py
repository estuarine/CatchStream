#!/usr/bin/python
import os
import sys
import time
from datetime import timedelta

"""This program records an Internet radio stream for a length of time 
designated by the user. It uses mplayer to save the stream as a wav file. 
At the end of the designated time, recording stops, the wav file is 
converted to mp3 using the lame encoder, and the original wav is deleted.

The script also tries to offer some safeguards against the hiccups and 
interruptions to which streaming audio is prone. Specifically, after the 
recording/conversion/deletion process has finished, the script checks to 
make sure the recording didn't end too soon. If it did, the stream 
relaunches and the recording process starts over again -- and again and 
again, if necessary. The second and subsequent recordings in this cycle 
are assigned to similar, though not identical, timestamped file names to
avoid overwriting the earlier recordings.


USAGE

The script can be invoked like so:

	python CatchStream.py [station] [period]

The allowable options for "station" are KCRW (in Santa Monica, CA), WFMU 
(Jersey City), WPRB (Princeton) and SomaFM (San Francisco -- specifically 
the Indie Pop Rocks channel). Feel free to add any others that catch your 
fancy; you will need to know the stream URL. 

The time period (if the user provides one) must be in the format hh:mm:ss 
or the script will abort.

If the station and period are not specified in the command line, the script 
will default to recording WFMU for half an hour. So:

	python CatchStream.py

is equivalent to:

	python CatchStream.py WFMU 00:30:00

You can also specify the station but not the time period, in which case the 
script will again default to half an hour:

	python CatchStream.py KCRW
	
is equivalent to:

	python CatchStream.py KCRW 00:30:00
	


ADDITIONAL NOTES

This script was written on a computer running Ubuntu Linux, and it uses system 
calls for some of the most crucial operations, so YMMV if you're trying to use 
this with Windows or OS X. Mplayer and lame must be installed, obviously.

One way this script could prove useful is to use the cron scheduling program 
(in Linux, OS X or some other Unix-like environment) to run the script at a 
particular time/date. For instance, you could tell cron to schedule a recording 
for two hours starting at 3 p.m. every Sunday. This can be especially helpful 
if your favorite online radio show is not available as a podcast. 

-- by Bob King, 2/22/2010 """ 


##########################################################################
##                                                                      ##
## Function to convert the user's specified time period from a string   ##
## to a datetime.timedelta object that Python can make some use out of. ##
## It throws a fatal exception if the time period doesn't follow the    ##
## format 'hh:mm:dd.'                                                   ##
##                                                                      ##
##########################################################################

def timeParse(timeString):

	try:
		timeParts = timeString.split(":")
		hrs, mins, secs = [int(t) for t in timeParts]
		timeResult = timedelta(hours = hrs, minutes = mins, seconds = secs)
		return timeResult
		
	except:
		print "\nInvalid format for time: %s!\n" % timeString	
		sys.exit()



##########################################################################
##                                                                      ##
## This next function is the crucial one that grabs the audio stream,   ##
## saves it to the hard drive and then converts the saved wav file to   ##
## mp3 (finally deleting the much bulkier wav at the end).              ##
##                                                                      ##
## The function also relaunches itself recursively if the recording     ##
## process is ended early, perhaps by an interruption in the stream.    ##
## It's meant to relaunch repeatedly until the user-allotted time has   ##
## expired. While the timing process is far from flawless (it doesn't   ##
## take into account the time needed to buffer the stream at the        ##
## beginning or do the lame conversion at the end), it should be better ##
## than losing 90 percent of the recording because the stream hiccupped ##
## near the beginning.                                                  ##
##                                                                      ##
##########################################################################

# Station is the name of the radio station, which also serves as the base
# for the recordings' file names.

# Url is the url for the audio feed

# timePlanned is the length of time the recording is supposed to last

# timeStarted is the time when the recording (or this iteration of it, 
# at least) began


def grabStream(station, url, timePlanned, timeStarted):

	# These commands are all system calls that work in Linux. 
	# Again, YMMV w/ Windows or Mac.

	# With mplayer, we use the -endpos option to specify how long the 
	# recording should be. Mplayer saves the recording to a file with a 
	# name like KCRW.wav, WFMU.wav, etc. We also set the mplayer cache 
	# at 4096 KBytes to minimize hiccups.
	
	# Then lame converts the wav file to an identically named mp3. 
	# The -V 0 option calls for a high-quality variable-bitrate recording. 
	# You can delete this option if you'd prefer the default of 128kpbs, 
	# which would yield a smaller file.
	
	# rm is simply the Linux/Unix command to delete the original wav file. 
	# You'll need to change this line if you're trying to run this script 
	# on a Windows computer.
	 

	commands = [ 'mplayer -endpos "%s" -cache 4096 -vc null -vo null -ao pcm:waveheader:file=%s.wav %s' % (timePlanned, station, url), \
	             'lame -V 0 %s.wav %s.mp3' % (station, station), \
	             'rm %s.wav' % station ]


	# Run the commands one at a time.

	for command in commands:
		print "\n%s\n" % command
		os.system(command)

	# Now check to see if we used all the allotted time.
		
	timeEnded = time.time()
	timeElapsed = timedelta(seconds = (timeEnded - timeStarted) )
	print "Streaming ended after %s (%s had been planned.)" % (timeElapsed, timePlanned)
		

	# If recording ended early, relaunch the stream	
	
	if timeElapsed < timePlanned:
		print "Resuming stream!\n"
		
		# Create newtimePlanned to shorten the recording period, 
		# subtracting the time we've already spent. (If we're 40 
		# minutes into an hour-long recording, for example, we 
		# just need 20 more minutes.
		#
		# newtimeStarted (i.e., now) restarts the recording clock. 
		
		newtimePlanned = timePlanned - timeElapsed
		newtimeStarted = time.time()
		
		# Time-stamp the name of the next recording file so we don't 
		# overwrite the one we just created. For instance, the first file 
		# created during this session might be called KCRW.mp3. The second one 
		# could end up being KCRW1234567.mp3. (But note: If you exit the 
		# script and start it all over again, you will create a new 
		# KCRW.mp3 that will overwrite any you created during an 
		# earlier session.)
		
		timeString = "%s" % int(newtimeStarted)
		newstation = station[:4] + timeString
		
		# The grabStream function now calls itself using
		# the newly generated options.
		
		print "New file: %s.wav\n" % newstation
		grabStream(newstation, url, newtimePlanned, newtimeStarted)


##########################################################################
##########################################################################
##########################################################################
##                                                                      ##
##                       *** MAIN PROGRAM ***                           ##
##                                                                      ##
##########################################################################
##########################################################################
##########################################################################


# Dictionary contains names and URLs of selected online radio stations
# This script has worked well with mp3 and aacplus streams. It has
# experienced problems with Real and Windows Media streams.

stations = { 'KCRW'   : 'http://media.kcrw.com/live/kcrwlive.pls', \
             'WFMU'   : 'http://stream0.wfmu.org/freeform-128k', \
             'WPRB'   : 'http://stardust.wavestreamer.com:2152/1', \
             'SomaFM' : 'http://somafm.com/indiepop130.pls' }
             
try:
	station = sys.argv[1]
except:
	station = "WFMU"
	
try:
	url = stations[station]
except:
	print "\nSorry! I don't know anything about %s!\n" % station
	sys.exit()
	
try:
	timeString = sys.argv[2]
except:
	timeString = "0:30:00"

timePlanned = timeParse(timeString)                
timeStarted = time.time()
print "\n*** Recording %s for %s. ***\n" % (station, timePlanned)

grabStream(station, url, timePlanned, timeStarted)
