from difflib import SequenceMatcher
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Card:

    def __init__(self, question: str, answer: str | int):
        self.priorities = [1, 2, 7, 14, 30, 90, 180]
        self.__reset(question, answer)

    def __reset(self, question, answer):
        self.question = question
        self.answer = answer
        self.priority = self.priorities[0]
        self.recent_answers = []
        self.due_date = datetime.now()

    def __compare(self, answer, prediction):
        return SequenceMatcher(None, answer, prediction).ratio()

    def __score(self, criteria, score):
        return True if score >= criteria else False
    
    def __progess(self, success):
        if success:
            # if answered successfully then send card to next box.
            current_rate = self.priority
            next_rate_idx = self.priorities.index(current_rate) + 1
            self.priority = self.priorities[next_rate_idx] if next_rate_idx < len(self.priorities) else self.priorities[-1]
            # add timedelta to curr time.
            self.due_date = datetime.now() + relativedelta(days=self.priority)
        else:
            # if incorrect, reset to daily question.
            self.priority = self.priorities[0]
            self.due_date = datetime.now() + relativedelta(days=self.priority)
    
    def attempt(self, prediction):
        # compute score and compare to criteria 
        score = self.__compare(self.answer, prediction)
        success = self.__score(0.75, score)
        self.__progess(success)
        # store recent answers
        self.recent_answers.append({
            "prediction" : prediction,
            "success" : success,
            "datetime" : datetime.now(),
        })

    def __repr__(self):
        print(f"{'Question: ':<17}{self.question}")
        print(f"{'Answer: ':<17}{self.answer}")
        print(self.priority)

    def render(self, input=True):
        html = f"""
        <div style="background-color: #f8f9fa; border-radius: 10px; box-shadow: 0px 0px 10px #ccc; padding: 20px; font-family: Arial;">
            <h4 style="color: #343a40; font-size: 24px; font-weight: bold; margin-top: 0px;">{self.question}</h4>
            <p style="margin-bottom: 5px;"><strong>Answer:</strong></p>
            <div id="answer-container" style="display:none;">
                <p style="color: #343a40; font-size: 20px;">{self.answer}</p>
            </div>
            <div id="input-container" style="margin-top: 10px;">
                <input id="answer-input" type="text" placeholder={"Enter your answer here" if input else self.answer} style="padding: 5px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px; width: 100%;">
                <button id="submit-button" type="button" class="btn btn-primary" style="display:{"block" if input else "none"}; background-color: #333; color: #fff; border: none; outline: none; border-radius: 5px; font-size: 16px; padding: 10px 20px; margin-top: 10px; cursor: pointer; transition: all 0.3s;">Submit</button>
            </div>
            <p style="margin-top: 15px; margin-bottom: 5px;"><strong>Due Date:</strong> {self.due_date.date()}</p>
        </div>
        """
        script = f"""
        <script>
            var answerContainer = document.getElementById('answer-container');
            var inputContainer = document.getElementById('input-container');
            var answerInput = document.getElementById('answer-input');
            var submitButton = document.getElementById('submit-button');
            submitButton.addEventListener('click', function() {{
                if (answerInput.value.trim().toLowerCase() === '{self.answer.strip().lower()}') {{
                    inputContainer.style.display = 'none';
                    answerContainer.style.display = 'block';
                }} else {{
                    alert('Incorrect answer.');
                    inputContainer.style.display = 'none';
                    answerContainer.style.display = 'block';
                }}
            }});
        </script>
        """
        return html + script
