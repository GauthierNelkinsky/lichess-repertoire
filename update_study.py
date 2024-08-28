import berserk
import re
import os
from delete_chapter import delete_chapter_from_study

def extract_chapter_id(header):
    """
    Extracts chapter_id from the 'Source' header of a PGN file.
    
    Parameters:
    - header: The PGN header where 'Source' is expected to be present.
    
    Returns:
    - The chapter_id extracted from the 'Source' header or None if not found.
    """
    match = re.search(r'https://lichess.org/study/[^/]+/([^/]+)', header)
    return match.group(1) if match else None

def extract_event_name(pgn_data):
    """
    Extracts the event name from the first game in the PGN data.
    
    Parameters:
    - pgn_data: The full PGN data as a string.
    
    Returns:
    - The event name from the 'Event' header or a default name if not found.
    """
    match = re.search(r'\[Event\s*"([^"]+)"\]', pgn_data)
    return match.group(1) if match else "Unnamed Chapter"

def update_study(study_file, client, session, orientation):
    """
    Updates the study by deleting existing chapters and adding new ones.
    
    Parameters:
    - study_file: The path to the PGN file containing the study's new chapters.
    - client: A Berserk Client object (authenticated).
    - session: A Berserk session object (authenticated).
    - orientation: The orientation for the new chapters ('white' or 'black').
    """
    study_id = os.path.splitext(os.path.basename(study_file))[0]
    print(f"Updating study {study_id}...")

    # Read the PGN file and extract chapter data
    with open(study_file, 'r') as f:
        pgn_data = f.read()

    headers = re.findall(r'\[Source "([^"]+)"\]', pgn_data)
    chapter_name = extract_event_name(pgn_data)  # Extract chapter name from the Event header

    # Extract existing chapter IDs
    existing_chapters = [extract_chapter_id(header) for header in headers if extract_chapter_id(header)]

    # Manually push the optimized PGN data to the study
    try:
        url = f'api/study/{study_id}/import-pgn'
        data = {
            "name": chapter_name,
            "pgn": pgn_data,
            "orientation": orientation,
        }
        requestor = berserk.session.Requestor(session=session, base_url='https://lichess.org', default_fmt=berserk.formats.JSON)

        response = requestor.request(
            method="POST",
            path=url,
            data=data
        )
        print(f"Optimized chapters added to study {study_id} with orientation {orientation}.")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Failed to add optimized chapters to study {study_id}: {e}")

    # Delete existing chapters from the study
    for chapter_id in existing_chapters:
        try:
            delete_chapter_from_study(session, study_id, chapter_id)
        except Exception as e:
            print(f"Failed to delete chapter {chapter_id} from study {study_id}: {e}")
