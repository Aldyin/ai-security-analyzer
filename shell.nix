{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.pip
    python312Packages.virtualenv
    python312Packages.tkinter

    gcc
    zlib
    openssl
    libffi

    cudaPackages.cudatoolkit
    cudaPackages.cuda_cudart
    cudaPackages.cuda_nvcc

    linuxPackages.nvidia_x11
  ];

  shellHook = ''
    export CUDA_PATH=${pkgs.cudaPackages.cudatoolkit}

    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
      pkgs.zlib
      pkgs.openssl
      pkgs.libffi
      pkgs.stdenv.cc.cc.lib

      pkgs.cudaPackages.cudatoolkit
      pkgs.cudaPackages.cuda_cudart
      pkgs.linuxPackages.nvidia_x11
    ]}:$LD_LIBRARY_PATH

    source .venv/bin/activate
  '';
}