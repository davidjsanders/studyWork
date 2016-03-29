#!/bin/bash
docker run -p 5000:5000 -v $(pwd)/datavolume:/Module/datavolume \
    -it dsanderscan/mscit_v1_00_module
