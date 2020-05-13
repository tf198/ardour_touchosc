import xml.etree.ElementTree as ET
from zipfile import ZipFile
import base64

ENCODE_ELEMENTS = ('name', 'osc_cs', 'la_t', "text")

MAP_ELEMENTS = {
    'value_from': 'scalef',
    'value_to': 'scalet',
    'osc': 'osc_cs',
    'width': 'w',
    'height': 'h',
    'send_press': 'sp',
    'send_release': 'sr',
    'label': 'la_t',
}

used = set()

class Elements(object):
    LAYOUT_IPAD_PRO = '<layout version="17" mode="3" w="1024" h="1366" orientation="vertical"/>'
    TAB_PAGE = '<tabpage scalef="0.0" scalet="1.0" li_t="" li_c="gray" li_s="14" li_o="false" li_b="false" la_t="" la_c="gray" la_s="14" la_o="false" la_b="false"/>'
    FADERH = '<control x="10" y="10" w="50" h="200" color="red" scalef="0.0" scalet="1.0" type="faderh" response="absolute" inverted="false" centered="false"/>'
    FADERV = '<control x="10" y="10" w="50" h="200" color="red" scalef="0.0" scalet="1.0" type="faderv" response="absolute" inverted="false" centered="false"/>'
    TOGGLE = '<control x="10" y="10" w="45" h="45" color="red" scalef="0.0" scalet="1.0" type="toggle" local_off="false"/>'
    BUTTON = '<control x="10" y="10" w="45" h="45" color="red" scalef="0.0" scalet="1.0" type="push" local_off="true" sp="true" sr="false"/>'
    LABELH = '<control x="10" y="10" w="80" h="25" color="gray" type="labelh" text="Label" size="14" background="true" outline="false"/>'
    LABELV = '<control x="10" y="10" w="25" h="80" color="gray" type="labelv" text="Label" size="14" background="true" outline="false"/>'
    ROTARYH = '<control x="10" y="10" w="100" h="100" color="red" scalef="0.0" scalet="1.0" type="rotaryh" response="absolute" inverted="false" centered="false" norollover="true"/>'
    ROTARYV = '<control x="10" y="10" w="100" h="100" color="red" scalef="0.0" scalet="1.0" type="rotaryv" response="absolute" inverted="false" centered="false" norollover="true"/>'
    LED = '<control x="10" y="10" w="20" h="20" color="red" scalef="0.0" scalet="1.0" type="led"/>'
    ENCODER = '<control x="10" y="10" w="100" h="100" color="red" type="encoder"/>'
    

def osc_element(element, **kwargs):
    if 'name' not in kwargs:
        raise RuntimeError("Missing required name")

    global used
    if kwargs['name'] in used:
        raise RuntimeError(f"Name reuse: {kwargs['name']}")
    used.add(kwargs['name'])

    s = getattr(Elements, element.upper())
    e = ET.fromstring(s)
    for k, v in kwargs.items():
        k = MAP_ELEMENTS.get(k,k)
        if k in ENCODE_ELEMENTS:
            v = osc_encode(v)
        e.attrib[k] = str(v)

    return e

def osc_write(e, filename):
    z = ZipFile(filename, 'w')
    z.writestr('index.xml', ET.tostring(e))
    z.close()
    #ET.dump(e)


def osc_encode(s):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')
