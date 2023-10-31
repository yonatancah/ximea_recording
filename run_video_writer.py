from video_writers.opencv import OpenCVVideoWriter
from camera.dummy_camera import DummyCamera

cam = DummyCamera()
frame = cam.get_frame()
image = frame.image
height, width, _ = image.shape

writer = OpenCVVideoWriter.open("test.mkv", frame_height=height, frame_rate=30, frame_width=width)
for _ in range(500):
    frame = cam.get_frame()
    writer.write(frame=frame.image)
writer.close()