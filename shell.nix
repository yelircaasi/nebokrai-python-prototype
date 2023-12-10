# not working yet -> poetry2nix
with import <nixpkgs> {};
with pkgs.python3Packages;

buildPythonPackage rec {
  name = "nebokrai";
  src = "./";
  propagatedBuildInputs = [ poetry-core ];
}