from PIL import Image
from io import BytesIO
import base64 as b64


def load_frames(path: str) -> list[Image.Image]:
    im = Image.open(path)
    frames = []

    # To iterate through the entire gif
    try:
        while 1:
            im.seek(im.tell()+1)
            frames.append(im.copy())
    except EOFError:
        return frames
    

def to_b64(image: Image.Image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return b64.b64encode(buffered.getvalue())

if __name__ == "__main__":
    from os import path

    print("hello")

    im_path = path.join(path.dirname(__file__), "pacman.gif")
    for i, frame in enumerate(load_frames(im_path)):
        print(f"showing {i}")
        frame.show(f"Frame {i}")
    