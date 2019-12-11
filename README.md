# virtual-cbct

## Dependencies and setup

This is a python 3 that project uses astra-toolbox to simulate cone beam CT. Dependencies for this project include numpy, scipy, opencv-python, matplotlib, imageio, boost, and an NVIDIA GPU and CUDA (at least version 5.5). Please download and install the CUDA toolkit following the instructions on their website if not already installed: [https://developer.nvidia.com/cuda-toolkit]

The following commands can be used to install the other dependencies:

```
pip install numpy
pip install opencv-python
pip install matplotlib
pip install boost
pip install scipy
pip install imageio
```

Finally, please install astra-toolbox following the directions on the associated github page [https://github.com/astra-toolbox/astra-toolbox]. astra-toolbox is available for MATLAB or Python. For this project to run, please follow the directions for downloading astra-toolbox for Python. Alternatively, it should also be possible to install dependencies with conda, including astra-toolbox per instructions on the github page. However, it should be noted that astra-toolbox does not work when installed from PyPI.


## Run instructions

Creating a virtual environment with the dependencies is recommended. To start the program, after activating the virtual environment simply run the main.py. Using command line from the project root directory on Windows OS:

```
python src\main.py
```
