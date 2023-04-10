from flask import Flask, render_template, url_for, flash, redirect, session
from dynamoUtils import createUser, userExists, verifyUser, getUserName
from subscriptionUtils import getMusicSubscriptions, removeMusicSubscriptionS3, addMusicSubscriptionS3
from forms import RegisterForm, LoginForm, MusicSearchForm
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8693f210b860a5ab14b3269295d1d203'


@app.route('/')
def index():
    response1 = requests.get(
        'https://44lyi97043.execute-api.us-east-1.amazonaws.com/default/createLoginTable', timeout=30)  # Lambda function API Gateway address to create the login table
    print(response1)

    response2 = requests.get(
        'https://44lyi97043.execute-api.us-east-1.amazonaws.com/default/createMusicTable', timeout=30)  # Lambda function API Gateway address to create the music table
    print(response2)

    response3 = requests.get(
        'https://44lyi97043.execute-api.us-east-1.amazonaws.com/default/createBucket', timeout=60)  # Lambda function API Gateway address to create s3 bucket and download the artists images and upload them to the s3 bucket
    print(response3)

    return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    subscriptions = getMusicSubscriptions(session['email'])
    returnMusic = []
    res = None

    form = MusicSearchForm()
    if form.validate_on_submit():
        # Lambda function API Gateway address to search for music
        url = 'https://44lyi97043.execute-api.us-east-1.amazonaws.com/default/searchMusic?'

        if form.title.data or form.artist.data or form.year.data:
            params = {}
            if form.title.data:
                params['title'] = form.title.data
            if form.artist.data:
                params['artist'] = form.artist.data
            if form.year.data:
                params['year'] = form.year.data
            res = requests.get(url, params=params)

    if res.status_code == 200:
        returnMusic = res.json()
        return render_template('home.html', title='Home', username=session['username'], subscriptions=subscriptions, musics=returnMusic, form=form)
    else:
        flash(f'No result is retrieved!', 'danger')

    return render_template('home.html', title='Home', username=session['username'], subscriptions=subscriptions, musics=returnMusic, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        userRigestered = userExists(form.email.data)
        if not userRigestered:
            newUser = {
                "email": form.email.data,
                "username": form.username.data,
                "password": form.password.data
            }
            createUser(newUser)
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'The email {form.email.data} already exists!', 'danger')

    return render_template("register.html", form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if verifyUser(form.email.data, form.password.data):
            session['username'] = getUserName(form.email.data)
            session['email'] = form.email.data
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful! Email or Password is invalid.', 'danger')
    return render_template("login.html", form=form, title='Login')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/removeMusicSubscription/<string:musicTitle>', methods=['GET'])
def removeMusicSubscription(musicTitle):
    removed = removeMusicSubscriptionS3(session['email'], musicTitle)
    if removed:
        flash(f'Subscription removed for {musicTitle}!', 'success')
        return redirect(url_for('home'))
    else:
        flash(f'Error removing subscription for {musicTitle}!', 'danger')
        return redirect(url_for('home'))


@app.route('/addMusicSubscription/<string:musicTitle>', methods=['GET'])
def addMusicSubscription(musicTitle):
    added = addMusicSubscriptionS3(session['email'], musicTitle)
    if added:
        flash(f'Subscription added for {musicTitle}!', 'success')
        return redirect(url_for('home'))
    else:
        flash(f'Error adding subscription for {musicTitle}!', 'danger')
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
