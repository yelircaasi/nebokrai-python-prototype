{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        projectName = "nebokrai";
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryEditablePackage;
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryEnv;
      in
      {
        packages = {
          ${projectName} = mkPoetryApplication {
            python = pkgs.python311;
            projectDir = self; 
            preferWheels = true; 
          };
          #${projectName} = mkPoetryEditablePackage {
          #  projectDir = ./.;
          #  python = pkgs.python311;
          #  editablePackageSources = {
          #    ${projectName} = ./src;
          #  };
          # preferWheels = true;
          #};
          #${projectName} = mkPoetryEnv {
          #  python = pkgs.python311;
          #  pyproject = ./pyproject.toml;
          #  poetrylock = ./poetry.lock;
          #  projectDir = ./.;
          #  editablePackageSources = {
          #    ${projectName} = ./src;
          #  };
          #  preferWheels = true;
          #};
          default = self.packages.${system}.${projectName};
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.${projectName} ];

          packages = with pkgs; [ 
            poetry 
            check-jsonschema 
            self.packages.${system}.${projectName}
          ];
        };
      });
}
