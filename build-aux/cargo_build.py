#!/usr/bin/env python3

import sys
import os
import subprocess
import shutil

project_build_root = sys.argv[1]
project_src_root = sys.argv[2]
cargo_env = sys.argv[3]
cargo_cmd = sys.argv[4]
cargo_options = sys.argv[5]
bin_output = sys.argv[6]
output_file = sys.argv[7]

print(f"""
### executing cargo build script with arguments: ###
    project_build_root: {project_build_root}
    project_src_root: {project_src_root}
    cargo_env: {cargo_env}
    cargo_cmd: {cargo_cmd}
    cargo_options: {cargo_options}
    bin_output: {bin_output}
    output_file: {output_file}
""", file=sys.stderr)

# Set environment variables.
# The cargo_env string is "KEY=value" where value may contain spaces.
build_env = os.environ.copy()
if '=' in cargo_env:
    key, value = cargo_env.split('=', 1)
    build_env[key.strip()] = value.strip()

# Parse cargo_options: the string contains paths with spaces that cannot be
# reliably split. Instead, reconstruct the args from known paths (argv[1]/[2])
# and extract only the simple flags/values from the options string.
cargo_args = [cargo_cmd, 'build']

# Always add manifest-path and target-dir from the known-good separate arguments
manifest_path = os.path.join(project_src_root, 'Cargo.toml')
target_dir = os.path.join(project_build_root, 'target')
cargo_args += ['--manifest-path', manifest_path]
cargo_args += ['--target-dir', target_dir]

# Extract simple flags that don't have path values with spaces
# These are: -p <name>, --release, --features <...>
if '-p ' in cargo_options:
    idx = cargo_options.index('-p ')
    rest = cargo_options[idx+3:]
    pkg_name = rest.split()[0] if rest.split() else ''
    if pkg_name:
        cargo_args += ['-p', pkg_name]

if '--release' in cargo_options:
    cargo_args += ['--release']

print(f"Running: {cargo_args}", file=sys.stderr)
res = subprocess.run(cargo_args, env=build_env)
if res.returncode != 0:
    print(f"cargo call failed, code {res.returncode}", file=sys.stderr)
    sys.exit(1)

# Copy the binary output
# On Windows, append .exe if not already present
bin_output_path = bin_output
if sys.platform == 'win32' and not bin_output_path.endswith('.exe'):
    bin_output_path += '.exe'

print(f"Copying {bin_output_path} -> {output_file}", file=sys.stderr)
try:
    shutil.copy2(bin_output_path, output_file)
except Exception as e:
    print(f"copy failed: {e}", file=sys.stderr)
    sys.exit(1)

print("### cargo build script finished ###", file=sys.stderr)
