from touchosc import osc_element, osc_encode, osc_write

def pushable(el, name, osc, x, y, text, color, el_type="button", **kwargs):
    el.append(osc_element(el_type, name=name, osc=osc,
        w=30, h=60, x=x, y=y, color="red", **kwargs))
    el.append(osc_element('labelv', name=name + "_label",
        outline="true", color="gray", background="false",
        w=30, h=60, x=x, y=y, text=text))

def control(el, name, osc, x, y, text, background, color, el_type="button",
        **kwargs):
    el.append(osc_element(el_type, name=name, 
        osc=osc,
        w=60, h=95, x=x, y=y, color=background, **kwargs))
    el.append(osc_element('labelv', name=name + "_label",
        outline="true", color=color, background="false",
        w=60, h=95, x=x, y=y, text=text, size=16))


TOP = 1024
BOTTOM = 20
RIGHT = 1366 -20
LEFT = 20

# calculate strip positions
elements = ('track', 'mute', 'solo', 'mode', 'fader', 'meter', 
        'leds', 'rec', 'input', 'pan', 'trim', 'name', 'spill')
heights = (30, 30, 30, 30, 300, 60, 20, 30, 20, 60, 40, 140, 30)
pos = [BOTTOM]
x = pos[0]
for k in heights:
    x += k + 10
    pos.append(x)

strip = dict(zip(elements, pos))
sizes = dict(zip(elements, heights))
##print(strip)

BANKS = 12
FEEDBACK = 1 + 2 + 4 + 8 + 16 + 64 + 128 
SYNC = f"/set_surface/{BANKS}/1/{FEEDBACK}"

tab = osc_element('tab_page', name="mixer_tab", label="Ardour Mixer",
        osc=SYNC)

#  BANK CONTROLS
pos = strip['fader'] + 300 - 30
#tab.append(osc_element('labelv', name="label_strips",
#    x=pos+40, y=LEFT, w=20, h=60,
#    background="false", text="Strips"))
pushable(tab, "strip_track", "/set_surface/strip_types", pos, LEFT,
        "Track", "red", value_to=3)
pushable(tab, "strip_bus", "/set_surface/strip_types", pos-40, LEFT,
        "Bus", "red", value_to=12)
pushable(tab, "strip_vca", "/set_surface/strip_types", pos-80, LEFT,
        "VCA", "red", value_to=16)
pushable(tab, "strip_selected", "/set_surface/strip_types", pos-120, LEFT,
        "Select", "red", value_from=256, value_to=256)


pushable(tab, "bank_up", "/bank_up", strip['fader']+80, LEFT,
        "+", "blue")
tab.append(osc_element('labelv', name="label_bank",
    x=strip['fader']+60, y=LEFT, w=20, h=60,
    background="false", text="Bank"))
pushable(tab, "bank_down", "/bank_down", strip['fader']+30, LEFT,
        "-", "blue")


# LABELS

label = {"h": 60, "w": 30, "y": 20, "outline": "true"}

tab.append(osc_element('labelv', name="mute_label", x=strip['mute'],
    text="Mute", color="yellow", **label))
tab.append(osc_element('labelv', name="solo_label", x=strip['solo'],
    text="Solo", color="green", **label))
tab.append(osc_element('labelv', name="mode_label", x=strip['mode'],
    text="Mode", color="orange", **label))
tab.append(osc_element('labelv', name="safe_label", x=strip['leds']-10,
    text="Safe", color="green", **label))
tab.append(osc_element('labelv', name="rec_label", x=strip['rec'],
    text="Rec", color="red", **label))
tab.append(osc_element('labelv', name="input_label", x=strip['input'],
    text="Input", color="orange", **label))
tab.append(osc_element('labelv', name="pan_label", x=strip['pan']+15,
    text="Pan", color="yellow", **label))
tab.append(osc_element('labelv', name="trim_label", x=strip['trim']+5,
    text="Trim", color="purple", **label))
tab.append(osc_element('labelv', name="spill_label", x=strip['spill'],
    text="Spill", color="red", **label))

for i in range(1, BANKS+1):

    y = 100 + 80 * (i-1)
    
    tab.append(osc_element('labelv', name=f"mixer_track_{i}", x=strip['track'],
        y=y+15, w=30, h=30,
        text=str(i), color="red", background="false", outline="true"))

    tab.append(osc_element('toggle', name=f"mute_{i}", x=strip['mute'],
        y=y, w=30, h=60,
        osc=f"/strip/mute/{i}", color="yellow"))

    tab.append(osc_element('toggle', name=f"solo_{i}", x=strip['solo'],
        y=y, w=30, h=60,
        osc=f"/strip/solo/{i}", color="green"))

    tab.append(osc_element('labelv', name=f"automation_{i}", x=strip['mode'],
        y=y, w=30, h=60, color="orange", text="-", outline="true",
        osc=f"/strip/fader/automation_name/{i}"))

    tab.append(osc_element('faderh', name=f"fader_{i}", x=strip['fader'],
        y=y, w=300, h=60,
        osc=f"/strip/fader/{i}"))
    
    tab.append(osc_element('rotaryv', name=f"meter_{i}", x=strip['meter'],
        y=y, w=60, h=60,
        osc=f"/strip/meter/{i}", color="green"))

    tab.append(osc_element('led', name=f"safe_{i}", x=strip['leds'], y=y+5,
        osc=f"/strip/record_safe/{i}", color="green"))
    tab.append(osc_element('led', name=f"touch_{i}", x=strip['leds'], y=y+30, 
        osc=f"/strip/fader/touch/{i}", color="orange"))
    
    tab.append(osc_element('toggle', name=f"rec_{i}", x=strip['rec'],
        y=y, w=30, h=60,
        osc=f"/strip/recenable/{i}"))
    
    tab.append(osc_element('led', name=f"mon_input_{i}", x=strip['input'], y=y+5,
        osc=f"/strip/monitor_input/{i}", color="yellow"))
    tab.append(osc_element('led', name=f"input_{i}", x=strip['input'], y=y+30, 
        osc=f"/strip/monitor_disk/{i}", color="orange"))
    
    tab.append(osc_element('rotaryh', name=f"pan_{i}", x=strip['pan'],
        y=y, w=60, h=60,
        color="yellow", inverted="true",
        osc=f"/strip/pan_stereo_position/{i}", centered="true"))
    
    tab.append(osc_element('rotaryh', name=f"trim_{i}", x=strip['trim'],
        y=y+10, w=40, h=40,
        color="purple", value_from="-20.0", value_to="20.0",
        osc=f"/strip/trimdB/{i}", centered="true"))

    tab.append(osc_element('labelh', name=f"name_{i}", x=strip['name'],
        y=y+10, w=sizes['name'], h=40, size=18,
        osc=f"/strip/name/{i}", text=f"", color="orange"))

    tab.append(osc_element('button', name=f"spill_{i}", x=strip['spill'],
        y=y+15, w=30, h=30,
        osc=f"/strip/spill/{i}", color="red", value_from=i, value_to=i))
    

# main
y = RIGHT - 60

tab.append(osc_element('labelv', name=f"mixer_master", x=strip['track'],
    y=y, w=30, h=60,
    text="Master", color="red", background="false", outline="true"))

tab.append(osc_element('toggle', name=f"master_mute", x=strip['mute'],
    y=y, w=30, h=60,
    osc=f"/master/mute", color="yellow"))

tab.append(osc_element('button', name=f"cancel_solos", x=strip['solo'],
    y=y, w=30, h=60,
    osc="/cancel_all_solos", color="green"))

tab.append(osc_element('labelv', name=f"master_automation", x=strip['mode'],
    y=y, w=30, h=60, color="orange", text="-", outline="true",
    osc=f"/master/fader/automation_name"))

tab.append(osc_element('faderh', name=f"master_fader", x=strip['fader'],
    y=y, w=300, h=60,
    osc=f"/master/fader"))

tab.append(osc_element('rotaryv', name="master_meter", x=strip['meter'],
    y=y, w=60, h=60,
    osc="/master/meter", color="green"))

tab.append(osc_element('led', name=f"solos_active", x=strip['leds'],
    y=y+5, osc="/cancel_all_solos", color="green"))
tab.append(osc_element('led', name=f"Master 2", x=strip['leds'],
    y=y+30, color="red"))


tab.append(osc_element('rotaryh', name=f"master_pan", x=strip['rec'],
    y=y, w=60, h=60,color="yellow",
    osc=f"/master/pan_stereo_position", centered="true"))

tab.append(osc_element('rotaryh', name=f"Master Trim", x=strip['rec'] + 70,
    y=y+10, w=40, h=40,
    color="purple", value_from="-20.0", value_to="20.0",
    osc=f"/master/trimdB", centered="true"))

#tab.append(osc_element('labelh', name=f"Channel {i}", x=strip['name'],
#    y=y+10, w=120, h=40, size=18,
#    text=f"", osc=f"/session_name"))


top_row = TOP - 90
bottom_row = top_row - 50 

# Controls

CONTROL_LEFT = 1063
CONTROL_RIGHT = 1063+105
CONTROL_WIDTH = 200
CONTROL_TOP = strip['name'] - 70

tab.append(osc_element('labelv', name="session", x=strip['spill'],
    y=CONTROL_LEFT, w=30, h=RIGHT-CONTROL_LEFT, color="red",
    outline="true",
    osc="/session_name", text="No Session"))

tab.append(osc_element('labelv', name="position", x=strip['name'], y=CONTROL_LEFT,
    h=RIGHT-CONTROL_LEFT, w=80, color="red", size=40,
    osc="/position/smpte", text="00:00:00:0"))

# Jog wheel
tab.append(osc_element('encoder', name="jog", x=BOTTOM+40, y=CONTROL_LEFT,
    w=CONTROL_WIDTH, height=CONTROL_WIDTH, value_from=-1, value_to=1,
    osc="/jog"))
tab.append(osc_element('labelv', name="jog_mode", x=BOTTOM+40, y=CONTROL_LEFT,
    w=CONTROL_WIDTH, h=CONTROL_WIDTH, osc="/jog/mode/name", text="Jog",
    background="false", color="red"))
tab.append(osc_element('faderv', name="jog_mode_selector",
    x=BOTTOM, y=CONTROL_LEFT, w=30, h=CONTROL_WIDTH,
    osc="/jog/mode", value_to=6))
#tab.append(osc_element('button', name="enc_jog", x=BOTTOM, 
#    y=CONTROL_LEFT,
#    w=30, h=30, color="red", osc="/jog/mode", value_to=0))
#tab.append(osc_element('button', name="enc_strip", x=BOTTOM, 
#    y=CONTROL_LEFT + 40,
#    w=30, h=30, color="green", osc="/jog/mode", value_to=6))

# Transport
control(tab, "transport_stop", "/transport_stop", CONTROL_TOP, CONTROL_LEFT,
        "Stop", "brown", "gray")
control(tab, "transport_play", "/transport_play", CONTROL_TOP, CONTROL_RIGHT,
        "Play", "green", "gray")
control(tab, "record", "/rec_enable_toggle", CONTROL_TOP-70, CONTROL_LEFT,
        "Record", "red", "gray")
control(tab, "forget", "/stop_forget", CONTROL_TOP-70, CONTROL_RIGHT,
        "Forget", "orange", "gray")

control(tab, "sync", f"/set_surface/{BANKS}/1/{FEEDBACK}",
        CONTROL_TOP-180, CONTROL_LEFT,
        "Sync", "green", "gray")
control(tab, "use_group", "/use_group", strip['meter']-70, CONTROL_LEFT,
        "Group", "orange", "gray", el_type='toggle')

ALL_STRIPS = 1 + 2 + 4 + 8 + 16 + 32 + 64 + 128 + 512
TRACK_FEEDBACK = 1 + 2 + 4 + 8192
tracks = osc_element('tab_page', name="track_tab", label="Tracks",
        osc=f"/set_surface/48/{ALL_STRIPS}/{TRACK_FEEDBACK}")

led = {"w": 20, "h": 20}

for i in range(6):
    x = TOP - 180 - i*160

    for j in range(8):
        y = 60 + j*125
        t = i*12 + j + 1

        tracks.append(osc_element('button', name=f"track_select_{t}",
            x=x, y=y, w=60, h=60,
            osc=f"/strip/expand/{t}", color="red"))
        tracks.append(osc_element('labelv', name=f"track_name_{t}",
            x=x+90, y=y-20, w=30, h=100,
            osc=f"/strip/name/{t}", text="-"))
        tracks.append(osc_element('led', name=f"track_hide_{t}",
            x=x+65, y=y+5,
            osc=f"/strip/hide/{t}", color="orange", **led))
        tracks.append(osc_element('led', name=f"track_meter_{t}",
            x=x+65, y=y+35,
            osc=f"/strip/meter/{t}", color="green", **led))
        tracks.append(osc_element('led', name=f"track_input_{t}",
            x=x+35, y=y+65,
            osc=f"/strip/monitor_input/{t}", color="yellow", **led))
        tracks.append(osc_element('led', name=f"track_disk_{t}",
            x=x+5, y=y+65,
            osc=f"/strip/monitor_disk/{t}", color="orange", **led))
        tracks.append(osc_element('led', name=f"track_recenable_{t}",
            x=x+35, y=y-25,
            osc=f"/strip/recenable/{t}", color="green", **led))
        tracks.append(osc_element('led', name=f"track_recsafe_{t}",
            x=x+5, y=y-25,
            osc=f"/strip/record_safe/{t}", color="yellow", **led))
        tracks.append(osc_element('led', name=f"track_solo_{t}",
            x=x-25, y=y+5,
            osc=f"/strip/solo/{t}", color="green", **led))
        tracks.append(osc_element('led', name=f"track_mute_{t}",
            x=x-25, y=y+35,
            osc=f"/strip/mute/{t}", color="yellow", **led))

def track_toggle(osc, x, y, text, background, color="yellow", **kwargs):
    name = f"track_toggle_{x}_{y}"
    tracks.append(osc_element('toggle', name=name, 
        x=x, y=y, w=50, h=120,
        osc=osc, color=background, **kwargs))
    tracks.append(osc_element('labelv', name=name + "_label",
        x=x, y=y, w=50, h=120, background="false",
        text=text, color=color))


def track_button(osc, x, y, text, background, color="yellow", **kwargs):
    name = f"track_button_{x}_{y}"
    tracks.append(osc_element('button', name=name, 
        x=x, y=y, w=50, h=120,
        osc=osc, color=background, **kwargs))
    tracks.append(osc_element('labelv', name=name + "_label",
        x=x, y=y, w=50, h=120, background="false", outline="true",
        text=text, color=color))

CONTROL_RIGHT = RIGHT - 200
CONTROL_LEFT = 1066
CONTROL_RIGHT = CONTROL_LEFT + 130
CONTROL_WIDTH = 250

TOP = TOP - 90

tracks.append(osc_element('labelv', name="select_name", 
    x=TOP, y=CONTROL_LEFT, color="red", outline="true", 
    w=30, h=250, osc="/select/name", text="No track selected"))
tracks.append(osc_element('labelv', name="select_group", 
    x=TOP-40, y=CONTROL_LEFT,
    w=30, h=250, osc="/select/group", text="-"))

TOP = TOP - 120
track_button("/transport_stop", TOP, CONTROL_LEFT, "Stop", "brown")
track_button("/transport_play", TOP, CONTROL_RIGHT, "Play", "green")
track_button("/cancel_all_solos", TOP-60, CONTROL_LEFT, "Solos", "green")

tracks.append(osc_element('faderh', name="select_fader", color="red",
    x=510, y=CONTROL_LEFT, h=60, w=200,
    osc="/select/fader"))
tracks.append(osc_element('faderh', name="select_meter", color="green",
    x=510, y=CONTROL_LEFT+70, h=20, w=200,
    osc="/select/meter"))

TOP = 500
tracks.append(osc_element('faderv', name="track_pan",
    x=TOP-40, y=CONTROL_LEFT, w=30, h=CONTROL_WIDTH, color="yellow",
    osc="/select/pan_stereo_position", centered="true", inverted="true"))
tracks.append(osc_element('faderv', name="track_pan_width",
    x=TOP-80, y=CONTROL_LEFT, w=30, h=120, color="brown",
    osc="/select/pan_stereo_width", value_from="0.5"))
tracks.append(osc_element('labelv', name="track_pan_width_label",
    x=TOP-80, y=CONTROL_LEFT, w=30, h=120, color="yellow",
    background="false", text="Stereo Width", inverted="true"))
tracks.append(osc_element('faderv', name="track_automation",
    x=TOP-120, y=CONTROL_LEFT, w=30, h=120, color="orange",
    osc="/select/fader/automation", value_to=3))
tracks.append(osc_element('labelv', name="track_automation_mode",
    x=TOP-120, y=CONTROL_LEFT, w=30, h=120, color="yellow", background="false",
    osc="/select/fader/automation_name", text="-"))
    

TOP = 280
track_toggle("/select/polarity", TOP, CONTROL_LEFT, "Polarity", "blue")
track_toggle("/select/hide", TOP-60, CONTROL_LEFT, "Hide", "orange")
track_toggle("/select/recenable", TOP-120, CONTROL_LEFT, "Record", "red")
track_toggle("/select/record_safe", TOP-180, CONTROL_LEFT, "Safe", "yellow")
track_button("/select/signal", TOP-60, CONTROL_RIGHT, "Signal", "green")
track_toggle("/select/monitor_input", TOP-120, CONTROL_RIGHT, "Input", "yellow")
track_toggle("/select/monitor_disk", TOP-180, CONTROL_RIGHT, "Disk", "orange")
track_toggle("/select/solo", TOP-240, CONTROL_LEFT, "Solo", "green")
track_toggle("/select/mute", TOP-240, CONTROL_RIGHT, "Mute", "yellow")

layout = osc_element('layout_ipad_pro', name="Ardour Mixer")
layout.append(tab)
layout.append(tracks)

osc_write(layout, 'Ardour iPad Pro.touchosc')
