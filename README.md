# Patate
An autonomous RC car to compete the IronCar Challenge...

The robot  uses Convolutional Neural Network to decide where to go (Left, Center or Right) from the camera's pictures and apply the CNN's decision to the engines for each video frame (58x160px - 60fps)

The CNN have been trained with pictures we took from a free wheels replica we pushed by hand on several tracks, until we collected approx 1500 pictures.

After training, the CNN hits at 89% accuracy on our validation tests and is able to ride severals laps.
We still got issues with high speeds and/or straight bends taken from the outside, and sometime the machine can't decide where to go because of multiples lines in view... We also need to add a File (FIFO) system to end up undecision's loops and force moving if stuck...
