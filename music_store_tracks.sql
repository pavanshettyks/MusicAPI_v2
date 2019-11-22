-- $ sqlite3 music_store.db < sqlite.sql


PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS tracks;

CREATE TABLE tracks (
	track_title VARCHAR,
	album_title VARCHAR,
	artist VARCHAR,
	length TIME,
	track_url VARCHAR,
	album_art_url VARCHAR,
	track_uuid GUID primary key
);

/*
INSERT INTO tracks(track_title, album_title, artist, length, track_url) VALUES('Stronger','Graduation', 'Kanye West', '00:05:11','/home/student/Music/tracks/Stronger.mp3');
INSERT INTO tracks(track_title, album_title, artist, length, track_url) VALUES('Yeah!','Confessions', 'Usher', '00:04:10','/home/student/Music/tracks/Yeah.mp3');
INSERT INTO tracks(track_title, album_title, artist, length, track_url) VALUES('I Gotta Feeling','The E.N.D.', 'The Black Eyed Peas', '00:04:48','/home/student/Music/tracks/I_Gotta_Feeling.mp3');
*/