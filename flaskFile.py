from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

def save_to_database(data, emotions_list):
    # Implement the code to save the data and audio files to the MySQL database
    # You can use the 'data' dictionary for name, age, email, state, and college
    # For audio files, you can use the 'audio_files' dictionary containing file names and binary data

    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='project',
            user='root',
            password=''
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Save the data (name, age, email, state, college) to a table
            insert_query = "INSERT INTO form (name, age, email, state, college) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data_values = (data['name'], data['age'], data['state'], data['college'], data['email'], data['phone'], emotions_list[0], emotions_list[1], emotions_list[2], emotions_list[3])
            cursor.execute(insert_query, data_values)

            # Save the audio files to the database
            # for audio_key, audio_value in audio_files.items():
                # insert_audio_query = "INSERT INTO your_audio_table (name, audio_data) VALUES (%s, %s)"
                # audio_values = (audio_key, audio_value)
                # cursor.execute(insert_audio_query, audio_values)

            connection.commit()
            cursor.close()
            connection.close()

    except Error as e:
        print("Error saving data to MySQL:", e)

def convert_mp3_to_wav(mp3_file):
    # Load the MP3 file using pydub
    audio = AudioSegment.from_mp3(mp3_file)

    # Change the sample width to 2 (16-bit) to convert to WAV
    audio = audio.set_sample_width(2)

    # Save the converted WAV file
    wav_file = mp3_file.replace('.mp3', '.wav')
    audio.export(wav_file, format='wav')

    return wav_file

@app.route('/submit-audio', methods=['POST'])
def submit_audio():
    try:
        data = {
            'name': request.form.get('name'),
            'age': int(request.form.get('age')),
            'state': request.form.get('state'),
            'college': request.form.get('college'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
        }

        audio_files = {}
        emotions_list = []
        for file_key, file in request.files.items():
            if file and file.filename:
                file_name = secure_filename(file.filename)
                audio_files[file_key] = file.read()

                if file_name.endswith('.mp3'):
                    wav_file = convert_mp3_to_wav(file)
                    # audio_files[file_key] = wav_file
                    emotion = predict_audio_emotion(wav_file)
                    emotions_list.append(emotion)

        
        
        
        save_to_database(data, emotions_list)

        return jsonify({'message': 'Data submitted successfully.'})

    except Exception as e:
        print("Error processing request:", e)
        return jsonify({'error': 'An error occurred while processing the request.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
