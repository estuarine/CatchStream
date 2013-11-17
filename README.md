CatchStream
===========

This Python script captures an Internet radio stream for a length of time 
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

-- by Bob King, 2/22/2010
