import sys
sys.path.insert(0, '.')

import os
import app

os.system(
    f"docker buildx build -t devgoldy/aghpb_api:{app.__version__} ."
)

os.system(
    "docker buildx build -t devgoldy/aghpb_api:latest ."
)