from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Clear session endpoint
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

# Index articles endpoint
@app.route('/articles')
def index_articles():
    # Query all articles
    articles = Article.query.all()
    
    # Serialize articles
    articles_list = [{
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'user_id': article.user_id
    } for article in articles]
    
    return jsonify(articles_list), 200

# Show article by ID endpoint
@app.route('/articles/<int:id>')
def show_article(id):
    
    if 'page_views' not in session:
        session['page_views'] = 0

    
    session['page_views'] += 1


    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    
    article = db.session.get(Article, id)

    if not article:
        return {'error': 'Article not found'}, 404

    
    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'author': article.author,  
        'preview': article.preview,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date,
        'user_id': article.user_id
    }), 200


if __name__ == '__main__':
    app.run(port=5555)
