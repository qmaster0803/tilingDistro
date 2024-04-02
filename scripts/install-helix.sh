# Install Rust compiler
wget https://sh.rustup.rs -O rustup.sh
bash rustup.sh -y
rm rustup.sh

# Reload terminal
source ~/.zshrc

# Install Helix
git clone https://github.com/helix-editor/helix
cd helix
cargo install --path helix-term --locked

# Fetch and compile Helix grammar
hx --grammar fetch
hx --grammar build
