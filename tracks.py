from flask import  Flask, request, jsonify, g
import sqlite3
import uuid


app = Flask(__name__)
app.config["DEBUG"] = True

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db(key):
    if key == 0:
        db = getattr(g, '_database', None)
        if db is None:
            print("shard 1")
            db = g._database = sqlite3.connect('TRACKSDATABASE_1')
            db.row_factory = make_dicts
        db.cursor().execute("PRAGMA foreign_keys=ON")
        return db
    elif key == 1:
        db1 = getattr(g, '_database1', None)
        if db1 is None:
            print("shard 2")
            db1 = g._database = sqlite3.connect('TRACKSDATABASE_2')
            db1.row_factory = make_dicts
        db1.cursor().execute("PRAGMA foreign_keys=ON")
        return db1
    elif key == 2:
        db2 = getattr(g, '_database2', None)
        if db2 is None:
            print("shard 3")
            db2 = g._database = sqlite3.connect('TRACKSDATABASE_3')
            db2.row_factory = make_dicts
        db2.cursor().execute("PRAGMA foreign_keys=ON")
        return db2

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    db1 = getattr(g, '_database1', None)
    if db1 is not None:
        db1.close()
    db2 = getattr(g, '_database2', None)
    if db2 is not None:
        db2.close()




@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db(0)
        with app.open_resource('music_store_tracks.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db1 = get_db(1)
        with app.open_resource('music_store_tracks_2.sql', mode='r') as f:
            db1.cursor().executescript(f.read())
        db1.commit()
        db2 = get_db(2)
        with app.open_resource('music_store_tracks_3.sql', mode='r') as f:
            db2.cursor().executescript(f.read())
        db2.commit()

def get_shard(shard_key):
    shard = shard_key%3
    return shard


def query_db(query,args=(),one=False):
    cur = get_db(0).execute(query,args)
    rv = cur.fetchall()
    cur.close()
    return(rv[0] if rv else None) if one else rv




# #To get all tracks
# @app.route('/api/v1/resources/tracks',methods=['GET'])
# def GetTrack():
#     query_parameters = request.args
#     track_title = query_parameters.get('track_title')
#     album_title = query_parameters.get('album_title')
#     artist = query_parameters.get('artist')
#     length = query_parameters.get('length')
#     album_art_url = query_parameters.get('album_art_url')
#     track_url= query_parameters.get('track_url')

#     query = "SELECT * FROM tracks WHERE"
#     to_filter = []

#     if track_title:
#         query += ' track_title=? AND'
#         to_filter.append(track_title)

#     if album_title:
#         query += ' album_title=? AND'
#         to_filter.append(album_title)

#     if artist:
#         query += ' artist=? AND'
#         to_filter.append(artist)

#     if length:
#         query += ' length=? AND'
#         to_filter.append(length)

#     if album_art_url:
#         query += ' album_art_url=? AND'
#         to_filter.append(album_art_url)

#     if track_url:
#         query += ' track_url=? AND'
#         to_filter.append(track_url)



#     query = query[:-4] + ';'
#     results = query_db(query, to_filter)
#     if not results:
#         return jsonify("No track present"),404
#     else:
#         resp = jsonify(results)
#         resp.headers['Location'] = 'http://127.0.0.1:5200/api/v1/resources/tracks'
#         resp.status_code = 200
#         return resp


# #To post a new track
# @app.route('/api/v1/resources/tracks',methods=['POST'])
# def InsertTrack():
#         if request.method == 'POST':
#             data =request.get_json(force= True)
#             track_title = data['track_title']
#             album_title = data['album_title']
#             artist = data['artist']
#             length = data['length']
#             track_url = data['track_url']
#             album_art_url = data['album_art_url']

#             executionState:bool = False

#             if track_url:

#                 query ="INSERT INTO tracks(track_title, album_title, artist, length, track_url, album_art_url) VALUES('"+track_title+"','"+album_title+"','"+artist+"','"+length+"','"+track_url+"','"+album_art_url+"');"
#                 print(query)
#                 cur = get_db().cursor()
#                 try:
#                     cur.execute(query)
#                     if(cur.rowcount >=1):
#                         executionState = True
#                     get_db().commit()
#                 except:
#                     get_db().rollback()
#                     print("Error")
#                 finally:
#                     if executionState:
#                         resp = jsonify(message="Data Inserted Successfully")
#                         resp.headers['Location'] = 'http://127.0.0.1:5200/api/v1/resources/playlist?track_url='+track_url
#                         resp.status_code = 201
#                         return resp
#                     else:
#                         return jsonify(message="Failed to insert data"), 409

#             else:
#                 return jsonify(message="Failed to insert data"),409



# #To edit a track
# @app.route('/api/v1/resources/tracks',methods=['PUT'])
# def EditTrack():
#         if request.method == 'PUT':
#             data =request.get_json(force= True)
#             track_title = data['track_title']
#             album_title = data['album_title']
#             artist = data['artist']
#             length = data['length']
#             track_url = data['track_url']
#             album_art_url = data['album_art_url']
#             query_parameters = request.args
#             track_url_param = query_parameters.get('track_url')

#             executionState:bool = False
#             if track_url == track_url_param:
#                 query ="UPDATE tracks SET track_title='"+track_title+"', album_title='"+album_title+"', artist='"+artist+"', length='"+length+"', album_art_url='"+album_art_url+"'  WHERE track_url='"+track_url+"';"
#                 print(query)
#                 cur = get_db().cursor()
#                 try:
#                     cur.execute(query)
#                     if(cur.rowcount >=1):
#                         executionState = True
#                     get_db().commit()
#                 except:
#                     get_db().rollback()
#                 finally:
#                     if executionState:
#                         resp = jsonify(message="Data updated successfully")
#                         resp.headers['Location'] = 'http://127.0.0.1:5200/api/v1/resources/tracks?track_url='+track_url
#                         resp.status_code = 200
#                         return resp

#                     else:
#                         return jsonify(message="Failed to edit data"), 409
#             else:
#                 return jsonify(message="Failed to edit data"), 409



# #To delete a track
# @app.route('/api/v1/resources/tracks', methods=['DELETE'])
# def DeleteTrack():
#         if request.method == 'DELETE':
#             query_parameters = request.args
#             track_url = query_parameters.get('track_url')
#             executionState:bool = False
#             cur = get_db().cursor()
#             try:
#                 cur.execute("DELETE FROM tracks WHERE track_url=?",(track_url,))

#                 if cur.rowcount >= 1:
#                     executionState = True
#                 get_db().commit()

#             except:
#                     get_db().rollback()
#                     print("Error")
#             finally:
#                     if executionState:
#                         return jsonify(message="Data SucessFully deleted"), 200
#                     else:
#                         return jsonify(message="Failed to delete data"), 409

app.run()
