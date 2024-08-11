# knapsack-gpu - Running the Knapsack Problem in Different Places
## Results
### CPU with [Google OR-Tools](https://github.com/google/or-tools)
#### In Python -- Google Colab T4 Runtime
Average CPU execution time: 1.374059 seconds
#### In Python -- 2.3Ghz i9 Macbook Pro
```Andrews-Personal-MacBook.local```

Average CPU execution time: 0.783799 seconds -- Run 1
Average CPU execution time: 0.801461 seconds -- Run 2

Combined Average CPU execution time: 0.79263 seconds
#### In Kotlin -- 2.3Ghz i9 Macbook Pro
TODO
#### In C -- 2.3Ghz i9 Macbook Pro
TODO
### GPU with [PyCUDA](https://github.com/inducer/pycuda) -- Google Colab T4 Runtime
Average PyCUDA execution time: 0.007630 seconds
### GPU with [PyOpenCL](https://pypi.org/project/pyopencl/) -- Google Colab T4 Runtime
```[<pyopencl.Platform 'NVIDIA CUDA' at 0x5bf263cd45a0>]```

Average CPU execution time: 0.000615 seconds
### GPU with [PyOpenCL](https://pypi.org/project/pyopencl/) -- 2.3Ghz i9 Macbook Pro
```[<pyopencl.Platform 'Apple' at 0x7fff0000>]```

Average CPU execution time: 0.001286 seconds
### GPU with CUDA in C
TODO
### GPU with OpenCL in C
TODO
## The Problems
TODO: Store the problems, or a way to generate the problems and store them to be used by multiple approaches.
