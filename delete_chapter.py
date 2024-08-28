import berserk

def delete_chapter_from_study(session, study_id, chapter_id):
    """
    Deletes a chapter from a Lichess study using the Lichess API.
    
    Parameters:
    - session: A Berserk session object (authenticated).
    - study_id: The ID of the Lichess study.
    - chapter_id: The ID of the chapter to delete.
    """
    # Correct API path for the DELETE request
    path = f'api/study/{study_id}/{chapter_id}'

    # Create a Requestor object with the session and default format as JSON
    requestor = berserk.session.Requestor(session=session, base_url='https://lichess.org', default_fmt=berserk.formats.TEXT)
    
    # Perform the DELETE request
    try:
        response = requestor.request(method='DELETE', path=path)
        print(f"Chapter {chapter_id} successfully deleted from study {study_id}.")
    except berserk.exceptions.ResponseError as e:
        print(f"Failed to delete chapter {chapter_id} from study {study_id}: {e}")
