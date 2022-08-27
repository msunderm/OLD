import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,PATCH,DELETE,OPTIONS"
        )
        response.headers.add("Acces-Control-Allow-Origins","*")
        return response

    @app.route("/")
    def hello():
        return "hello"
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    """
    @TODO:Create an endpoint to handle GET requests for all available categories.
    """
    @app.route("/categories", methods=['GET'])
    def all_categories():
        selections = Category.query.order_by(Category.id).all         
        if len(selections) == 0:
            abort(404)
        return jsonify(
            {
                "success": True,
                "categories": [selection.format() for selection in selections],
                "total_categories": len(Category.query.all()),
            }
        )
  
    """
    @TODO: Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions).
    """
    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1)*QUESTIONS_PER_PAGE 
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.route("/questions", methods=['GET'])
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request,selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions, 
                "totalQuestions": len(Question.query.all())
            }
        )   

    """

    http://127.0.0.1:5000/questions?page=2 works, also in postman


    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify ( 
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),  
                }
            )
        except:
            abort(422)      

    """
    @TODO:
    Create an endpoint to POST a new question,

 
    """
   
    @app.route("/questions", methods=['POST'])
    def create_questions():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        
        try:
            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(422)   
  

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    """
    @app.route("/questions", methods=["POST"])
    def get_questionsForSearch():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        search = body.get("search",None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search))
                )
                current_questions = paginate_questions(request, selection)
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                )
              
                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(selection.all()),
                    }
                )

            else:
                question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "questions": current_questions,
                        "total_questions": len(Question.query.all()),
                    }
                ) 
        except:
            abort(422)
        
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    This doesn't work correctly
    """
    

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions(category_id):
        questions = Question.query.order_by(Question.category==category_id).all()
  
        if questions is None:
            abort(404)

        else:
            return jsonify({
                'success': True,
                'questions': questions[category_id].format(),
                
            })    


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
 
    """

    """
    @TODO:
    Create error handlers for all expected errors
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    return app

