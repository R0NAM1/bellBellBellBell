from datetime import datetime
import pjsua2 as pj
import pandas
import time
import traceback
import subprocess

## Simple Bell is a simple loop that checks every second if this minute has a bell associated
## If so then ring the bell and flag it's been rung this minute
## When the minute rolls over force set the flag to false
## Also check if it is Sun - Sat, only work on configured days
# This version is a rewrite from using pyVoIP to PjSIP

# Related settings
bellExtension = 425 # INT # Extension to call that will act as the bell interface
sipUsername = '420'
sipPassword = 'password'
sipServer = '10.1.2.3'
sipServerPort = 5060
bellWav = 'sounds/bells/default_bell_2s.wav' # MUST BE 16000hz mono, default file has 2 second delay at start
useMulticast = True #Overrides SIP account and uses muticast with pcm_mulaw audio
multicastAddress = '237.100.100.100'
multicastPort = 25311

# Comment out days that don't need to ring
daysToRing = [
    # "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday"
    # "Friday",
    # "Saturday" 
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

# Subclass to extend the Account and get notifications etc.
class Account(pj.Account):
  def onRegState(self, prm):
      print("***OnRegState: " + prm.reason)

class MyCall(pj.Call):
    def __init__(self, acc, dest_uri):
        pj.Call.__init__(self, acc)
        self.dest_uri = dest_uri
    # Add call reject handling!
    def on_state(self):
        if self.info().state == pj.PJSIP_INV_STATE_CALLING:
            print("Invalid State Calling Error", self.dest_uri)
        elif self.info().state == pj.PJSIP_INV_STATE_INCOMING:
            print("Invalid State Incoming Error", self.info().remote_uri)
            # self.answer()
        elif self.info().state == pj.PJSIP_INV_STATE_EARLY:
            pass
        elif self.info().state == pj.PJSIP_INV_STATE_CONNECTING:
            pass
        elif self.info().state == pj.PJSIP_INV_STATE_CONFIRMED:
            print("Call Connected, should I play audio now?...")
            # self.start_audio("testeaudio.wav")
        elif self.info().state == pj.PJSIP_INV_STATE_DISCONNECTED:
            print("Channel deleted, reason:", self.info().last_reason)
            self.delete()
            
# AudioMediaPlayer subclass to let me know when the WAV file is done playing
class AudioMediaPlayer(pj.AudioMediaPlayer):
    def __init__(self):
        pj.AudioMediaPlayer.__init__(self) # Init parent class
        self.is_end_of_file = False
        
    def onEof2(self):
        print("-- Setting EOF flag --")
        self.is_end_of_file = True

def attemptSIPCall(account):
    print("-- Dialing Specified SIP Extension " + str(bellExtension) + ".")
    counter = 1
    callHappened = False # Failsafe so we don't accidently double call
    
    while True:
        try:
            if callHappened:
                break
            
            print("------------------------------------")
            print("---- Attempt " + str(counter) + "...")
            
            if (counter > 12):
                print("---- Over 12 Attempts! Abandoning all hope! (breaking)")
                break            
            
            # Dial Bell extension
            dest_uri = "sip:" + str(bellExtension) + "@" + sipServer
            print("---- Calling " + dest_uri)
            call = MyCall(account, dest_uri)
            prm = pj.CallOpParam(True) # Default settings
            call.makeCall(dest_uri, prm)
            
            print("---- Call made! Waiting for call to be answered for 20000 cycles....")
            # Wait until call is answered....
            
            answerCounter = 1
            while True:
                
                # Check if call even still exists or if was rejected
                try:
                    ci = call.getInfo()
                except:
                    print("!!! | Exception raised waiting for call to be answered, happens if call disconnects!")
                    print("!!! | Going to treat this as a failed attempt, trying next attempt in 5 seconds")
                    time.sleep(5)
                    # End attempt
                    break
                
                if answerCounter == 20000:
                    print("Waited 20000 cycles for call to be answered but it wasn't. Breaking!")
                    break
                elif(ci.stateText == "CONFIRMED"):
                    print("-- Call was answered!!!")
                    break
                else:
                    time.sleep(0.01)
                    if answerCounter == 500:
                        print("-- 500 out of 20000 call checks...")
                    elif answerCounter == 1000:
                        print("-- 1000 out of 20000 call checks...")
                    elif answerCounter == 10000:
                        print("-- 10000 out of 20000 call checks...")
                    elif answerCounter == 15000:
                        print("-- 15000 out of 20000 call checks...")
                    answerCounter = answerCounter + 1
            
            # Give PJSIP time to process all this in the background
            time.sleep(0.2)
            
            # Play the audio over the SIP call
            ci = call.getInfo()
            mi = ci.media[0]
            m = call.getMedia(mi.index)
            am = pj.AudioMedia.typecastFromMedia(m)
            
            print("---- Writing audio to SIP stream in real time...")
            wav_player = None
            wav_player = AudioMediaPlayer()
            wav_player.createPlayer(bellWav, True)
            wav_player.startTransmit(am)
            
            # Wait for the audio to finish playing
            wavCount = 0
            while True:
                if wav_player.is_end_of_file == True:
                    print("---- Audio written to SIP stream! Hanging up now.")            
                    break
                else:
                    if wavCount >= 500:
                        print("DEBUG | wavCount exceeded 500, end of file might not have occured! Breaking!")
                        try:
                            prm = pj.CallOpParam(True) # Default settings
                            call.hangup(prm)
                        except:
                            pass
                        break
                    # print("-- Not at EOF: " + str(wav_player.is_end_of_file))
                    wavCount = wavCount + 1
                    time.sleep(0.1)

            callHappened = True

            print("------------------------------------")
            print("")
            
            # Hang up the call
            prm = pj.CallOpParam(True) # Default settings
            call.hangup(prm)
            # Sleep for an additional two seconds...
            time.sleep(2)
            break # Break out of forever loop
            
        except Exception as e:
            print(f"DEBUG | !! An error occurred: {e}")
            print("Traceback follows as: " + str(traceback.format_exc()))
            counter = counter + 1
            time.sleep(1)

def attemptMulticastCall():
    print("-- Making multicast call to " + multicastAddress + ":" +  str(multicastPort) + ".")
    ffmpegCommand = "ffmpeg -re -i " + bellWav + " -filter_complex 'aresample=8000,asetnsamples=n=160' -acodec pcm_mulaw -ac 1 -f rtp 'rtp://@" + multicastAddress + ':' + str(multicastPort) + "'"
    # print("-- DEBUG! | Running command: " + ffmpegCommand)

    subprocess.call(ffmpegCommand, shell=True)

    
# Main loop
# Single threaded so while True is acceptable here since SIGINT will be caught just fine
if __name__ == '__main__':
    print("===== Simple bellBellBellBell started! =====")
    if useMulticast == False:
        print("-- Running on the pjsip library with SIP Option Selected =====================================================================")
                    
        # Also most of the below is copy and pasted examples, but it works so I do not care!
        # Create and initialize the library
        ep_cfg = pj.EpConfig()
        ep_cfg.logConfig.level = 0
        # ep_cfg.logConfig.console_level = 0
        # ep_cfg.logConfig.msg_logging = False
        # Only needed if we do our own thread management sometimes I think? PjSip manages it's own crap
        # ep_cfg.uaConfig.threadCnt = 0
        ep = pj.Endpoint()
        ep.libCreate()
        
        # Create SIP transport. Error handling sample is shown
        sipTpConfig = pj.TransportConfig()
        sipTpConfig.port = 5060
        ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, sipTpConfig)
        
        # Start the library
        ep.libInit(ep_cfg)
        # Don't use any sound devices detected by ALSA automatically
        ep.audDevManager().setNullDev()
        ep.libStart()
        
        print("-- pjsip initialized  ===============================================================================")
        print("")
        
        # Create the phone account config
        acfg = pj.AccountConfig()
        acfg.idUri = "sip:" + sipUsername + "@" + sipServer + ":" + str(sipServerPort)
        acfg.regConfig.registrarUri = "sip:" + sipServer + ":" + str(sipServerPort)
        cred = pj.AuthCredInfo("digest", "*", sipUsername, 0, sipPassword)
        acfg.sipConfig.authCreds.append(cred)
        
        print("-- Account config loaded")
        
        # Create account object based on above config
        acc = Account()
        acc.create(acfg)
        print("-- Phone account created, registered & started.")
    
    else:
        print("-- Running on subprocess library with Mulicast Option Selected =====================================================================")
        print("-- FFMPEG being used as Multicast broadcaster")
    print("====== simple-bell.py is now started, operational and waiting for a defined time! ===================")
    print("")
    
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
            #if True: # Use for debugging
                
                # We are in a ringable minute and need to ring the bell!
            
                print("=========================================================================================")
                print("!-- Time to ring bell at " + formatted_time + " on " + formatted_date + "!")                

                if useMulticast == False:

                    attemptSIPCall(acc)
                else:
                    attemptMulticastCall()

                print("-- Call done! Sleeping for 60 seconds to not ring again...")
                print("=========================================================================================")
                print("")
                
                # Bell has rung! Wait 60 seconds to it's sure for an entire minute to pass, people don't put bells 3 minutes apart, 
                time.sleep(60)
                
                # Continue loop!