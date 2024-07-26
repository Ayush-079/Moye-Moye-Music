
import sqlite3


def push(name, duration, audio_path, thumbnail_path):
    
    
    conn = sqlite3.connect('songs_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT audio_blob, thumbnail FROM audio_data WHERE filename = ? LIMIT 1', (name,))
        result = cursor.fetchone()
        if result:
            print('data already exists.....')
            return 0
        else:
            pass
    except:
        pass
    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_data (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            audio_blob BLOB,
            duration REAL,
            thumbnail BLOB
        )
    ''')

    # Read audio and thumbnail content
    with open(audio_path, 'rb') as mp3_file:
        audio_content = mp3_file.read()

    with open(thumbnail_path, 'rb') as mp3_file:
        thumbnail_content = mp3_file.read()

    # Insert data into the table
    cursor.execute('''
        INSERT INTO audio_data (filename, audio_blob, duration, thumbnail)
        VALUES (?, ?, ?, ?)
    ''', (name, audio_content, duration, thumbnail_content))
    # cursor.execute('SELECT audio_blob,thumbnail FROM audio_data WHERE filename = ? and thumbnail=?', (filename,thumbnail))
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("saved into database")





def get(audio_keyword):
    # Connect to the database
    conn = sqlite3.connect('songs_database.db')
    cursor = conn.cursor()

    # Prepare the search pattern with wildcards for partial matching
    search_pattern = f"%{audio_keyword}%"

    # Fetch the audio data with partial matching
    cursor.execute('SELECT audio_blob, thumbnail, duration, filename FROM audio_data WHERE filename LIKE ? LIMIT 1', (search_pattern,))
    result = cursor.fetchone()
    if result:
        audio_blob = result[0]
        thumbnail = result[1]
        duration = result[2]
        filename=result[3]
        print(f"Audio, duration, and thumbnail data for '{audio_keyword}' retrieved successfully.")
    else:
        audio_blob = None
        thumbnail = None
        print(f"No audio data found for '{audio_keyword}'.")

    # Close the connection
    conn.close()
    return audio_blob, thumbnail, duration, filename


