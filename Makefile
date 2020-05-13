
IPAD_PRO=Ardour\ iPad\ Pro.touchosc

all: ${IPAD_PRO}

${IPAD_PRO}: ardour_ipad_pro.py
	python $<
