from datetime import datetime
from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import pandas
import time
import wave
import traceback

## Simple Bell is a simple loop that checks every second if this minute has a bell associated
## If so then ring the bell and flag it's been rung this minute
## When the minute rolls over force set the flag to false
## Also check if it is Sun - Sat, only work on configured days

bellExtension = '6000' # Extension to call that will act as the bell interface
sipUsername = '9010'
sipPassword = 'password'
sipServer = '10.36.0.50'
bellWav = 'bell.wav' # MUST BE 8000hz mono

# Comment out days that don't need to ring
daysToRing = [
#    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday"
#    "Friday",
#    "Saturday" 
]

# Time is in 24HR Format,
# Input like: "08:15" "15:30"
# NORMAL SCHEDULE
timesToRing = [
    "08:10",
    "08:15",
    "09:10",
    "09:14",
    "10:09",
    "10:13",
    "11:08",
    "11:12",
    "12:07",
    "12:37",
    "12:41",
    "13:36",
    "13:40",
    "14:35",
    "14:39",
    "15:30"
]

def answerCallback():
    try:
        # Dial extension 9000
        print("-- Dialing Specified SIP Extension " + bellExtension + ".")
        call.dial("sip:" + bellExtension + "@" + sipServer)
        
        # Wait for the call to connect
        while call.state != CallState.ANSWERED:
            time.sleep(0.1)
        print("-- Call answered!")

        # Open and read the audio file into memory
        f = wave.open(bellWav, 'rb')
        frames = f.getnframes()
        data = f.readframes(frames)
        f.close()
        print("-- WAV read into memory, playing over active SIP connection.")

        # Play the audio over the SIP call
        call.write_audio(data)

        # Wait for the audio to finish playing
        stop = time.time() + (frames / 8000)
        while time.time() <= stop and call.state == CallState.ANSWERED:
            time.sleep(0.1)

        print("-- WAV read into SIP connection, hanging up!")
        
        # Hang up the call
        call.hangup()
        
    except Exception as e:
        print(f"!! An error occurred: {e}")
        print("Traceback follows as: " + str(traceback.format_exc()))
        call.hangup()

# Main loop
# Single threaded so while True is acceptable here since SIGINT will be caught just fine
if __name__ == '__main__':
    print("Simple bellBellBellBell started!")
    print("")
    
    while True:
        # Loop start!
        # Sleep for 1 second
        time.sleep(1)
        
        current_date = date.today()
        formatted_date = current_date.strftime("%Y-%m-%d")
        dayOfTheWeek = pandas.to_datetime(formatted_date)
        
        # Check if it's a day we can ring the bell
        if (dayOfTheWeek.day_name()) in daysToRing:
        
            # Check if this minute is in timesToRing
            current_time = datetime.now()
            rounded_minute = current_time.replace(second=0, microsecond=0)
            formatted_time = rounded_minute.strftime("%H:%M")
            
            if formatted_time in timesToRing:
                # We are in a ringable minute and need to ring the bell!
                print("Time to ring bell at " + formatted_time + " on " + formatted_date + "!")
                # Bell has rung! Wait 60 seconds to it's sure for an entire minute to pass, people don't put bells 3 minutes apart, 
                # always 5!
                
                phone = VoIPPhone(
                    sipServer,
                    "6000",
                    sipUsername,
                    sipPassword,
                    myIP="<Your computer's local IP>",
                    callCallback=answerCallback
                )
                
                phone.start()
                time.sleep(10)
                phone.stop()
                
                print("-- Sleeping for 60 seconds to not ring again...")
                time.sleep(50)
                # Continue loop!