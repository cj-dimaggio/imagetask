# imagetask
A library for generating complex image derivatives efficiantly by serializing commands through Base64 encoded signed urls. Imagetask aims to be as extensible as possible, allowing for pluggable image loading strategies, storage providers and caching systems. 

## Example

    from imagetask import ImageTaskApp
    from imagetask.processors import *
    from PIL import Image

    # Create our imagetask context
    it = ImageTaskApp(dict(SECRET_KEY="123"))

    # Reference an image file (either a local or remote file)
    img = it.new("/tmp/image.png")

    # Chain together image processes
    img.processors = [
        Crop(width=100, height=50, x=0, y=0),
        Resize(50, 50),
        Transpose()
    ]

    # Print the image reference represented by a URL
    print img.url

    # Regenerate the image reference from the url
    img2 = it.from_serial_data(img.url)

    # Actually generate the new image
    real_img = img2.generate()

    # Open up the new image with PIL and check it's size
    print Image.open(real_img).size
