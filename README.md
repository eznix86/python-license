# Python License

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Automatically adds or updates SPDX license and copyright headers in source files.
Designed for use in pre-commit hooks.

## Installation

```sh
pip install python-license
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

## License

This project is licensed under the [Apache License 2.0](./LICENSE).

See the [NOTICE](./NOTICE) file for additional information.
