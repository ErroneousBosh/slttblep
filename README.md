Basic Instructions

open the Arduino editor
open the slttblep.ino sketch
compile and run

Output is on pin 11
Analogue input 1 is frequency
Ground pin 2 to disable antialiasing

Wire a pot with its wiper to A0, one end to GND and the other to +5 for the
frequency control

Wire a simple RC filter to pin 11 for the output

To hear the effect of removing the antialiasing, ground pin 2

Audio example, no antialiasing followed by antialiasing:
<audio controls src="media/blepsweep.ogg">Sorry, it's not possible to play this clip</audio>
