import cv2
import os
from PIL import Image

def write_label(label):
  #chnage to dir of images to be labeled
  directory = ("/content/images")
  counter = 0
  for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    #print(f)
    if f.endswith(".jpg"):
      coords = coin_coords(f)
      if not coords:
        print("dasd")
        return
      img = Image.open(f)
      # get width and height
      width = img.width
      height = img.height
      #remove extension, add counter, change to xml file
      label_file = filename[:-4] + str(counter) + ".xml"
      fp = open(label_file, "w")
      fp.write("<annotation>\n")
      folder = "\t<folder>" + directory + "</folder>\n"
      path = "\t<path>" + f + "</path>\n"
      fp.write(folder)
      fname = "\t<filename>" + filename + "</filename>\n"
      fp.write(fname)
      fp.write(path)
      fp.write("\t<source>\n\t\t<database>Unknown</database>\n\t</source>\n")
      fp.write("\t<size>\n")
      wide = "\t\t<width>" + str(width) + "</width>\n"
      h = "\t\t<height>" + str(height) + "</height>\n"
      fp.write(wide)
      fp.write(h)
      fp.write("\t\t<depth>3</depth>\n")
      fp.write("\t</size>\n")
      fp.write("\t<segmented>0</segmented>\n")
      fp.write("\t<object>\n")
      lab = "\t\t<name>" + label + "</name>\n"
      fp.write(lab)
      fp.write("\t\t<pose>Unspecified</pose>\n")
      fp.write("\t\t<truncated>0</truncated>\n")
      fp.write("\t\t<difficult>0</difficult>\n")
      fp.write("\t\t<bndbox>\n")
      xmin = "\t\t\t<xmin>" + str(coords[0][0]) + "</xmin>\n"
      ymin = "\t\t\t<ymin>"+ str(coords[0][1]) + "</ymin>\n"
      xdim = coords[0][0] + coords[0][2]
      xmax = "\t\t\t<xmax>" + str(xdim) + "</xmax>\n"
      ydim = coords[0][1] + coords[0][3]
      ymax = "\t\t\t<ymax>" + str(ydim) + "</ymax>\n"
      fp.write(xmin)
      fp.write(ymin)
      fp.write(xmax)
      fp.write(ymax)
      fp.write("\t\t</bndbox>\n")
      fp.write("\t</object>\n")
      fp.write("</annotation>\n")
      fp.close()

def coin_coords(filename):
  coords = []
  image = cv2.imread(filename)
  input_image_cpy = image.copy()
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  avg = cv2.blur(gray_image,(10,10))
  thresh = 155
  maxValue = 255
 
  th, dst = cv2.threshold(avg, thresh, maxValue, cv2.THRESH_BINARY)

  ROI_number = 0
  cnts = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    if(x > 1000 and w > 1000):
      coords.append([x,y,w,h])
    #print("x:",x,"y:",y,"w:",w,"h:",h)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)

  #cv2_imshow(image)
  #print(coords)
  return coords


def main():
  #change label
  label = "nickel"
  write_label(label)
  print("done")

if __name__ == "__main__":
  main()
