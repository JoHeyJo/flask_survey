from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def start_page():
    """render a page that shows the user the title of the survey, the instructions, and a button to start the survey."""

    title = survey.title
    instructions = survey.instructions

    return render_template("survey_start.html",
                           title=title,
                           instructions=instructions)


@app.post("/begin")
def show_first_question():
    """ Generate each question page with choices """

    session["responses"] = []

    return redirect("question/0")


@app.get("/question/<int:q_id>")
def show_questions(q_id):

    question = survey.questions[q_id]
    

    return render_template("question.html", question=question)


@app.post("/answer")
def show_next_question():

    choice = request.form.get("answer")
    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses
    # breakpoint()

    if len(responses) == len(survey.questions):
        return redirect("/completion")

    return redirect(f"/question/{len(responses)}")

@app.get("/completion")
def show_completion():

  return render_template("completion.html")
