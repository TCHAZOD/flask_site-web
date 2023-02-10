import sqlite3
from flask import Flask, redirect, url_for ,render_template, request, session#, check_user
#app= Flask(__name__, template_folder = 'template')
#app= Flask(__name__, template_folder = '../template')

def register_user_to_db(username, passeword):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('INSERT INTO users (username, passeword) values (?, ?)',(username, passeword))
    con.commit()
    con.close()
    
def check_user(username, passeword):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT username, passeword from users where username=? and passeword=?',(username, passeword))
    
    result = cur.fetchone()
    if result:
        return True
    else:
        return False
    
app = Flask(__name__)
app.secret_key = "sana"
    
@app.route('/')
def index():
    return render_template("login.html")

@app.route('/register',methods=["POST","GET"])
def register():
        if request.method == 'POST':
            username = request.form['username']
            passeword = request.form['passeword']
            #email = request.form['email']
            
            
            register_user_to_db(username, passeword)
            return redirect(url_for('index'))
        else:
            return render_template('register.html')  
            
@app.route('/login', methods=['POST','GET']) 
def login():
    if request.method == 'POST':
        username = request.form['username']
        passeword = request.form['passeword']
        print(check_user(username, passeword))
        if check_user(username, passeword):
            session['username'] = username
            
        return redirect(url_for('home'))
    else:
        redirect(url_for('index')) 
        
            
         
        
        
@app.route('/home', methods=['POST',"GET"])
def home():
        if ('username') in session:
            return render_template('home.html', username=session['username'])
        else:
            return "Username or Password is wrong!"      

@app.route('/logout')
def logout():
        session.clear()
        return redirect(url_for('index'))
            

if __name__ == '__main__':
    app.run(debug=True)
    


