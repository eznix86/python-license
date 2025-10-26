# Python License

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Automatically adds or updates SPDX license and copyright headers in source files.
Designed for use in pre-commit hooks.

## Installation

```sh
pipx install python-license
```

## Usage
```sh
license <license> "<author>" [options]
```
Examples:

```sh
license GPL-2.0-or-later "John Doe" --check
license MIT "Jane Smith" --fix --dir src/
license Apache-2.0 "ACME Corp" --ignore-file .licenseignore --fix
```

Check [.pre-commit-config.yaml](./.pre-commit-config.yaml) as an example.

Note. `.licenseignore` is a file that can be used to ignore specific files or directories from being processed. Example in [.licenseignore](./.licenseignore)

## License

This project is licensed under the [Apache License 2.0](./LICENSE).

See the [NOTICE](./NOTICE) file for additional information.
