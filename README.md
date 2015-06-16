# pytracer

A simple ray tracer written in Python using NumPy and PIL

Try running `$ python main.py -h` for an explanation of the input parameters. Look at one of the `.scene` input files to see how scenes are specified.

If no output file is specified with the `-o` flag, the output will be displayed with PIL's `Image.show()` method, which by default will attempt to display the image using the command `display`. If that command is not available on your system, that call will fail, and you will get no output.
