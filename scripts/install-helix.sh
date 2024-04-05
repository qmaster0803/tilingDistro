# Download tar and extracr
mkdir -p $HOME/Software
cd $HOME/Software
wget "https://github.com/helix-editor/helix/releases/download/24.03/helix-24.03-x86_64-linux.tar.xz"
tar xf helix-24.03-x86_64-linux.tar.xz
rm helix-24.03-x86_64-linux.tar.xz

mv helix-24.03-x86_64-linux helix-24.03
cd helix-24.03

# Link helix/runtime to ~/.config/helix/runtime
mkdir -p $HOME/.config/helix
ln -s $HOME/Software/helix-24.03-x86_64-linux.tar.xz/runtime $HOME/.config/helix/
