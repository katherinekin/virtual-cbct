# virtual-cbct

## Dependencies

This project uses astra-toolbox to simulate cone beam CT. Dependencies for this project include numpy, scipy, opencv-python, matplotlib, imageio, boost, and an NVIDIA GPU and CUDA (at least 5.5). Please install astra-toolbox following the directions on the associated github page. Paver is required to run the build tool and unittests. Creating a virtual environment with the dependencies is recommended.
```
pip install paver
pip install numpy
pip install opencv-python
pip install matplotlib
pip install boost
pip install scipy
pip install imageio
```