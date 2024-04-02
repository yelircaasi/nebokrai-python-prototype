{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "nixpkgs";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
  }:
    {
      # Nixpkgs overlay providing the application
      overlay = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
        (final: prev: {
          # The application
          nebokrai = prev.poetry2nix.mkPoetryEnv {
            projectDir = ./.;
            editablePackageSources = {
              nebokrai = ./src/nebokrai;
            };
          };
        })
      ];
    }
    // (flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [self.overlay];
      };
    in rec {
      devShells = {
        nebokrai = pkgs.mkreports;
      };

      packages = {
        nebokrai = pkgs.nebokrai;
      };
      devShell = devShells.nebokrai;
    }));
}
