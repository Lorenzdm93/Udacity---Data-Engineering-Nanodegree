import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

ARN = config.get("IAM_ROLE", "ARN")
LOG_DATA = config.get("S3", "LOG_DATA")
LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_event"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_song"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_event (
        artist VARCHAR,
        auth VARCHAR,
        firstName VARCHAR,
        gender CHAR(1),
        itemInSession INT,
        lastName VARCHAR,
        length FLOAT,
        level VARCHAR,
        location TEXT,
        method VARCHAR,
        page VARCHAR,
        registration VARCHAR,
        sessionId INT,
        song VARCHAR,
        status INT,
        ts BIGINT,
        userAgent TEXT,
        userId INT
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_song (
        artist_id VARCHAR,
        artist_latitude FLOAT,
        artist_location TEXT,
        artist_longitude FLOAT,
        artist_name VARCHAR,
        duration FLOAT,
        num_songs INT,
        song_id VARCHAR,
        title VARCHAR,
        year INT
    )
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplay (
        songplay_id INT IDENTITY(0,1),
        start_time TIMESTAMP,
        user_id INT,
        level VARCHAR,
        song_id VARCHAR,
        artist_id VARCHAR,
        session_id INT,
        location TEXT,
        user_agent TEXT
    )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT,
        first_name VARCHAR,
        last_name VARCHAR,
        gender CHAR(1),
        level VARCHAR
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS song (
        song_id VARCHAR,
        title VARCHAR,
        artist_id VARCHAR,
        year INT,
        duration FLOAT
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artist (
        artist_id VARCHAR,
        name VARCHAR,
        location TEXT ,
        latitude FLOAT ,
        longitude FLOAT
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP,
        hour INT,
        day INT,
        week INT,
        month INT,
        year INT,
        weekday VARCHAR
    ) """)

# STAGING TABLES

staging_events_copy = ("""
    copy staging_event
    from {0}
    iam_role {1}
    json {2};
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    copy staging_song
    from {0}
    iam_role {1}
    json 'auto';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT 
        distinct timestamp with time zone 'epoch' + ste.ts/1000 * interval '1 second', 
        ste.userId, 
        ste.level, 
        sts.song_id, 
        sts.artist_id, 
        ste.sessionId, 
        ste.location, 
        ste.userAgent
    FROM staging_event ste 
    INNER JOIN staging_song sts
        ON ste.song = sts.title 
        AND ste.artist = sts.artist_name 
        AND ste.length = sts.duration
    WHERE ste.page = 'NextSong'
    """)

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT 
        DISTINCT userId, 
        firstName, 
        lastName, 
        gender, 
        level
    FROM staging_event
    WHERE page = 'NextSong' 
    AND userId is not null
""")

song_table_insert = ("""
    INSERT INTO song (song_id, title, artist_id, year, duration)
    SELECT 
        DISTINCT song_id, 
        title, 
        artist_id, 
        year, 
        duration
    FROM staging_song
    WHERE song_id is not null
""")

artist_table_insert = ("""
    INSERT INTO artist (artist_id, name, location, latitude, longitude)
    SELECT 
        DISTINCT artist_id, 
        artist_name, 
        artist_location, 
        artist_latitude, 
        artist_longitude
    FROM staging_song
    WHERE artist_id is not null
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT 
        start_time, 
        extract(hour from start_time), 
        extract(day from start_time), 
        extract(week from start_time), 
        extract(month from start_time), 
        extract(year from start_time), 
        extract(weekday from start_time)
    FROM songplay""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
