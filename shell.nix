{ pkgs ? import <nixpkgs> {} }:
let 
  nebokrai = pkgs.poetry2nix.mkPoetryEnv {
    python = pkgs.python311;
    projectDir = ./.;
    editablePackageSources = {
      nebokrai = ./src;
    };
    preferWheels = true;
  };
in nebokrai.env
