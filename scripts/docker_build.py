import sys; sys.path.insert(0, '.')

import os
from main import __version__

os.system(
    f"docker build -t devgoldy/aghpb_api:{__version__} --build-arg ARCH=amd64 ."
)

os.system(
    "docker build -t devgoldy/aghpb_api:latest --build-arg ARCH=amd64 ."
)