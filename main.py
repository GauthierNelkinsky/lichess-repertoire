import configparser
import os
from download_studies import export_studies_from_file
from optimize import optimize
from update_study import update_study
from datetime import datetime
from find_errors import find_errors
import berserk

def main():
    # Load configuration from config.txt
    config = configparser.ConfigParser()
    config.read('config.txt')

    # Directories and files from configuration
    input_dir = config['Paths']['input_dir']
    output_dir = config['Paths']['output_dir']
    api_token = config['API']['token']

    # Actions configuration
    actions = {
        "log": config.getboolean('Actions', 'log'),
        "optimize": config.getboolean('Actions', 'optimize'),
        "update": config.getboolean('Actions', 'update'),
        "find_errors": config.getboolean('Actions', 'find_errors')
    }

    session = berserk.TokenSession(api_token)
    client = berserk.Client(session=session)

    # Define paths for input files
    black_input_file = os.path.join(input_dir, config['Files']['black_input'])
    white_input_file = os.path.join(input_dir, config['Files']['white_input'])

    # Create directories for the output files
    repertoires_dir = os.path.join(output_dir, 'repertoires')
    optimized_studies_dir = os.path.join(output_dir, 'optimized', 'studies')
    optimized_repertoires_dir = os.path.join(output_dir, 'optimized', 'repertoires')
    
    os.makedirs(repertoires_dir, exist_ok=True)
    os.makedirs(optimized_studies_dir, exist_ok=True)
    os.makedirs(optimized_repertoires_dir, exist_ok=True)

    # Generate a timestamp for the backup directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join('./backup', timestamp)
    os.makedirs(backup_dir, exist_ok=True)

    # Define output files for repertoires
    black_output_file = os.path.join(repertoires_dir, 'black_repertoire.pgn')
    white_output_file = os.path.join(repertoires_dir, 'white_repertoire.pgn')

    # Export studies for black and white repertoires
    if actions["log"]:
        print("Starting study export...")
    export_studies_from_file(black_input_file, black_output_file, os.path.join(backup_dir, 'black'), session, client)
    export_studies_from_file(white_input_file, white_output_file, os.path.join(backup_dir, 'white'), session, client)

    # Optimize the exported PGN files for repertoires
    if actions["optimize"]:
        optimize(black_output_file, os.path.join(optimized_repertoires_dir, 'black_optimized.pgn'))
        optimize(white_output_file, os.path.join(optimized_repertoires_dir, 'white_optimized.pgn'))

    # Optimize each backup file and save to the optimized studies directory, then update the study
    if actions["optimize"] or actions["update"]:
        for root, _, files in os.walk(backup_dir):
            for file in files:
                if file.endswith('.pgn'):
                    backup_file_path = os.path.join(root, file)

                    # Recreate the subdirectory structure within optimized_studies_dir
                    relative_path = os.path.relpath(root, backup_dir)
                    optimized_file_dir = os.path.join(optimized_studies_dir, relative_path)
                    os.makedirs(optimized_file_dir, exist_ok=True)

                    optimized_file_path = os.path.join(optimized_file_dir, file)

                    if actions["optimize"]:
                        try:
                            optimize(backup_file_path, optimized_file_path)
                            if actions["log"]:
                                print(f"Optimized {backup_file_path} and saved to {optimized_file_path}.")
                        except Exception as e:
                            if actions["log"]:
                                print(f"Failed to optimize {backup_file_path}: {e}")

                    if actions["update"]:
                        # Determine the orientation based on the directory structure
                        if 'white' in relative_path.lower():
                            orientation = 'white'
                        elif 'black' in relative_path.lower():
                            orientation = 'black'
                        else:
                            orientation = 'unknown'

                        try:
                            update_study(optimized_file_path, client, session, orientation)
                            if actions["log"]:
                                print(f"Updated study from {optimized_file_path} with orientation {orientation}.")
                        except Exception as e:
                            if actions["log"]:
                                print(f"Failed to update study from {optimized_file_path}: {e}")

    # Find errors
    if actions["find_errors"]:
        find_errors(black_output_file, os.path.join(output_dir, config['Files']['black_errors_file']), "black")
        find_errors(white_output_file, os.path.join(output_dir, config['Files']['white_errors_file']), "white")

if __name__ == "__main__":
    main()
