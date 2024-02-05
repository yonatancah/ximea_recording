from ximea import xiapi

def list_connected_cameras():
    system = xiapi.Camera()

    try:
        num_cameras = system.get_number_devices()
        print(f"Number of connected cameras: {num_cameras}")

    except xiapi.Xi_error as e:
        print(f"Error: {e}")
    
if __name__ == "__main__":
    list_connected_cameras()
