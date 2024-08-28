import berserk
import os

def export_studies_from_file(input_file, repertoire_file, backup_dir, session, client):
    """Fetch and save all studies listed in a file to individual backup files and a compiled PGN file."""
    # Initialize a session using the API token
    
    # Ensure the backup directory exists
    os.makedirs(backup_dir, exist_ok=True)
    requestor = berserk.session.Requestor(session=session, base_url='https://lichess.org', default_fmt=berserk.formats.TEXT)

    # Open the output file for the repertoire
    with open(repertoire_file, 'w') as pgn_file:
        # Read each study ID from the input file
        with open(input_file, 'r') as infile:
            for line in infile:
                study_id = line.strip()
                if study_id:  # Ensure the line is not empty
                    try:
                        # Fetch the study's PGN content
                        url = f'api/study/{study_id}.pgn?source=true&orientation=true'
                        
                        response = requestor.request(
                            method="GET",
                            path=url,
                        )


                        # Create a backup file for the current study
                        backup_file_path = os.path.join(backup_dir, f'{study_id}.pgn')
                        with open(backup_file_path, 'w') as backup_file:
                            backup_file.write(response + "\n\n")
                            pgn_file.write(response + "\n\n")
                    
                    except berserk.exceptions.ResponseError as e:
                        print(f"Failed to fetch or save study {study_id}: {e}")
                    except Exception as e:
                        print(f"An error occurred while processing study {study_id}: {e}")
    
    print(f"Studies from {input_file} have been exported and backed up.")
