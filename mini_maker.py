from argparse import ArgumentParser
import Image,ImageDraw

sizes = {'small' : ((100,100),80,24),
         'standard' : ((300,300),80,24)}

def create_mini(image,size=sizes['standard']):
  """Returns a new image of a mini with the image scaled on the top,
     a flipped copy on the bottom, and a division bar inbetween"""
  THUMBNAIL_SIZE,DIVISION_BAR_WIDTH,DIVISION_BAR_HEIGHT = size
  scaled_image = image.copy()
  scaled_image.thumbnail(THUMBNAIL_SIZE,Image.ANTIALIAS)
  width,height = scaled_image.size
  output_image = Image.new("RGBA", (max(DIVISION_BAR_WIDTH,width),
                                    DIVISION_BAR_HEIGHT + (height * 2)))
  #Draw Top Image
  output_image.paste(scaled_image,(0,0))
  #Draw Bottom Image
  output_image.paste(scaled_image.transpose(Image.FLIP_TOP_BOTTOM),
                     (0,height + DIVISION_BAR_HEIGHT))
  #Draw middle division bar
  draw = ImageDraw.Draw(output_image)
  division_bar_x = (width/2) - (DIVISION_BAR_WIDTH/2)
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
  parser.add_argument('filename',
		       help='The name of the image to use for the mini')
  args = parser.parse_args()
  create_mini(Image.open(args.filename),sizes[args.size]).save(args.filename+"-mini.png","PNG")
