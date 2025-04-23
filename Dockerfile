FROM futureys/selenium-python:20250419190000
# - pythonでseleniumを使ってスクリーンショットを撮ると、日本語が文字化けしてしまう | プログラミング学習サイト【侍テラコヤ】
#   https://terakoya.sejuku.net/question/detail/33885)
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-ipafont-gothic=00303-23 \
 && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock /workspace/
RUN uv sync
COPY . /workspace/
ENTRYPOINT ["sudo", "-u", "selenium", "uv", "run", "test.py"]
