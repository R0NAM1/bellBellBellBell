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

myIpAddress = '10.42.0.8' # Put in the address on the interface you want to use
bellExtension = 6001 # INT # Extension to call that will act as the bell interface
sipUsername = '9010'
sipPassword = 'password'
sipServer = '10.36.0.50'
sipServerPort = 5060
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

def attemptCall(phoneObject):
    print("-- Dialing Specified SIP Extension " + str(bellExtension) + ".")
    counter = 1
    callHappened = False # Failsafe so we don't accidently double call
    
    # Open and read the audio file into memory
    f = wave.open(bellWav, 'rb')
    frames = f.getnframes()
    wavdata = f.readframes(frames)
    f.close()
    # print("-- WAV read into as a " + str(len(wavdata)) + " byte long array")
    
    while True:
        try:
            if callHappened:
                break
            
            print("===============================")
            print("---- Attempt " + str(counter) + "...")
            
            if (counter > 10):
                print("---- Over 10 Attempts! Abandoning all hope! (breaking)")
                break            
            
            # Dial extension 9000
            mycall = phoneObject.call(bellExtension)
            
            # Wait for the call to connect
            while mycall.state != CallState.ANSWERED:
                time.sleep(0.1)
            print("---- Call answered! Waiting 2 seconds to let stream stabilize...")
            time.sleep(2) # Waiting 2 seconds to let stream stabilize

            # Play the audio over the SIP call
            print("---- Writing audio to SIP stream...")
            mycall.write_audio(wavdata)
            print("---- Audio written to SIP stream!")
            callHappened = True
            
            # Wait for the audio to finish playing
            stop = time.time() + (frames / 8000)
            while time.time() <= stop:
                time.sleep(0.1)


            print("---- Audio should have played all the way, hanging up...")
            print("======================================================")
            print("")
            
            # Hang up the call
            mycall.hangup()
            # Sleep for an additional two seconds...
            time.sleep(2)
            phoneObject.stop()
            break # Break out of forever loop
            
        except Exception as e:
            print(f"!! An error occurred: {e}")
            print("Traceback follows as: " + str(traceback.format_exc()))
            counter = counter + 1
            time.sleep(1)

# Main loop
# Single threaded so while True is acceptable here since SIGINT will be caught just fine
if __name__ == '__main__':
    print("===== Simple bellBellBellBell started! =====")
    print("Note: 500 message is from the pyVoIP library")
    
    while True:
        # Loop start!
        # Sleep for 1 second
        time.sleep(1)
        
        current_date = datetime.today()
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
                print("-- Time to ring bell at " + formatted_time + " on " + formatted_date + "!")
                
                # We just regegister every time so we don't have to deal with the registration expiring, which happens!
                phoneObject = VoIPPhone(
                    sipServer,
                    sipServerPort,
                    sipUsername,
                    sipPassword,
                    myIP=myIpAddress
                )
                
                phoneObject.start()
                print("-- Phone object created, registered & started, attempting call!")
                
                attemptCall(phoneObject)
                print("-- Call done! Sleeping for 60 seconds to not ring again...")
                
                # Bell has rung! Wait 60 seconds to it's sure for an entire minute to pass, people don't put bells 3 minutes apart, 
                time.sleep(60)
                
                # Continue loop!