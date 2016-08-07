from imagetask.processors import Resize


class ScaleToFit(Resize):
    def process(self, img):
        from pilkit.lib import Image
        import math
        if not self.height:
            ratio = (self.width/float(img.size[0]))
            self.height = math.ceil((float(img.size[1])*float(ratio)))
        elif not self.width:
            ratio = (self.height/float(img.size[1]))
            self.width = math.ceil((float(img.size[0])*float(ratio)))

        if self.upscale or (self.width < img.size[0] and self.height < img.size[1]):
            img = img.convert('RGBA')
            img = img.resize((int(self.width), int(self.height)), Image.ANTIALIAS)
        return img