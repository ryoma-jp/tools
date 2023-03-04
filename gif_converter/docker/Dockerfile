# --- build command ---
#   * docker build --network=host -f Dockerfile -t gif_converter .

FROM ubuntu:22.10

ENV TZ=Asia/Tokyo

RUN apt update && \
    apt install -y libgl1-mesa-dev vim python3.11 python3.11-dev python3-pip && \
    DEBIAN_FRONTEND=noninteractive apt install -y libopencv-dev

RUN pip install opencv-python==4.7.0.72 \
                Pillow==9.4.0

