#!/bin/bash

WORK_ROOT="${PWD}/.."
CONTAINER="gif_converter:latest"

echo "[INFO] WORK_ROOT=${WORK_ROOT}"
echo "[INFO] CONTAINER=${CONTAINER}"

docker run --rm -v "${WORK_ROOT}:/work" -it ${CONTAINER} /bin/bash

