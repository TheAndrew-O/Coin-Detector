import cv2
import os
from PIL import Image

def write_label(label):
  #change to dir of images to be labeled
  directory = ("/home/andrew/coin/autolabel/images/")
  #counter = 0
  for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    #print(f)
    if f.endswith(".jpg"):
      coords = coin_coords(f)
      if not coords:
        print("No coin found")
        continue
      img = Image.open(f)
      # get width and height
      width = img.width
      height = img.height
      #remove extension, add counter, change to xml file
      l_file = filename[:-4] + ".xml"
      label_file = directory + l_file 
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
      xmin = "\t\t\t<xmin>" + str(coords[0]) + "</xmin>\n"
      ymin = "\t\t\t<ymin>"+ str(coords[1]) + "</ymin>\n"
      xdim = coords[0] + coords[2]
      xmax = "\t\t\t<xmax>" + str(xdim) + "</xmax>\n"
      ydim = coords[1] + coords[3]
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
  max_area = 0
  image = cv2.imread(filename)
  input_image_cpy = image.copy()
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  avg = cv2.blur(gray_image,(10,10))
  thresh = 145
  maxValue = 255
 
  th, dst = cv2.threshold(avg, thresh, maxValue, cv2.THRESH_BINARY)

  ROI_number = 0
  cnts = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    area = w * h
    if(area > max_area):
        max_area = area
        coords = [x,y,w,h]
    #print("x:",x,"y:",y,"w:",w,"h:",h)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)

  #cv2.imshow(image)
  #cv2.waitKey(0)
  #cv2.destroyAllWindows()
  #print(coords)
  return coords


def main():
  #change label
  label = input("Enter label\n")
  write_label(label)
  print("done")

if __name__ == "__main__":
  main()
