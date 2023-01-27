A Program for getting the distanc a particle traveled through a bubble chamber

Setup:

- create a python virtual enviroment in your directory through python3 -m venv <venv_dir_name>
- Set your python interpreter to be your python virtual environment
- Install the latest ersion of pip: pip3 install --upgrade pip
- Install opencv: pip3 install opencv-python
- Check if opencv was installed correctly:
  -- main.py:
  import cv2
  print(cv2.**version**)
- run main.py: python3 main.py

Input Images:
There are a few rules I followed to create my image inputs:

1. Each image size was 580x559px (images are included in the repo if you'd like to use them. The source image is included as well)
2. The starting pixel is colored with hex: #EE00FF.
3. The particle path will be drawn in three ways: a lower path, upper path, and center path. This is beause the particle in the image
   did not travel on a per-pixel basis, but rather on a spread of pixel values.
4. For each drawn path, whenever a gap in the source path, the drawn path was continued in a straight line. If there was no pixel that satisfied the drawn path's rules nearby a the end of the source path's gap, I would draw vertically until I reached one. This sounds more extreme than it actually was. I only had to travel vertically by 1 or 2 pixels in each drawn path.
5. For the lower path, I followed the lowest pixel in the source path. It was colored with hex: #FFFF00
6. For the upper path, I followed the highest pizel in the source path. It was colored with hex: #11FF00
7. For the center path, I checked the distance between the lowest and highest pixel. If the distance was even, I took the lowest path closest to the center. If it was an odd number of pixels, I took the center pixel. It was colored with hex: #FF0000
8. I followed these rules very closely, but there were still some spots where human judgement was needed. This will introduce some systematic error into the analysis but I believe it to be a necessary addition due to some parts of the source path being intersected by other particles and making the path drawing rules difficult to follow.
