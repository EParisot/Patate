# Patate
An autonomous RC car to compete the IronCar Challenge...

At the beginning, the project was an RC car, recycled into, an... RC car, with more power, a camera, speech with Google Assistant, music player, Wifi extender...
https://github.com/Klhnikov/PiRobot

The new robot uses Convolutional Neural Network to decide where to go (Left, Center or Right) from the camera's pictures and apply the CNN's decision to the engines for each video frame (128x160px - 60fps)

The CNN have been trained with pictures we took from a free wheels replica we pushed by hand on several tracks, until we collected approx 1500 pictures.

After training, the CNN hits at 89% accuracy on our validation tests and is able to ride severals laps.

UPDATE : Patate42 won the first french edition of IronCar race !!!
We had to do a new dataset from scratch an modify the code a bit but it's still the same principle !
