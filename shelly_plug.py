#
# run this with       uvicorn shelly_plug:shelly_plug_s --reload
#

from fastapi import FastAPI
import random

shelly_plug_s = FastAPI()


@shelly_plug_s.get("/settings")
def settings():
    """
    Shelly Plug extends the common /settings endpoint with power consumption status and contains the settings for this device.
    Shelly Plug adds max_power to the list of parameters which can be set via the common /settings endpoint:

    Attribute 	        | Type 	           | Description
    ---|---|---
    max_power 	        | number 	       | Overpower threshold in Watts
    led_power_disable 	| bool 	           | PlugS only Whether LED indication for output status is enabled
    actions 	        | hash 	           | List with all supported url actions. For detailed actions descriptions, see /settings/actions
    relays 	            | array of hashes  | See /settings/relay/0 for explanation of values


    Parameter 	        | Type 	           | Description
    ---|---|---
    max_power 	        | number 	       | Overpower threshold in Watts
    led_power_disable 	| bool 	           | PlugS only Disable LED indication for output status
    actions 	        | hash 	           | For setting actions, see /settings/actions
    """
    # GET / settings(Shelly PlugS)
    r = {
        "max_power": 3500,
        "led_power_disable": False,
        "actions": {
            "active": False,
            "names": [
                "btn_on_url",
                "out_on_url",
                "out_off_url"
            ]
        },
        "relays": [
            {
                "name": None,
                "appliance_type": "General",
                "ison": False,
                "has_timer": False,
                "overpower": False,
                "default_state": "off",
                "auto_on": 0,
                "auto_off": 0,
                "schedule": False,
                "schedule_rules": [],
                "max_power": 0
            }
        ]
    }

    return r


@shelly_plug_s.put("/settings/relay/{id:int}")
def settings_relay(id:int):
    """<pre>
    To control Shelly Plug/PlugS, use these resources:

    /settings/relay/0 to configure the behavior of the plug
    /relay/0 to control and monitor the plug
    The returned document here is identical to the data returned in /settings for the single output channel in the relays array.
    The channel index exists to preserve API compatibility with multi-channel Shelly devices.
    Attributes in the response match the set of accepted parameters.

    Attribute 	       | Type 	           | Description
    ---|---|---
    name 	           | string 	       | Relay name
    appliance_type 	   | string 	       | Custom configurable appliance type
    ison 	           | bool 	           | State of the channel
    has_timer 	       | bool 	           | Whether there is an active timer on the channel
    overpower 	       | bool 	           | Whether an overpower condition has occurred
    default_state 	   | string 	       | Default power-on state, one of off, on, last
    auto_on 	       | number 	       | Automatic flip back timer, seconds. Will engage after turning the plug OFF
    auto_off 	       | number 	       | Automatic flip back timer, seconds. Will engage after turning the plug ON
    schedule 	       | bool 	           | Whether scheduling is enabled
    schedule_rules 	   | array of strings  | Rules for schedule activation
    max_power 	       | number 	       | Overpower threshold in Watts

    Parameter 	    Type 	               | Description
    ---|---|---
    name 	        string 	               | Set relay name
    appliance_type 	string 	               | Set custom configurable appliance type
    reset 	        any 	               | Submitting a non-empty value will reset settings for the plug output to factory defaults
    default_state 	string 	               | Accepted values: off, on, last
    auto_on 	    number 	               | Automatic flip back timer, seconds. Will engage after turning the plug OFF
    auto_off 	    number 	               | Automatic flip back timer, seconds. Will engage after turning the plug ON
    schedule 	    bool 	               | Enable schedule timer
    schedule_rules 	array of strings 	   | Rules for schedule activation, e.g. 0000-0123456-on
    max_power 	    number 	               | Overpower threshold in Watts
    """
    # GET /settings/relay/0

    r =  {
        "name": f"{id}",
        "appliance_type": "General",
        "ison": False,
        "has_timer": False,
        "overpower": False,
        "default_state": "off",
        "auto_on": 0,
        "auto_off": 0,
        "schedule": False,
        "schedule_rules": [],
        "max_power": 0
    }

    return r


@shelly_plug_s.get("/status")
def status():
    """
    Shelly Plug adds information about the current state of the plug (ON or OFF) and instantaneous power reading in Watts.

    Attribute 	      | Type 	        | Description
    ---|---|---
    relays 	          | array of hashes | Contains the current state of the relay output channels. See /relay/0 for description of attributes
    meters 	          | array of hashes | Current status of the power meter
    temperature 	  | number 	        | PlugS only internal device temperature in °C
    overtemperature   | bool            | PlugS only true when device has overheated
    tmp.tC 	          | number 	        | PlugS only Internal device temperature in °C
    tmp.tF 	          | number 	        | PlugS only Internal device temperature in °F
    tmp.is_valid 	  | bool 	        | PlugS only Whether the internal temperature sensor functions correctly
    """
    # GET /status (Shelly PlugS)
    power_1min = random.uniform(30, 100)
    power_2min = power_1min * random.uniform(1.5, 2.5)
    power_3min = power_2min * random.uniform(1.1, 1.3)
    r = {
        "relays": [
            {
                "ison": True,
                "has_timer": False,
                "timer_started": 0,
                "timer_duration": 0,
                "timer_remaining": 0,
                "overpower": False,
                "source": "http"
            }
        ],
        "meters": [
            {
                "power": random.uniform(30, 100),
                "overpower": 23.78,
                "is_valid": True,
                "timestamp": 0,
                "counters": [power_1min, power_2min, power_3min],
                "total": 4
            }
        ],
        "temperature": random.uniform(18.0, 50.0),
        "overtemperature": False,
        "tmp": {
            "tC": 41.94,
            "tF": 107.5,
            "is_valid": True
        }
    }

    return r


@shelly_plug_s.get("/meter/{id}")
def meter(id:int):
    """
    Attribute   | Type 	            | Description
    ---|---|---
    power 	    | number 	        | Current real AC power being drawn, in Watts
    is_valid    | bool 	            | Whether power metering self-checks OK
    overpower   | number 	        | Value in Watts, on which an overpower condition is detected
    timestamp   | number 	        | Timestamp of the last energy counter value, with the applied timezone
    counters    | array of numbers 	| Energy counter value for the last 3 round minutes in Watt-minute
    total 	    | number 	        | Total energy consumed by the attached electrical appliance in Watt-minute
    """
    # GET / meter / 0

    print(f"selected meter id: {id}")
    if(id != 0):
        print(f"meter with id {id} is not available.")
        r = False
    else:
        power_1min = random.uniform(30, 100)
        power_2min = power_1min * random.uniform(1.5, 2.5)
        power_3min = power_2min * random.uniform(1.1, 1.3)
        r = {
            "power": 0,
            "overpower": 23.78,
            "is_valid": True,
            "timestamp": 0,
            "counters": [power_1min, power_2min, power_3min],
            "total": 4
        }

    return r


@shelly_plug_s.get("/relay/{id:int}")
def relay(id:int):
    """
    To control Shelly Plug/PlugS, use these resources:

    /settings/relay/0 to configure the behavior of the plug
    /relay/0 to control and monitor the plug
    Shows current status of the output channel and accepts commands for controlling the channel.

    Attribute 	       | Type 	    | Description
    ---|---|---
    ison 	           | bool 	    | Whether the channel is turned ON or OFF
    has_timer 	       | bool 	    | Whether a timer is currently armed for this channel
    timer_started 	   | number 	| Unix timestamp of timer start; 0 if timer inactive or time not synced
    timer_duration 	   | number 	| Timer duration, s
    timer_remaining |	number 	    | experimental If there is an active timer, shows seconds until timer elapses; 0 otherwise
    overpower 	       | bool 	    | Whether an overpower condition turned the channel OFF
    source 	           | string 	| Source of the last relay command

    Parameter 	| Type 	    | Description
    ---|---|---
    turn 	    | string 	| Accepted values are on, off, toggle. This will turn ON/OFF the respective output channel when request is sent
    timer 	    | number 	| A one-shot flip-back timer in seconds
    :param id:
    :return:
    """
    # GET /relay/0
    print(f"relay id: {id}")
    r = {
        "ison": False,
        "has_timer": False,
        "timer_started": 0,
        "timer_duration": 0,
        "timer_remaining": 0,
        "overpower": False,
        "source": "http"
    }
    return r
