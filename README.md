# Chess Study Optimization Script

This project provides a script to automate the process of downloading, optimizing, and updating chess studies. The script reads from a configuration file to determine which actions to perform and where to store the results.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Input Files](#input-files)
- [Usage](#usage)
- [Actions](#actions)
- [Backup and Repository Files](#backup-and-repository-files)
- [License](#license)

## Features

- **Download Studies:** Automatically download chess studies from the specified input files.
- **Optimize PGN Files:** Optimize downloaded chess studies by removing duplicates and adding FEN headers.
- **Update Studies:** Update existing chess studies on Lichess using optimized data.
- **Configurable Actions:** Enable or disable specific actions like logging, optimization, and updating through the configuration file.

## Requirements

- Python 3.x
- `berserk` Python library (for Lichess API interaction)

To install the required Python libraries, you can use:

```bash
pip install berserk
```

## Configuration

The script uses a `config.txt` file to determine input and output paths, files, API tokens, and actions to perform. Below is a sample configuration file:

### Sample `config.txt`

```ini
[Paths]
input_dir = ./input
output_dir = ./output

[Files]
black_input = blackstudies.txt
white_input = whitestudies.txt
black_output = blackrepertoire.pgn
white_output = whiterepertoire.pgn
black_optimized_output = blackrepertoire_optimized.pgn
white_optimized_output = whiterepertoire_optimized.pgn

[API]
token = your_lichess_api_token_here

[Actions]
log = True
optimize = True
update = True
```

### Configuration Parameters

- **Paths**:
  - `input_dir`: Directory containing input study files.
  - `output_dir`: Directory where the output files will be saved.

- **Files**:
  - `black_input`: Filename for the black studies input list.
  - `white_input`: Filename for the white studies input list.
  - `black_output`: Filename for the black repertoire PGN output.
  - `white_output`: Filename for the white repertoire PGN output.
  - `black_optimized_output`: Filename for the optimized black repertoire PGN.
  - `white_optimized_output`: Filename for the optimized white repertoire PGN.

- **API**:
  - `token`: Your Lichess API token for authentication.

- **Actions**:
  - `log`: Enable or disable logging of actions (`True` or `False`).
  - `optimize`: Enable or disable optimization of PGN files (`True` or `False`).
  - `update`: Enable or disable updating studies on Lichess (`True` or `False`).
  - `find_errors`: Enable or disable logging of errors (`True`or `False`).


## Input Files

The input files (`blackstudies.txt` and `whitestudies.txt`) contain a list of Lichess study IDs. These IDs correspond to the studies you wish to download and process.

Each line in the input file represents a unique Lichess study ID. The script will read these IDs, download the corresponding studies, and perform the configured actions such as optimization and updating.

## Usage

1. **Configure the script**: Edit the `config.txt` file to specify your input/output paths, file names, API token, and desired actions.
2. **Prepare Input Files**: Create text files (e.g., `blackstudies.txt`, `whitestudies.txt`) in the input directory, listing the Lichess study IDs you wish to process.
3. **Run the script**: Execute the main script by running:

    ```bash
    python main.py
    ```

4. **Output**: The script will create output and optimized directories based on the configuration, and save logs, optimized files, and other results accordingly.

## Actions

The script supports the following configurable actions:

- **Log**: Prints logs to the console about the script's progress.
- **Optimize**: Processes and optimizes PGN files.
- **Update**: Updates studies on Lichess using the optimized data.

## Backup and Repository Files

When the script downloads studies, it stores them in a backup directory with a timestamp, preserving the original versions. In addition to this, the script creates a "Repository file" that merges all the downloaded studies into a single large PGN file. This repository file can be particularly useful for training your repertoire using tools like [listudy.org](https://listudy.org).

The repository file is saved in the specified output directory and contains all the downloaded studies, allowing for comprehensive analysis and training.

## Contributing

Contributions to improve this repository are welcome! If you have any suggestions, feature requests, or bug fixes, feel free to fork the repository, make your changes, and submit a pull request. Let's collaborate to make this tool even better.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.