{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    cowsay
    (python311.withPackages (ps: with ps; [ pip ]))
  ];
  shellHook = ''
    export LC_ALL=C
    cowsay "Happy Hacking ;)"
  '';
}
