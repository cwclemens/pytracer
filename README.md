# pytracer

A simple ray tracer written in Python using NumPy and PIL

To run, just do
`$ python main.py`

Until command-line parsing is added, you'll have to specify which scene file to parse in `main.py`. The `write_image` function in `main.py` calls PIL's `Image.show()`, which may not work on all platforms, so you may have to add an output file path to get it to work.
