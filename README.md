# PyGA
Genetic algorithm implementations in Python.

### Usage

Run `genlearn.py` with Python 3 or pypy for better performance. 

```
$ pypy3 genlearn.py -t "<target string>" 
                   [-s <population size>] 
                   [-m <mutation rate>] 
                   [-p <power>]
```

Additionally, `genpixel.py` can be used for images represented by ASCII characters (visually, as in ASCII art). Filename of the input image is set on line `188`, where the image is converted into an ASCII string.
