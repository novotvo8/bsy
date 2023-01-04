#!/bin/sh
clone()
{
    git clone https://novotvo8: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@gist.github.com/5f6e9ef9fe8a3a54b74dff0c94fd61e1.git
}

cd controller
clone
# rm -rf 5f6e9ef9fe8a3a54b74dff0c94fd61e1/.git
# rm -r 5f6e9ef9fe8a3a54b74dff0c94fd61e1
cd ../

for i in 0 1 2
do
    cp -R controller/5f6e9ef9fe8a3a54b74dff0c94fd61e1 bot$i
    # rm -rf bot$i/5f6e9ef9fe8a3a54b74dff0c94fd61e1/.git
    # rm -r bot$i/5f6e9ef9fe8a3a54b74dff0c94fd61e1
done