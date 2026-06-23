#!/bin/bash
# Build script for rnote on Windows ARM64 (CLANGARM64)
set -euxo pipefail

export MSYSTEM=CLANGARM64
export PATH="/clangarm64/bin:/c/Users/Johan/.cargo/bin:$PATH"
export PKG_CONFIG_PATH="/clangarm64/lib/pkgconfig:/clangarm64/share/pkgconfig"

echo "=== Environment ==="
echo "MSYSTEM=$MSYSTEM"
echo "clang: $(clang --version | head -1)"
echo "rustc: $(rustc --version)"
echo "cargo: $(cargo --version)"
echo "pkg-config: $(pkg-config --version)"

cd "/c/Users/Johan/OneDrive - uni-bielefeld.de/Dokumente/Programmieren/C#/rnote"

echo "=== Git Submodules ==="
git submodule update --init --recursive || echo "No submodules or already initialized"

echo "=== Meson Setup ==="
meson setup \
    --prefix=C:/msys64/clangarm64 \
    -Dprofile=devel \
    -Dwin-build-environment-path=C:/msys64/clangarm64 \
    _mesonbuild

echo "=== Meson Compile ==="
meson compile -C _mesonbuild

echo "=== BUILD COMPLETE ==="
