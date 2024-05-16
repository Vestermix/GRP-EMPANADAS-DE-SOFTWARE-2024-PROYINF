import pydicom
from PIL import Image
import numpy as np

ds = pydicom.dcmread('funcionalidadesbase\imagenes\IMG-0002-00001.dcm')
image_2d = ds.pixel_array.astype(float)
image_2d_scaled = (np.maximum(image_2d, 0)/image_2d.max())*255.0
image_2d_scaled = np.uint8(image_2d_scaled)
im = Image.fromarray(image_2d_scaled)
print(ds)
print('\n\n\n')
print(ds.PatientName)