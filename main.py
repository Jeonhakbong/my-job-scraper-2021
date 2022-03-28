import os
from flask import Flask, render_template, request, redirect, send_file
from jobkor import job_search
from exporter import save_to_file

os.system("clear")

app = Flask("My Job Scrapper")
myDB = {}

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/report')
def report():
  word = request.args.get("word")
  if word:
    word = word.lower()
    existingJobs = myDB.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = job_search(word)
      myDB[word] = jobs
  else:
    return redirect("/")
  return render_template("report.html",
    searchingBy=word,
    resultNumber=len(jobs),
    jobs=jobs)

@app.route('/export')
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = myDB.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file('jobs.csv')
  except:
    return redirect('/')
    
app.run(host='0.0.0.0')
