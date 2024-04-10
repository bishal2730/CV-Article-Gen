from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt
from flask import render_template
import gspread
from datetime import datetime
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import json
import http.client
import os.path
from google.oauth2.service_account import Credentials
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registercvlogintest314159', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    return render_template('dashboard.html', user=user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/mathjr')
def mathjr():
    return render_template('mathjr.html')

# Route for danson.html


@app.route('/danson')
def danson():
    return render_template('danson.html')

# Route for siam.html


@app.route('/siam')
def siam():
    return render_template('siam.html')

# Route for chim.html


@app.route('/chim')
def chim():
    user = current_user  # Get the current logged-in user
    print("Current user name:", user.name)
    return render_template('chim.html')


def article_json(topic, key_word, language):
    model = ChatOpenAI(
        model="gpt-3.5-turbo-1106",
        openai_api_key='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',
        temperature=0,
        max_tokens=4095
    )

    prompt_template = """Role: Act as a content writer. You are about to write an article for an edtech site.
        Task: Generate an article for the requested topic. Generate the output as shown in the example below:

        Example :

        Input Query : Generate me an article for "GCF"

        Output:
        --
        "title": "Your Post Title",
        "content": " ",
        "acf": --
            "faq_quesion_1": "What is the importance of finding the Greatest Common Factor (GCF)?",
            "faq_answer_1": "Finding the Greatest Common Factor (GCF) is crucial as it helps simplify fractions and solve various mathematical problems efficiently.",
            "faq_quesion_2": "How does the GCF concept relate to factors?",
            "faq_answer_2": "The GCF is closely related to the concept of factors, as it represents the largest number that divides two or more numbers without leaving a remainder.",
            "faq_quesion_3": "Can the GCF be utilized to simplify fractions?",
            "faq_answer_3": "Yes, the GCF is instrumental in simplifying fractions by dividing both the numerator and denominator by their greatest common factor.",
            "faq_quesion_4": "What methods are available to determine the GCF of numbers?",
            "faq_answer_4": "Several methods exist to find the GCF, including prime factorization, listing factors, and using the Euclidean algorithm.",
            "faq_quesion_5": "How is the concept of GCF applied in real-life situations?",
            "faq_answer_5": "The concept of GCF finds practical applications in various real-life scenarios such as simplifying recipes, dividing resources equally, and optimizing resource allocation in business operations.",
            "articles_description": "<h3>What is GCF?:</h3> In the realm of mathematics, particularly when dealing with numbers and their relationships, the term Greatest Common Factor or GCF frequently arises. But what exactly does it entail? Let's embark on a journey into the realm of GCF and uncover its significance in solving mathematical quandaries.",
            "analogy_of_defination": "<h3>The GCF Explained:</h3> The Greatest Common Factor (GCF) of two or more numbers is the largest number that divides each of the given numbers without leaving a remainder. In simpler terms, it is the greatest number that is a factor of all the given numbers.",
            "articles_methods": "<h3>Finding the GCF: </h3>  There are several methods to determine the GCF of numbers. One approach involves listing the factors of each number and identifying the greatest common factor. Another method entails using prime factorization to find the GCF efficiently.",
            "examples": "<h3>Finding the GCF of 24 and 36:</h3> <strong> Step 1: </strong> List the factors of each number<br>Factors of 24: 1, 2, 3, 4, 6, 8, 12, 24<br>Factors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36<br><strong> Step 2: </strong> Identify the greatest common factor<br>The greatest common factor of 24 and 36 is 12.<br>Thus, the GCF of 24 and 36 is 12.",
            "example": "<strong> Summary::</strong> <br> This example demonstrates the method of finding the Greatest Common Factor (GCF) of two numbers, 24 and 36. Initially, the factors of each number are listed, followed by identifying the greatest common factor among them. By determining that the largest number shared by both sets of factors is 12, it is concluded that the GCF of 24 and 36 is 12. This process illustrates how the GCF is utilized to identify the largest divisor common to both numbers, facilitating calculations and problem-solving in various mathematical contexts. ",
            "article_tips_and_tricks": "<strong>1. Prime Factorization:</strong><br> <strong>Scenario:</strong> Finding the GCF of 18 and 24.<br> <strong>Tip: </strong>To find the GCF, list the factors of each number and identify the greatest common factor.<br> Calculation: Factors of 18: 1, 2, 3, 6, 9, 18 <br> Factors of 24: 1, 2, 3, 4, 6, 8, 12, 24 <br> Greatest common factor: 6<br> Answer: A) 6 cookies. <br><strong>2. The Garden Plot Puzzle</strong><br><strong>Scenario:</strong> Finding the GCF of 30 and 42.<br><strong>Tip: </strong>List the factors of each number and identify the greatest common factor to find the GCF.<br>Calculation: Factors of 30: 1, 2, 3, 5, 6, 10, 15, 30<br>Factors of 42: 1, 2, 3, 6, 7, 14, 21, 42<br>Greatest common factor: 6<br>Answer: B) 14 meters.<br><strong>3. The Classroom Bookshelf Challenge</strong><br><strong>Scenario:</strong> Finding the GCF of 36 and 48.<br><strong>Tip:</strong> Utilize the method of listing factors to find the GCF of the given numbers.<br>Calculation: Factors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36<br>Factors of 48: 1, 2, 3, 4, 6, 8, 12, 16, 24, 48<br>Greatest common factor: 12<br>Answer: C) 24 books.",
            "application": "<strong>Real-Life Applications of GCF:</strong>,<br> <strong>Story: The GCF Expedition of Emma and Noah</strong><br>Emma and Noah, two adventurous friends, embarked on a journey filled with puzzles and challenges that required the application of GCF to overcome obstacles and achieve success.<br> <strong>Challenge 1: The Puzzle Maze</strong><br> Emma and Noah found themselves in a perplexing maze filled with enigmatic symbols. To unlock the next passage, they needed to decipher the greatest common factor of two numbers written on a plaque. The numbers were 16 and 24. Recognizing the significance of GCF, they quickly determined that the greatest common factor was 8, allowing them to proceed through the maze.<br>  <strong>Challenge 2: The Cryptic Cipher</strong> <br> Continuing their expedition, Emma and Noah stumbled upon an ancient cryptic cipher inscribed on a stone tablet. To decipher the message, they had to compute the GCF of two mysterious numbers engraved beneath the inscription. The numbers revealed were 42 and 56. Applying their knowledge of GCF, they deduced that the greatest common factor was 14, unlocking the hidden message and unraveling the mystery. <br>  <strong>Challenge 3: The Guardian's Riddle</strong> <br>In their final challenge, Emma and Noah encountered a wise guardian guarding a hidden treasure. The guardian presented them with a riddle that involved determining the GCF of three numbers carved on a stone pedestal. The numbers were 36, 54, and 72. Drawing upon their understanding of GCF, Emma and Noah calculated that the greatest common factor was 18, earning them the guardian's approval and access to the treasure.",
            "quiz": "<strong>Quiz 1: </strong><br> What is the significance of finding the Greatest Common Factor (GCF)?,<br> <strong>Quiz 2: </strong><br>  How does the GCF concept relate to factors?,<br> <strong>Quiz 3: </strong><br> Can the GCF be utilized to simplify fractions?,<br> <strong>Quiz 4: </strong><br> What methods are available to determine the GCF of numbers?,<br> <strong>Quiz 5: </strong><br> How is the concept of GCF applied in real-life situations?"
            ``
        ``

        Instruction:

        1. Always generate output on JSON format.
        2. Never use single quote in the question.
        3. Always remember that its faq_quesion not faq_question
        4. Remember don't put anything inside the content part let it be emty as it is
        5, Don't put : in the between  "Your Post Title"
        6. Always put the h3 tag between each sub heading and strong tag between each context . For eg: "<h3>sub heading</h3>, <strong>context</strong>.
        7. , 5 Tips and Tricks, 5 Quizzes, 5 Real-Life Applications and 5 FAQs.
        8. Also generate "example" which is a small Summary of the "examples"
        9. Generae that explain in more words
        10. Always generate 3 examples

    {context}

    """
    prompt = PromptTemplate(
        input_variables=["context"],
        template=prompt_template,
    )

    chain = LLMChain(llm=model, prompt=prompt)

    query = f'''Generate me an article for "{topic}" in language "{language}". Compulsorily use these keywords in the article: "{key_word}".'''
    content = chain.invoke({'context': query})

    # Print content for debugging
    print("Generated Content:", content)

    # Check if content is in expected format
    if 'text' not in content:
        print("Error: 'text' key not found in content.")
        return None
    output = content['text'].replace('--', '{')
    output = output.replace('``', '}')
    # Print output for debugging
    print("Output:", output)

    # Try to decode JSON
    try:
        article = json.loads(output)
        print("Article JSON:", article)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None

    return article


scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(
    "credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Route to handle form submission for mathForm


@app.route('/submit_ChimvineForm', methods=['POST'])
def submit_Chimvine_form():
    google_sheet_ip = request.form['ChimvineForm-name']
    print("Google Sheet IP from Chimvine:", google_sheet_ip)
    # Get the current user's username
    user = current_user  # Get the current logged-in user
    print("Current user name:", user.name)
    if user:
        first_name = user.name

    else:
        first_name = ''

    print("Logged-in User's First Name:", first_name)

    # Handle the data from mathForm

    sheet_id = google_sheet_ip
    workbook = client.open_by_key(sheet_id)

    # Access the first sheet of the workbook
    sheet = workbook.sheet1

    created_contents = []
    failed_contents = []

    # Retrieve all values from the sheet along with row numbers
    all_rows_with_row_numbers = list(
        enumerate(sheet.get_all_records(), start=2))  # Start from row 2

    # Iterate through each row in the sheet along with row numbers
    for row_number, row_data in all_rows_with_row_numbers:
        article_title = row_data.get("article_title", "")
        seo_keywords = row_data.get("seo_keywords", "")
        language = row_data.get("language", "")
        status = row_data.get("Status", "")
        Date = row_data.get("Date", "")
        Time = row_data.get("Time", "")
        User = row_data.get("User", "")

        print(
            f"Article Title: {article_title}, SEO Keywords: {seo_keywords}, Language: {language}, Status: {status}, Date: {Date}, Time: {Time}")

        # Generate content for the article
        content = article_json(article_title, seo_keywords, language)
        print(content)
        if content:
            print(f"Posted to WordPress: {article_title}")
            created_contents.append(article_title)
            # Prepare the payload
            payload = json.dumps(content)
            print(payload)

            # Send the POST request to create the new article
            conn = http.client.HTTPSConnection("site.chimpvine.com")
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic bmlyYWphbmFkbWluOmRRRVogU3VqWSBPYjFtIHRLVFcgR2JxRCBaeFd1'
            }
            conn.request("POST", "/wp-json/wp/v2/article", payload, headers)
            res = conn.getresponse()
            print(res)
            data = res.read()
            # Update status in Google Sheet
            if res.status == 201:
                date = datetime.now().strftime("%Y-%m-%d")
                time = datetime.now().strftime("%H:%M:%S")
                User_Name = f"{first_name} "
                sheet.update_cell(row_number, sheet.find(
                    "Status").col, "Posted successfully!")
                sheet.update_cell(row_number, sheet.find("Date").col, date)
                sheet.update_cell(row_number, sheet.find("Time").col, time)
                sheet.update_cell(
                    row_number, sheet.find("User").col, User_Name)
            else:
                sheet.update_cell(row_number, sheet.find(
                    "Status").col, "Post Failed!")
                sheet.update_cell(row_number, sheet.find("Date").col, date)
                sheet.update_cell(row_number, sheet.find("Time").col, time)
                failed_contents.append(article_title)
                print(data.decode("utf-8"))
        else:
            print(f"Failed to generate content for: {article_title}")
            # Update status in Google Sheet
            sheet.update_cell(
                row_number, sheet.find("Status").col, "Content Generation Failed!")
            failed_contents.append(article_title)

    else:
        print("No data found in the spreadsheet.")

    return render_template('chim.html', created_contents=created_contents, failed_contents=failed_contents)


# For Siam

@app.route('/submit_SiamForm', methods=['POST'])
def submit_Siam_form():
    google_sheet_ip = request.form['SiamForm-name']
    print("Google Sheet IP from SiamForm:", google_sheet_ip)
    # Get the current user's username
    user = current_user  # Get the current logged-in user
    print("Current user name:", user.name)
    if user:
        first_name = user.name

    else:
        first_name = ''

    print("Logged-in User's First Name:", first_name)

    # Handle the data from mathForm

    sheet_id = google_sheet_ip
    workbook = client.open_by_key(sheet_id)

    # Access the first sheet of the workbook
    sheet = workbook.sheet1

    created_contents = []
    failed_contents = []

    # Retrieve all values from the sheet along with row numbers
    all_rows_with_row_numbers = list(
        enumerate(sheet.get_all_records(), start=2))  # Start from row 2

    # Iterate through each row in the sheet along with row numbers
    for row_number, row_data in all_rows_with_row_numbers:
        article_title = row_data.get("article_title", "")
        seo_keywords = row_data.get("seo_keywords", "")
        language = row_data.get("language", "")
        status = row_data.get("Status", "")
        Date = row_data.get("Date", "")
        Time = row_data.get("Time", "")
        User = row_data.get("User", "")

        print(
            f"Article Title: {article_title}, SEO Keywords: {seo_keywords}, Language: {language}, Status: {status}, Date: {Date}, Time: {Time}")

        # Generate content for the article
        content = article_json(article_title, seo_keywords, language)
        print(content)
        if content:
            print(f"Posted to WordPress: {article_title}")
            created_contents.append(article_title)
            # Prepare the payload
            payload = json.dumps(content)
            print(payload)

            # Send the POST request to create the new article
            conn = http.client.HTTPSConnection("chimpvinesiam.com")
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic bmlyYWphbmFkbWluOjdZWDYgNmJRQSBIazNHIGxxSUkgYzRYTiBhRkJl'
            }
            conn.request("POST", "/wp-json/wp/v2/article", payload, headers)
            res = conn.getresponse()
            print(res)
            data = res.read()
            # Update status in Google Sheet
            if res.status == 201:
                date = datetime.now().strftime("%Y-%m-%d")
                time = datetime.now().strftime("%H:%M:%S")
                User_Name = f"{first_name} "
                sheet.update_cell(row_number, sheet.find(
                    "Status").col, "Posted successfully!")
                sheet.update_cell(row_number, sheet.find("Date").col, date)
                sheet.update_cell(row_number, sheet.find("Time").col, time)
                sheet.update_cell(
                    row_number, sheet.find("User").col, User_Name)
            else:
                sheet.update_cell(row_number, sheet.find(
                    "Status").col, "Post Failed!")
                sheet.update_cell(row_number, sheet.find("Date").col, date)
                sheet.update_cell(row_number, sheet.find("Time").col, time)
                failed_contents.append(article_title)
                print(data.decode("utf-8"))
        else:
            print(f"Failed to generate content for: {article_title}")
            # Update status in Google Sheet
            sheet.update_cell(
                row_number, sheet.find("Status").col, "Content Generation Failed!")
            failed_contents.append(article_title)

    else:
        print("No data found in the spreadsheet.")

    return render_template('siam.html', created_contents=created_contents, failed_contents=failed_contents)


# For Dansonsolution and Math Trciks Jr

def article_generator(topic, key_word, language):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key='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',
        temperature=0,
        max_tokens=4095
    )

    prompt_template = """Role: Act as a content writer. You are about to write an article for an edtech site.
        Task: Generate an article for the requested topic. Generate the output as shown in the example below:

        Example :

        Input Query : Generate me an article for "Least Common Multiple"

        OUTPUT:

        <h2>Introduction</h2>

        <h4>What is LCM?:</h4>
        When dealing with numbers, especially in mathematics, you often come across the term "Least Common Multiple" or LCM. But what exactly does it mean? Let's dive into the world of LCM and understand its significance in solving mathematical problems.

        <h2>Definition</h2>

        <h4>The LCM Explained: </h4>
        The Least Common Multiple (LCM) of two or more numbers is the smallest multiple that is exactly divisible by each of the numbers. In simpler terms, it is the smallest number that is a multiple of all the given numbers.

        <h2>Methods </h2>

        <h4>Finding the LCM: </h34>
        There are various methods to find the LCM of numbers. One common method is to list the multiples of each number and find the smallest multiple that is common to all the numbers. Another method involves using prime factorization to find the LCM.

        <h2>Example</h2>

        <h4>Finding the LCM of 12 and 15:</h4>
        <strong> Step 1: </strong> List the multiples of each number
        Multiples of 12: 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, ...
        Multiples of 15: 15, 30, 45, 60, 75, 90, 105, 120, ...
        <strong> Step 2: </strong> Identify the smallest common multiple
        The smallest common multiple of 12 and 15 is 60.
        So, the LCM of 12 and 15 is 60.

        <h2>Quizzes</h2>

        <strong>1. "The Bakery Dilemma"</strong>
        <strong> Scenario: </strong>
        A bakery needs to pack cookies in boxes of 12 and 15. What is the least number of cookies they can pack in each box to ensure no cookies are left over?
        A) 60 cookies
        B) 30 cookies
        C) 45 cookies
        D) 120 cookies
        Equation: LCM of 12 and 15
        Answer: A) 60 cookies

        <strong>2. "The Garden Planting Puzzle"</strong>
        <strong> Scenario: </strong> A gardener wants to plant flowers in rows of 8 and 10. What is the least number of flowers they need to plant to fill each row without any flowers left over?
        A) 40 flowers
        B) 80 flowers
        C) 20 flowers
        D) 100 flowers
        Equation: LCM of 8 and 10
        Answer: A) 40 flowers

        <strong>3. "The Classroom Seating Arrangement"</strong>
        <strong> Scenario: </strong> A teacher wants to arrange students in rows of 6 and 9. What is the least number of students needed to fill each row without any students left over?
        A) 18 students
        B) 36 students
        C) 12 students
        D) 24 students
        Equation: LCM of 6 and 9
        Answer: A) 18 students

        <strong>4. "The Music Playlist Dilemma"</strong>
        <strong> Scenario: </strong> A DJ wants to create a playlist with songs that repeat every 4 and 6 minutes. What is the least amount of time before the playlist repeats a song?
        A) 12 minutes
        B) 24 minutes
        C) 18 minutes
        D) 36 minutes
        Equation: LCM of 4 and 6
        Answer: A) 12 minutes

        <strong>5. "The Sports Equipment Packing Challenge"</strong>
        <strong>Scenario: </strong>A coach needs to pack sports equipment in bags of 5 and 7. What is the least number of equipment items they can pack in each bag without any items left over?
        A) 35 items
        B) 70 items
        C) 25 items
        D) 50 items
        Equation: LCM of 5 and 7
        Answer: A) 35 items

        <h2>Tips and Tricks</h2>

        <strong>1. The Bakery Dilemma</strong>
        <strong>Scenario:</strong> Finding the LCM of 12 and 15.
        <strong>Tip: </strong>To find the LCM, list the multiples of each number and identify the smallest common multiple.
        Calculation: Multiples of 12: 12, 24, 36, 48, 60, ...
        Multiples of 15: 15, 30, 45, 60, ...
        Smallest common multiple: 60
        Answer: A) 60 cookies.

        <strong>2. The Garden Planting Puzzle</strong>
        <strong>Scenario:</strong> Finding the LCM of 8 and 10.
        <strong>Tip: </strong>List the multiples of each number and identify the smallest common multiple to find the LCM.
        Calculation: Multiples of 8: 8, 16, 24, 32, 40, ...
        Multiples of 10: 10, 20, 30, 40, ...
        Smallest common multiple: 40
        Answer: A) 40 flowers.

        <strong>3. The Classroom Seating Arrangement</strong>
        <strong>Scenario:</strong> Finding the LCM of 6 and 9.
        <strong>Tip:</strong> Use the method of listing multiples to find the LCM of the given numbers.
        Calculation: Multiples of 6: 6, 12, 18, 24, 30, ...
        Multiples of 9: 9, 18, 27, 36, ...
        Smallest common multiple: 18
        Answer: A) 18 students.

        <strong>4. The Music Playlist Dilemma</strong>
        <strong>Scenario:</strong> Finding the LCM of 4 and 6.
        <strong>Tip:</strong> List the multiples of each number and identify the smallest common multiple to find the LCM.
        Calculation: Multiples of 4: 4, 8, 12, 16, 20, ...
        Multiples of 6: 6, 12, 18, 24, ...
        Smallest common multiple: 12
        Answer: A) 12 minutes.

        <strong>5. The Sports Equipment Packing Challenge</strong>
        <strong>Scenario:</strong> Finding the LCM of 5 and 7.
        <strong>Tip:</strong> Use the method of listing multiples to find the LCM of the given numbers.
        Calculation: Multiples of 5: 5, 10, 15, 20, 25, ...
        Multiples of 7: 7, 14, 21, 28, ...
        Smallest common multiple: 35
        Answer: A) 35 items.

        <h2>Real-Life Applications</h2>

        <strong>Story: "The LCM Adventure of Alex and Lily"</strong>
        Alex and Lily were two adventurous siblings who loved solving puzzles and riddles. One day, they encountered a series of challenges that required them to use the concept of LCM to overcome obstacles and complete their quests.

        <strong>Challenge 1: The Treasure Hunt</strong>
        Alex and Lily embarked on a treasure hunt that led them to a mysterious cave. Inside the cave, they found a locked chest with a riddle written on it. The riddle stated, "To open the chest, find the least number that is a multiple of 4, 6, and 8." Remembering their lessons on LCM, Alex and Lily quickly calculated the LCM of 4, 6, and 8, which turned out to be 24. They used the number to unlock the chest and discovered a map to the hidden treasure.

        <strong>Challenge 2: The Magical Bridge</strong>
        As they continued their adventure, Alex and Lily encountered a magical bridge guarded by a mystical creature. The creature challenged them to find the least number of steps that would cause the bridge to light up. The steps were numbered 5, 7, and 9. Applying their knowledge of LCM, Alex and Lily calculated the LCM of 5, 7, and 9, which turned out to be 315. As they took 315 steps, the bridge lit up, allowing them to cross safely.

        <strong>Challenge 3: The Enchanted Garden</strong>
        In the final challenge, Alex and Lily entered an enchanted garden filled with beautiful flowers. They were tasked with arranging the flowers in rows, with each row containing 12, 15, and 18 flowers. Using the concept of LCM, they determined that they needed 180 flowers to fill each row without any flowers left over. The garden bloomed with vibrant colors, and the siblings completed their adventure successfully.

        <h2>FAQ</h2>

        <strong>What is the significance of finding the LCM of numbers?</strong>
        Finding the LCM is important in various mathematical and real-life scenarios. It helps in solving problems related to scheduling, repeating patterns, and resource allocation. In mathematics, the LCM is used in operations involving fractions, simplifying expressions, and solving equations.

        <strong>How is the LCM related to the concept of multiples?</strong>
        The LCM is directly related to the concept of multiples. It represents the smallest common multiple of two or more numbers. Multiples are the result of multiplying a number by an integer, and the LCM is the smallest multiple that is common to all the given numbers.

        <strong>Can the LCM be used to find the common denominator in fractions?</strong>
        Yes, the LCM is used to find the common denominator when adding or subtracting fractions. By finding the LCM of the denominators, you can convert the fractions to equivalent fractions with the same denominator, making it easier to perform operations.

        <strong>Are there specific methods to find the LCM of numbers?</strong>
        Yes, there are different methods to find the LCM, including listing multiples, using prime factorization, and using the method of division. Each method has its advantages and can be applied based on the given numbers and the preferred approach.

        <strong>How does the concept of LCM apply to real-life situations?</strong>
        The concept of LCM has practical applications in various real-life situations, such as scheduling events, planning recurring tasks, and organizing resources. It helps in determining the least amount of time, distance, or quantity needed to fulfill specific requirements, making it a valuable tool in problem-solving.

        Instruction:
        1. Always include Introduction, Defination, Methods, Example, Quizzes, Real-Life Applications and FAQs.
        2. Always put the h3 tag between each sub heading and strong tag between each context . For eg: "<h3>sub heading</h3>, <strong>context</strong>.
        3. Always compulsorily generate 5 Examples, 5 Tips and Tricks, 5 Quizzes,5 Real-Life Applications and 5 FAQs. More than one 'tips and tricks', 'Real-Life Applications' and 'quizzes' can be added for each keywords to make 5 in total for all three categories.
        4. Always generate article of around 5000-6000 words.
        5. Do not add a conclusion. Finish at FAQ.


        {context}
        """

    prompt = PromptTemplate(
        input_variables=["context"],
        template=prompt_template,)

    chain = LLMChain(llm=llm, prompt=prompt)

    query = f'''Generate me an article for "{topic}" in language "{language}". Compulsorily use these keywords in article : "{key_word}".'''

    content = chain.run(query)

    return content

# For Math Tricks Jr


@app.route('/submit_math_form', methods=['POST'])
def submit_math_form():
    google_sheet_ip = request.form['mathForm-name']
    print("Google Sheet IP from mathForm:", google_sheet_ip)
    # Get the current user's username
    user = current_user  # Get the current logged-in user
    print("Current user name:", user.name)
    if user:
        first_name = user.name

    else:
        first_name = ''

    print("Logged-in User's First Name:", first_name)

    # Handle the data from mathForm

    sheet_id = google_sheet_ip
    workbook = client.open_by_key(sheet_id)

    # Access the first sheet of the workbook
    sheet = workbook.sheet1

    created_contents = []
    failed_contents = []

    # Retrieve all values from the sheet along with row numbers
    all_rows_with_row_numbers = list(
        enumerate(sheet.get_all_records(), start=2))  # Start from row 2

    # Iterate through each row in the sheet along with row numbers
    for row_number, row_data in all_rows_with_row_numbers:
        article_title = row_data.get("article_title", "")
        seo_keywords = row_data.get("seo_keywords", "")
        language = row_data.get("language", "")
        status = row_data.get("Status", "")
        Date = row_data.get("Date", "")
        Time = row_data.get("Time", "")
        User = row_data.get("User", "")

        print(
            f"Article Title: {article_title}, SEO Keywords: {seo_keywords}, Language: {language}, Status: {status}, Date: {Date}, Time: {Time}")

        # Generate content for the article
        content = article_generator(article_title, seo_keywords, language)

        print(content)
        if content:
            print(f"Posted to WordPress: {article_title}")
            created_contents.append(article_title)
            # Prepare the payload
            # Prepare WordPress Post Data
            wordpress_payload = {
                "title": article_title,
                "content": content,
            }

            # Convert payload to bytes
            payload_bytes = json.dumps(wordpress_payload).encode('utf-8')

            # Send WordPress Post Request
            conn = http.client.HTTPSConnection("mathtricksjr.com")
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic TmlyYWphbl9hZG1pbjpSeEFTIEp5a3QgQ0lsOSBySmFIIFFzRXAgU0ZqeA=='
            }

            conn.request("POST", "/wp-json/wp/v2/posts", payload_bytes,
                         headers)  # Use payload_bytes instead of payload
            res = conn.getresponse()
            print(res)
            data = res.read()
            # Update status in Google Sheet
            if res.status == 201:
                date = datetime.now().strftime("%Y-%m-%d")
                time = datetime.now().strftime("%H:%M:%S")
                User_Name = f"{first_name}"
                sheet.update_cell(row_number, sheet.find(
                    "Status").col, "Posted successfully!")
                sheet.update_cell(row_number, sheet.find("Date").col, date)
                sheet.update_cell(row_number, sheet.find("Time").col, time)
                sheet.update_cell(
                    row_number, sheet.find("User").col, User_Name)
            else:
                sheet.update_cell(row_number, sheet.find(
                    "Status").col, "Post Failed!")
                sheet.update_cell(row_number, sheet.find("Date").col, date)
                sheet.update_cell(row_number, sheet.find("Time").col, time)
                failed_contents.append(article_title)
                print(data.decode("utf-8"))
        else:
            print(f"Failed to generate content for: {article_title}")
            # Update status in Google Sheet
            sheet.update_cell(
                row_number, sheet.find("Status").col, "Content Generation Failed!")
            failed_contents.append(article_title)

    else:
        print("No data found in the spreadsheet.")

    return render_template('siam.html', created_contents=created_contents, failed_contents=failed_contents)


# For Dansonsolutions


@app.route('/submit_DansonsolutionsForm', methods=['POST'])
def submit_DansonsolutionsForm():
    google_sheet_ip = request.form['DansonsolutionsForm-name']
    print("Google Sheet IP from Dansonsolutions:", google_sheet_ip)
    # Get the current user's username
    user = current_user  # Get the current logged-in user
    print("Current user name:", user.name)
    if user:
        first_name = user.name

    else:
        first_name = ''

    print("Logged-in User's First Name:", first_name)

    # Handle the data from mathForm

    sheet_id = google_sheet_ip
    workbook = client.open_by_key(sheet_id)

    # Access the first sheet of the workbook
    sheet = workbook.sheet1

    created_contents = []
    failed_contents = []

    # Retrieve all values from the sheet along with row numbers
    all_rows_with_row_numbers = list(
        enumerate(sheet.get_all_records(), start=2))  # Start from row 2

    # Iterate through each row in the sheet along with row numbers
    for row_number, row_data in all_rows_with_row_numbers:
        article_title = row_data.get("article_title", "")
        seo_keywords = row_data.get("seo_keywords", "")
        language = row_data.get("language", "")
        status = row_data.get("Status", "")
        Date = row_data.get("Date", "")
        Time = row_data.get("Time", "")
        User = row_data.get("User", "")

        print(
            f"Article Title: {article_title}, SEO Keywords: {seo_keywords}, Language: {language}, Status: {status}, Date: {Date}, Time: {Time}")

        # Generate content for the article
        content = article_generator(article_title, seo_keywords, language)

        print(content)
        if content:
            print(f"Posted to WordPress: {article_title}")
            created_contents.append(article_title)
            # Prepare the payload
            # Prepare WordPress Post Data
            wordpress_payload = {
                "title": article_title,
                "content": content,
            }

            # Convert payload to bytes
            payload_bytes = json.dumps(wordpress_payload).encode('utf-8')

            # Send WordPress Post Request
            conn = http.client.HTTPSConnection("dansonsolutions.com")
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ZGFuc29uYWRtaW46OWZrVCBHcUxwIDJ1Z3IgNDMwYyBDczBKIHM3V1U='
            }

            conn.request("POST", "/wp-json/wp/v2/posts", payload_bytes,
                         headers)  # Use payload_bytes instead of payload
            res = conn.getresponse()
            print(res)
            data = res.read()
            # Update status in Google Sheet
            if res.status == 201:
                date = datetime.now().strftime("%Y-%m-%d")
                time = datetime.now().strftime("%H:%M:%S")
                User_Name = f"{first_name}"
                sheet.update_cell(row_number, sheet.find(
                    "Status").col, "Posted successfully!")
                sheet.update_cell(row_number, sheet.find("Date").col, date)
                sheet.update_cell(row_number, sheet.find("Time").col, time)
                sheet.update_cell(
                    row_number, sheet.find("User").col, User_Name)
            else:
                sheet.update_cell(row_number, sheet.find(
                    "Status").col, "Post Failed!")
                sheet.update_cell(row_number, sheet.find("Date").col, date)
                sheet.update_cell(row_number, sheet.find("Time").col, time)
                failed_contents.append(article_title)
                print(data.decode("utf-8"))
        else:
            print(f"Failed to generate content for: {article_title}")
            # Update status in Google Sheet
            sheet.update_cell(
                row_number, sheet.find("Status").col, "Content Generation Failed!")
            failed_contents.append(article_title)

    else:
        print("No data found in the spreadsheet.")

    return render_template('danson.html', created_contents=created_contents, failed_contents=failed_contents)


if __name__ == '__main__':
    app.run(debug=True)
