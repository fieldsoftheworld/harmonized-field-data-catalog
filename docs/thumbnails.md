# Rendering a thumbnail

Every collection needs one: `PTL-VIZ-001` fails a collection without an asset
in the `thumbnail` role, so a new collection fails the gates until it has one.

`tools/thumbnail.py` renders it from the collection's own MapLibre style with
[chiitiler](https://github.com/Kanahiro/chiitiler), which draws server-side
with maplibre-gl-native. That needs Node and a GL stack, so it does not run
everywhere.

## What the machine needs

**Node** comes from the pixi environment (`nodejs` is a dependency of this
repository), so no root is needed for it.

**The GL libraries do need root.** maplibre-gl-native renders through EGL:

    sudo apt-get install -y libegl1 libgles2 libgbm1 libopengl0 \
        libx11-6 libxext6 libxrandr2 libxi6 libxcursor1 libxinerama1

On a machine where EGL finds no device, run the server under `xvfb-run -a`
(`sudo apt-get install -y xvfb`).

## Running it

Clone chiitiler once, somewhere with room — not `/tmp` on the conversion
server, which is small:

    git clone --depth 1 https://github.com/Kanahiro/chiitiler /data/cache/fiboa/tools/chiitiler
    cd /data/cache/fiboa/tools/chiitiler
    pixi run --manifest-path ~/fiboa/harmonized-field-data-catalog npm install

Start it in a screen and leave it there:

    screen -dmS chiitiler bash -lc 'cd /data/cache/fiboa/tools/chiitiler && \
        CHIITILER_PROCESSES=0 npx tsx src/main.ts tile-server --port 13579 --cache memory'
    curl -s -o /dev/null -w "%{http_code}\n" http://localhost:13579/health   # 200

Then, from this repository:

    pixi run thumbnail se                  # writes catalog/se/thumbnail.jpg
    pixi run thumbnail se --center 13.3,55.7   # frame it yourself
    pixi run thumbnail se --rank 1         # the second-densest cluster

The tool needs the edition's `.pmtiles` and the collection's
`latest/<id>.parquet` where the collection.json points, which on the
conversion server is what `staging/` already holds.

**Look at the image.** The gate only proves that something landed in the
frame, not that the picture is good. A frame centred on a city or a lake
passes the blank check and still looks empty.

## Without a GL stack

Copy the two files to a machine that has one (a laptop) and render there:

    scp <server>:~/fiboa/harmonized-field-data-catalog/staging/se/year=2025/se-2025.pmtiles catalog/se/year=2025/
    scp <server>:~/fiboa/harmonized-field-data-catalog/staging/se/latest/se.parquet catalog/se/latest/

`catalog/**` ignores `*.parquet` and `*.pmtiles`, so the copies stay out of
the repository; only `thumbnail.jpg` is committed.
