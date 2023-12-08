from flask import Flask, render_template, request, redirect, url_for, session
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask_socketio import SocketIO


app = Flask(__name__)
app.secret_key = 'mdmoinuddinmansoori'
socketio = SocketIO(app)


# Dummy database (replace with an actual database in a real project)
users = [{'username': 'user1', 'password': 'password1'}, {'username': 'user2', 'password': 'password2'}]

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
        return redirect(url_for('dashboard_page'))

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/signupsucc', methods=['POST'])
def signupsucc():
    return render_template('login.html')

@app.route('/upload_page')
def index():
    profile_picture = request.args.get('profile_picture', 'default-profile.jpg')
    return render_template('upload.html', profile_picture=profile_picture)
    # return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        data = pd.read_excel(uploaded_file, header=0)
        cleaned_data = data.drop_duplicates()
        session['cleaned_data'] = cleaned_data.to_html(classes='data')
        profile_picture = request.args.get('profile_picture', 'default-profile.jpg')
        return render_template('display.html', tables=[data.to_html(classes='data')], titles=['Data'], profile_picture=profile_picture)
    return render_template('index.html', error='Please upload a file.')

@app.route('/chart_options')
def chart_options():
    if 'cleaned_data' not in session:
        return redirect(url_for('index'))

    return render_template('display.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    if 'cleaned_data' not in session:
        return redirect(url_for('index'))

    chart_type = request.form.get('chart_type')
    x_axis = request.form.get('x_axis')
    y_axis = request.form.get('y_axis')

    cleaned_data = pd.read_html(session['cleaned_data'], index_col=0)[0]
    
    plt.clf()

    if chart_type == 'pie':
        plt.pie(cleaned_data[y_axis], labels=cleaned_data[x_axis], autopct='%1.1f%%')
        plt.title('Pie Chart')

    elif chart_type == 'bar':
        plt.bar(cleaned_data[x_axis], cleaned_data[y_axis])
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Bar Graph')

    elif chart_type == 'line':
        plt.plot(cleaned_data[x_axis], cleaned_data[y_axis], marker='o')
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Line Chart')

    elif chart_type == 'bubble':
        # For simplicity, bubble chart is represented as a scatter plot with marker size based on a third column
        size_column = request.form.get('size_column')
        plt.scatter(cleaned_data[x_axis], cleaned_data[y_axis], s=cleaned_data[size_column])
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Bubble Chart')

    elif chart_type == 'scatter':
        plt.scatter(cleaned_data[x_axis], cleaned_data[y_axis], marker='o' )
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Scatter Plot')

    elif chart_type == 'stacked_bar':
        # For simplicity, stacked bar chart is represented as a regular bar chart
        plt.bar(cleaned_data[x_axis], cleaned_data[y_axis], bottom=cleaned_data[y_axis])
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Stacked Bar Chart')

    else:
        return render_template('display.html', error='Invalid chart type selected')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    # Save the generated chart to user's chart history
    chart_entry = {
        'title': f'{chart_type.capitalize()} Chart',
        'type': chart_type,
        'x_axis': x_axis,
        'y_axis': y_axis,
        'plot_url': plot_url
    }

    if 'chart_history' not in session:
        session['history'] = []

    session['history'].append(chart_entry)
    profile_image = session.get('profile_image')
    return render_template('generated_chart.html', plot_url=plot_url, profile_image=profile_image)

@app.route('/history_page')
def chart_history():
    if 'history' not in session:
        session['history'] = []
        
    profile_picture = request.args.get('profile_picture', 'default-profile.jpg')
    return render_template('history.html', profile_picture=profile_picture, chart_history=session['history'])

    # return render_template('history.html')


@app.route('/dashboard_page')
def dashboard_page():
    # Retrieve the profile image URL from the session
    profile_image = session.get('profile_image')
    return render_template('dashboard.html', profile_image=profile_image)


@app.route('/feedback_page')
def feedback_page():
    profile_picture = request.args.get('profile_picture', 'default-profile.jpg')
    return render_template('feedback.html', profile_picture=profile_picture)
    # return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback = request.form['feedback']

    # Add code to handle feedback (e.g., store in a database)

    return "Thank you for your feedback!"

@app.route('/explore_page')
def explore_page():
    return render_template('explore.html')


@app.route('/logout_page')
def logout_page():
    profile_picture = request.args.get('profile_picture', 'default-profile.jpg')
    return render_template('logout.html', profile_picture=profile_picture)
    # return render_template('logout.html')

@app.route('/setting_page')
def setting_page():
    profile_picture = request.args.get('profile_picture', 'default-profile.jpg')
    return render_template('setting.html', profile_picture=profile_picture)
    # return render_template('setting.html')


@app.route('/voice_command')
def voice_command():
    profile_picture = request.args.get('profile_picture', 'default-profile.jpg')
    return render_template('voice.html', profile_picture=profile_picture)
    # return render_template('voice.html')

@app.route('/upload_profile', methods=['POST'])
def upload_profile():
    print("oppp")
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file.filename != '':
            # Save the uploaded profile picture to a permanent location
            file_path = os.path.join('static', 'profile_pictures', file.filename)
            file.save(file_path)

            # Set the profile image URL in the session
            session['profile_image'] = file.filename
            return redirect(url_for('dashboard_page'))

    # Redirect back to the dashboard_page if no file is provided or there is an issue
    return redirect(url_for('dashboard_page'))

if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()

    # Start the Flask-SocketIO application
    socketio.run(app,host='0.0.0.0', port=5000, debug=True)

 