from app import create_app
from app.extensions import db

app = create_app()

from datetime import datetime

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}


if __name__ == '__main__':    
    with app.app_context():
        db.create_all()
    app.run(debug=True)