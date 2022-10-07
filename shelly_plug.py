from fastapi import FastAPI
import random

shelly_plug_s = FastAPI()


@shelly_plug_s.get("/settings")
def settings():
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
    for the given meter id, returns the current power and the last 3 minutes' Watt minute values\n
    :param id: id of the meter whose data is intended\n
    :return: JSON\n
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
