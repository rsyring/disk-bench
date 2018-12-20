# from: https://unix.stackexchange.com/a/392091
fio \
    --directory=/data/tmp/fio \
    --output-format=json \
    --loops=2 \
    --size=1G \
    --stonewall \
    --ioengine=libaio \
    --direct=1 \
    --name=seqread --bs=1m --rw=read \
    --name=seqwrite --bs=1m --rw=write \
    --name=512Kread --bs=512k --rw=randread \
    --name=512Kwrite --bs=512k --rw=randwrite \
    --name=4kQD32read --bs=4k --iodepth=32 --rw=randread \
    --name=4kQD32write --bs=4k --iodepth=32 --rw=randwrite
