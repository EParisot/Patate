
#### Download and Install Anaconda Python 3.6

https://www.continuum.io/downloads

#### Change to course folder

```
cd patate\Data_processing
```

#### Create the course environment

```
conda env create
```

wait for the environment to create.

#### Activate the environment (Mac/Linux)
```
source activate patate
```

#### Activate the environment (Windows)
```
activate patate
```

Check that your prompt changed to

```
(patate) $
```

#### Launch Jupyter Notebook

```
jupyter notebook
```

#### Open your browser to

```
http://localhost:8888
```

#### Troubleshooting installation
If for some reason you don't see `Houston we are go!`, the simplest solution is to delete the environment and start from scratch again.

To remove the environment:

- close the browser and go back to your terminal
- stop jupyter notebook (CTRL-C)
- deactivate the environment (Mac/Linux):

```
source deactivate
```

- deactivate the environment (Windows 10):

```
deactivate patate
```

- delete the environment:

```
conda remove -y -n patate--all
```

- restart from environment creation and make sure that each steps completes till the end.

#### Updating Conda

One thing you can also try is to update your conda executable. This may help if you already had Anaconda installed on your system.

```
conda update conda
```

These instructions have been tested on:

- Mac OSX Sierra 10.12.4
- Ubuntu 16.04
- Windows 10