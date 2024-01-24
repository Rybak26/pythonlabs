from flask import Flask, render_template, request
import platform
import datetime

app = Flask(__name__)


class Portfolio:
    def __init__(self):
        self.page_title = None
        self.os_info = self.get_os_info()
        self.user_agent = request.headers.get('User-Agent')
        self.current_time = self.get_current_time()

    def get_os_info(self):
        return str(platform.system() + " " + platform.release() + " " + platform.version())

    def get_current_time(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")


@app.route('/')
def home():
    portfolio = Portfolio()
    portfolio.page_title = "Основна сторінка"
    return render_template('page1.html', portfolio=portfolio)


@app.route('/page1')
def page1():
    portfolio = Portfolio()
    portfolio.page_title = "Основна сторінка"
    return render_template('page1.html', portfolio=portfolio)


@app.route('/page2')
def page2():
    portfolio = Portfolio()
    portfolio.page_title = "Про мене"
    return render_template('page2.html', portfolio=portfolio)


@app.route('/page3')
def page3():
    portfolio = Portfolio()
    portfolio.page_title = "Контакти"
    return render_template('page3.html', portfolio=portfolio)


my_skills = ["Java","Python" , "JavaScript" , "SQL"]


@app.route('/skills')
@app.route('/skills/<int:id>')
def display_skills(id=None):
    portfolio = Portfolio()
    if id is None:
        return render_template('page2.html', portfolio=portfolio, skills=my_skills, total=len(my_skills))
    elif 0 <= id < len(my_skills):
        return render_template('page2.html', portfolio=portfolio, skills=[my_skills[id]])
    else:
        return "Skill not found"


if __name__ == '__main__':
    app.run()
