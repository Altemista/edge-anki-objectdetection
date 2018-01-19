import os

def init():
    global enable_debug_images
    enable_debug_images = os.environ.get('ENABLE_DEBUG_IMAGES')
    if enable_debug_images is None:
        enable_debug_images = False
    else:
        enable_debug_images = True