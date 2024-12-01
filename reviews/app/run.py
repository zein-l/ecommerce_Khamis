import sys
import os
from reviews.app import create_app
from reviews.app.db import db

# Ensure the parent directory is included in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = create_app()

if __name__ == '__main__':
    # Create the database tables within the app context
    with app.app_context():
        db.create_all()
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5004)

for rule in app.url_map.iter_rules():
    print(f"Endpoint: {rule.endpoint}, Methods: {rule.methods}, URL: {rule.rule}")
