# Patate
An autonomous RC car to compete the IronCar Challenge...

The robot  uses Convolutional Neural Network to decide where to go (Left, Center or Right) from the camera's pictures and apply the CNN's decision to the engines for each video frame (58x160px - 60fps)

The CNN have been trained with pictures we took from a free wheels replica we pushed by hand on several tracks, until we collected approx 1500 pictures.

After training, the CNN hits at 89% accuracy on our validation tests and is able to ride severals laps.
