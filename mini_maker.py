from argparse import ArgumentParser
import Image,ImageDraw

sizes = {'small' : ((100,100),80,24),
         'standard' : ((300,300),80,24)}

def size_same(image1,image2):
  """Returns a 2-tuple containing copies of image1 and image2
     scaled to be the same size."""
  width1,height1 = image1.size
  width2,height2 = image2.size
  size = ((width1+width2)/2,(height1+height2)/2)
  return (image1.resize(size,Image.ANTIALIAS),
          image2.resize(size,Image.ANTIALIAS))

def create_mini(front_side,back_side=None,size=sizes['standard']):
  """Returns a new image of a mini with the image scaled on the top,
     a flipped copy on the bottom, and a division bar inbetween"""
  THUMBNAIL_SIZE,DIVISION_BAR_WIDTH,DIVISION_BAR_HEIGHT = size
  if back_side:
    front_side,back_side=size_same(front_side,back_side)
  else:
    back_side = front_side
  scaled_front_side = front_side.copy()
  scaled_front_side.thumbnail(THUMBNAIL_SIZE,Image.ANTIALIAS)
  scaled_back_side = back_side.copy()
  scaled_back_side.thumbnail(THUMBNAIL_SIZE,Image.ANTIALIAS)
  width,height = scaled_front_side.size
  output_width = max(DIVISION_BAR_WIDTH,width)
  output_height = DIVISION_BAR_HEIGHT + (height * 2)
  output_image = Image.new("RGBA", (output_width,output_height))
  #Draw Top Image
  output_image_x = (output_width/2)-(width/2)
  output_image.paste(scaled_front_side,(output_image_x,0))
  #Draw Bottom Image
  output_image.paste(scaled_back_side.transpose(Image.FLIP_TOP_BOTTOM),
                     (output_image_x,height + DIVISION_BAR_HEIGHT))
  #Draw middle division bar
  draw = ImageDraw.Draw(output_image)
  division_bar_x = (output_width/2) - (DIVISION_BAR_WIDTH/2)
  draw.rectangle([division_bar_x, height,
                  division_bar_x+DIVISION_BAR_WIDTH, height+DIVISION_BAR_HEIGHT],
		  fill="black")
  del draw
  return output_image

if __name__=="__main__":
  parser = ArgumentParser(description="Creates paper minis from images")
  parser.add_argument('-s,--size', 
                      dest='size',
		      help='The size of the mini. Either small or standard.',
		      default='standard')
  parser.add_argument('-b,--backside',
                      dest='back_side',
		      help='The backside of the mini. If omitted, both sides are the same.')
  parser.add_argument('filename',
		       help='The name of the image to use for the mini')
  args = parser.parse_args()
  create_mini(Image.open(args.filename),
              Image.open(args.back_side) if args.back_side else None,
	      size=sizes[args.size]).save(args.filename+"-mini.png","PNG")
