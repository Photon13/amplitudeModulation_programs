import freefield
import slab
from slab import Sound

freefield.initialize('loctest_freefield')  # This sets the default mode to "loctest_freefield"
sound = Sound.read("path_to_your_file.wav")


freefield.set_output(channel="dome")  # Use the dome configuration
freefield.play_sound(sound) # Sound = class from slab