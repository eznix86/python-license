# Python License

[![PyPI version](https://badge.fury.io/py/python-license.svg)](https://badge.fury.io/py/python-license)
[![Python versions](https://img.shields.io/pypi/pyversions/python-license.svg)](https://pypi.org/project/python-license/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://github.com/eznix86/python-license/workflows/Tests/badge.svg)](https://github.com/eznix86/python-license/actions)

One command to add SPDX license headers to all your source files. Works best with pre-commit hooks.

## What It Does

Automatically adds SPDX-compliant license headers to your source files.

**For Python files:**
```python
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025  Your Name

def your_code():
    pass
```

**For JavaScript/TypeScript/Go/Rust:**
```javascript
// SPDX-License-Identifier: MIT
// Copyright (C) 2025  Your Company

function yourCode() {}
```

**For CSS:**
```css
/*
 * SPDX-License-Identifier: Apache-2.0
 * Copyright (C) 2025  Your Name
*/

body { margin: 0; }
```

**For HTML/Vue:**
```html
<!--
SPDX-License-Identifier: Apache-2.0
Copyright (C) 2025  Your Name
-->

<!DOCTYPE html>
```

### Key Features

- Supports 50+ file types including Python, JavaScript, TypeScript, Go, Rust, Java, C/C++, Swift, Kotlin, Ruby, Shell, SQL, Vue, and more
- Custom notice templates for extended license information (e.g., AGPL, GPL notices)
- Automatically updates copyright year ranges (e.g., `2023` becomes `2023-2025` when modified)
- Check mode for CI/CD integration to ensure all files have headers
- Respects `.licenseignore` and `.gitignore` files automatically
- Preserves shebang lines in executable scripts
- Handles multiple comment styles (hash, slash, dash, block comments)

## Supported Languages

**Hash comments (#):** Python, Shell (bash/zsh/fish), Ruby, Perl, R, YAML, TOML, CMake

**Slash comments (//):** JavaScript, TypeScript, Go, Rust, Java, C/C++, Swift, Kotlin, C#, PHP, Scala, Objective-C, Gradle, Groovy, SCSS, Sass, Less

**Dash comments (--):** SQL, Lua, Haskell, Elm

**Block comments:** CSS (`/* */`), HTML/XML/SVG/Vue (`<!-- -->`)

**Special files:** Dockerfile, Makefile, Jenkinsfile, Vagrantfile, Rakefile, Gemfile, Podfile, Fastfile, CMakeLists.txt, and more

## Installation

```sh
pipx install python-license
```

Or with pip:
```sh
pip install python-license
```

## Usage

### Command Line

Basic syntax:
```sh
license [options] <license-id> "<author>"
```

Examples:
```sh
# Check files without modifying (dry-run)
license --check Apache-2.0 "John Doe"

# Add/update headers in specific directory
license --fix MIT "Jane Smith" --dir src/

# Use custom ignore file
license --ignore-file .licenseignore --fix GPL-3.0 "ACME Corp"

# Process specific files only
license --fix Apache-2.0 "Your Name" file1.py file2.js

# Set custom copyright year
license --fix --year 2024 MIT "Your Company"

# Add extended notice (e.g., for AGPL, GPL licenses)
license --fix --notice-template NOTICE.template AGPL-3.0-or-later "Your Name"
```

### Pre-commit Hook (Recommended)

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/eznix86/python-license
    rev: v1.0.1
    hooks:
      - id: license-headers
        args: ['--check', 'Apache-2.0', 'Your Name']
```

For automatic fixing on commit:
```yaml
repos:
  - repo: https://github.com/eznix86/python-license
    rev: v1.0.1
    hooks:
      - id: license-headers
        args: ['--fix', 'Apache-2.0', 'Your Name']
```

See [.pre-commit-config.yaml](./.pre-commit-config.yaml) for a complete example.

### Options

| Option | Description |
|--------|-------------|
| `--check` | Check files without modifying (default mode) |
| `--fix` | Add or update headers in files |
| `--dir DIR` | Root directory to process (default: current directory) |
| `--year YEAR` | Copyright year (default: current year) |
| `--no-recursive` | Don't process subdirectories |
| `--verbose`, `-v` | Show all processed files |
| `--ignore-file FILE` | Path to ignore file (default: .licenseignore or .gitignore) |
| `--notice-template FILE` | Path to notice template file to append after copyright |
| `files` | Specific files to process (overrides --dir) |

### Notice Templates

For licenses that require extended notices (like AGPL, GPL), create a template file:

**NOTICE.template:**
```
This file is part of Your Project.

Your Project is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

See the LICENSE file for more details.
```

Then use it with:
```sh
license --fix --notice-template NOTICE.template AGPL-3.0-or-later "Your Name"
```

**Result:**
```javascript
// SPDX-License-Identifier: AGPL-3.0-or-later
// Copyright (C) 2025  Your Name
//
// This file is part of Your Project.
//
// Your Project is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// See the LICENSE file for more details.
```

### Ignore Files

Create a `.licenseignore` file to exclude specific files or directories:

```
# Ignore patterns (similar to .gitignore)
*.min.js
*.min.css
generated/*
vendor/
third_party/
build/
dist/

# Negate patterns (don't ignore these)
!important.min.js
```

If no `.licenseignore` exists, the tool automatically uses `.gitignore` patterns.

See [.licenseignore](./.licenseignore) for an example.

## FAQ

### Does it overwrite existing headers?

No, it intelligently updates them. If a file already has an SPDX header, it will:
- Update the license identifier if changed
- Update the copyright year range (e.g., `2023` → `2023-2025`)
- Preserve the existing header structure

### How does it handle copyright years?

The tool automatically manages copyright year ranges:
- First added: `Copyright (C) 2025  Your Name`
- After modification in 2026: `Copyright (C) 2025-2026  Your Name`
- If already current: no change

### Can I use it in CI/CD?

Yes! Use `--check` mode to fail the build if any files are missing headers:

```yaml
# GitHub Actions example
- name: Check license headers
  run: license --check Apache-2.0 "Your Name"
```

This returns exit code 1 if any files need updating.

### What files are excluded by default?

The tool automatically excludes common build artifacts and dependencies:
- Version control: `.git/`, `.svn/`, `.hg/`
- Dependencies: `node_modules/`, `vendor/`, `third_party/`
- Build outputs: `build/`, `dist/`, `target/`, `__pycache__/`
- Minified files: `*.min.js`, `*.min.css`
- Lock files: `*.lock`, `*.sum`, `go.mod`
- Config files: `*.json`, `*.toml`, `*.yaml`

### Can I use custom SPDX license identifiers?

Yes! Use any valid SPDX license identifier. Common examples:
- `MIT`
- `Apache-2.0`
- `GPL-3.0-or-later`
- `BSD-3-Clause`
- `ISC`

See [SPDX License List](https://spdx.org/licenses/) for all valid identifiers.

### Does it work with monorepos?

Yes! You can:
- Run it on the entire repo
- Use `--dir` to target specific packages
- Use different `.licenseignore` files in different directories
- Process specific files only

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the [Apache License 2.0](./LICENSE).

See the [NOTICE](./NOTICE) file for additional information.
