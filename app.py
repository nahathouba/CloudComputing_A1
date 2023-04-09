from flask import Flask, render_template, request, url_for, flash, redirect, session
from dynamoUtils import tableExists, createLogInTable, createMusicTable, createUser, userExists, verifyUser, getUserName
from s3Utils import downloadArtistImage, uploadArtistImageS3, createArtistImageBucket, bucketExists, isImagesUploaded
from subscriptionUtils import createMusicSubscriptionTable, getMusicSubscriptions, removeMusicSubscriptionS3, addMusicSubscriptionS3
from musicUtils import searchMusic
from forms import RegisterForm, LoginForm, MusicSearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8693f210b860a5ab14b3269295d1d203'


isLoginTableExist = tableExists('login')
if not isLoginTableExist:
    # Create the login table and load the users if not exist
    createLogInTable()

isMusicTableExist = tableExists('music')
if not isMusicTableExist:
    # Create the music table and load the music if not exist
    createMusicTable()

# Create the artist image S3 bucket
if not bucketExists():
    createArtistImageBucket()
    # Download the artist images from the URL
    downloadArtistImage()
    # Upload the artist images to the S3 bucket
    uploadArtistImageS3()

isSubscriptionTableExist = tableExists('user-music-subscriptions')
if not isSubscriptionTableExist:
    # Create the user music subscribtion table if not exist
    createMusicSubscriptionTable()

# Check still no the images are uploaded to the S3 bucket
if not isImagesUploaded():
    # Download the artist images from the URL
    downloadArtistImage()
    # Upload the artist images to the S3 bucket
    uploadArtistImageS3()


@ app.route('/')
def index():
    return redirect(url_for('home'))


@ app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    subscriptions = getMusicSubscriptions(session['email'])
    returnMusic = []

    form = MusicSearchForm()
    if form.validate_on_submit():
        returnMusic = searchMusic(
            form.title.data, form.year.data, form.artist.data
        )
        if returnMusic != []:
            return render_template('home.html', title='Home', username=session['username'], subscriptions=subscriptions, musics=returnMusic, form=form)
        else:
            flash(f'No result is retrieved!', 'danger')

    return render_template('home.html', title='Home', username=session['username'], subscriptions=subscriptions, musics=returnMusic, form=form)


@ app.route('/register', methods=['GET', 'POST'])
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


@ app.route('/login', methods=['GET', 'POST'])
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
    app.run(debug=False)
