from flask import Flask, request, render_template_string

app = Flask(__name__)

# This will hold the last received data
last_received_data = ""

@app.route('/postdata', methods=['POST'])
def receive_data():
    global last_received_data
    json_data = request.data  # Get JSON data from POST
    last_received_data = str(json_data)  # Convert JSON to string
    return {'status': 'success', 'message': 'Data received'}

@app.route('/')
def show_data():
    # Use a simple template to display the data
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
        <body style="background-color:powderblue;">
        <style>
        h1 {text-align: center;}
        </style>
            <title>Stocker Blog</title>
        </head>
        <body>
            <h1>Stocker Blog</h1>
            <p>{{ data }}</p>
        </body>
        </html>
    ''', data=last_received_data)

if __name__ == '__main__':
    app.run(debug=True)
