import praw
import prawcore
from flask import Flask, render_template, request, redirect, url_for
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


reddit = praw.Reddit(
    client_id="MK-kRHDda1DsI5D46uu9Yg",
    client_secret="sl1UPKbyeXJbES85MQein9tDvyLFmg",
    password="ramennoodles5501",
    username="no_info23",
    user_agent="/u/no_info23/useragent_1",
)


def get_subreddits(keyword: str):
    keyword = keyword.replace(" ", "")
    url = F"https://www.reddit.com/subreddits/search?q={keyword}"
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome()
    driver.get(url)

    try:
        fetched_subs = driver.find_elements(By.CLASS_NAME, "titlerow")
    except selenium.common.exceptions.NoSuchElementException:
        pass
    
    subr_list = [(elem.text).split(" ")[0].split("/")[1][:-1] for elem in fetched_subs]

    return subr_list[0:5]


def get_posts(subreddits, timeframe):

    all_submissions = []

    for subr in subreddits:
        subreddit = reddit.subreddit(subr)
        
        # loop through the top 5 submissions in the last month
        try:
            for submission in subreddit.top(time_filter=timeframe, limit=10):
                current_submission = [submission.title, int(submission.score), submission.url]
                all_submissions.append(current_submission)

        except (prawcore.exceptions.NotFound, prawcore.exceptions.Forbidden, prawcore.exceptions.Redirect):
            pass

    return all_submissions


def sort_posts(submissions):
    n = len(submissions)

    if n > 0:

        for i in range(n - 1):

            for j in range(0, n - i - 1):
                if submissions[j][1] < submissions[j+1][1]:
                    submissions[j][1], submissions[j+1][1] = submissions[j+1][1], submissions[j][1]

        return submissions[0: 10]

    else:
        return None


def start(keyword, timeframe):
    subreddits = get_subreddits(keyword)
    posts = get_posts(subreddits, timeframe)
    top_posts = sort_posts(posts)
    return top_posts


app = Flask(__name__)


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        subreddit_name = request.form.get("subreddit_name")
        timeframe = request.form.get("timeframe")
        
        if timeframe == None:
            timeframe = "month"

        ranked_posts = start(subreddit_name, timeframe)

        return render_template("index.html", ranked_posts=ranked_posts, keyword=subreddit_name, chosen_timeframe=timeframe)
    
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
