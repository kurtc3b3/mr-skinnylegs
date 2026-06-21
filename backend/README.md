mkdkir obscura-tmp
cd obscura-tmp

curl -LO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-aarch64-macos.tar.gz
tar xzf obscura-aarch64-macos.tar.gz
./obscura --version


./obscura fetch https://example.com --eval "document.title"
docker run -d --name obscura -p 127.0.0.1:9222:9222 h4ckf0r0day/obscura

./obscura serve --port 9222


curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustc --version
cargo --version
git clone https://github.com/h4ckf0r0day/obscura.git
cd obscura
cargo build --release -p obscura-cli --bin obscura
# binary: target/release/obscura


obscura scrape url1 url2 --eval "document.title" --format json
