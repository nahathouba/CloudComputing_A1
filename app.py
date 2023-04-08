from flask import Flask, render_template, request, url_for, flash, redirect, session
from utils import tableExists, createLogInTable, createMusicTable, createUser, userExists, verifyUser, getUserName
from s3Utils import downloadArtistImage, uploadArtistImageS3, createArtistImageBucket, bucketExists
from subscriptionUtils import createMusicSubscriptionTable, getMusicSubscriptions, removeMusicSubscriptionS3
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8693f210b860a5ab14b3269295d1d203'


# isTableExist = tableExists('login')
# if not isTableExist:
# Create the login table and load the users
# createLogInTable()

# isTableExist = tableExists('music')
# if not isTableExist:
# Create the music table and load the music
# createMusicTable()

# Create the artist image S3 bucket
if not bucketExists():
    createArtistImageBucket()
# Download the artist images from the URL
# downloadArtistImage()
# Upload the artist images to the S3 bucket
# uploadArtistImageS3()

# createMusicSubscriptionTable()


@ app.route('/')
def index():
    return render_template("index.html")


@ app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    subscriptions = getMusicSubscriptions(session['email'])

    return render_template('home.html', title='Home', username=session['username'], subscriptions=subscriptions)


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


if __name__ == "__main__":
    app.run(debug=True)
