from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill

class BannerImage(ImageSpec):   
    processors = [ResizeToFill(580, 400)]
    format = 'JPEG'

register.generator('shared:banner', BannerImage)
