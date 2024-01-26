from flask import Flask, request, render_template, redirect, url_for, Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laptops.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)  

class Laptop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    specs = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

laptops_bp = Blueprint('laptops', __name__)
api_laptops = Api(laptops_bp)

class LaptopResource(Resource):
    def get(self, laptop_id):
        laptop = Laptop.query.get_or_404(laptop_id)
        return {'id': laptop.id, 'brand': laptop.brand, 'model': laptop.model, 'specs': laptop.specs}

    def put(self, laptop_id):
        parser = reqparse.RequestParser()
        parser.add_argument('brand', type=str, required=True, help='Brand cannot be blank')
        parser.add_argument('model', type=str, required=True, help='Model cannot be blank')
        parser.add_argument('specs', type=str, required=True, help='Specs cannot be blank')

        args = parser.parse_args()
        laptop = Laptop.query.get_or_404(laptop_id)
        laptop.brand = args['brand']
        laptop.model = args['model']
        laptop.specs = args['specs']
        db.session.commit()
        return {'message': 'Laptop updated successfully'}

    def delete(self, laptop_id):
        laptop = Laptop.query.get_or_404(laptop_id)
        db.session.delete(laptop)
        db.session.commit()
        return {'message': 'Laptop deleted successfully'}

class LaptopsResource(Resource):
    def get(self):
        laptops = Laptop.query.all()
        laptops_data = [{'id': laptop.id, 'brand': laptop.brand, 'model': laptop.model, 'specs': laptop.specs} for laptop in laptops]
        return jsonify(laptops_data)

    def post(self):
        try:
            if request.content_type == 'application/json':
                data = request.get_json()
            else:
                data = request.form
            if 'brand' not in data or 'model' not in data or 'specs' not in data:
                return {'message': 'Missing required data'}, 400
            new_laptop = Laptop(brand=data['brand'], model=data['model'], specs=data['specs'])
            db.session.add(new_laptop)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return {'message': str(e)}, 500

api_laptops.add_resource(LaptopResource, '/laptop/<int:laptop_id>')
api_laptops.add_resource(LaptopsResource, '/laptops', endpoint='laptops')

@laptops_bp.route('/')
def get_laptops():
    laptops = Laptop.query.all()
    return render_template('index.html', laptops=laptops)

@laptops_bp.route('/delete/<int:laptop_id>', methods=['GET'])
def delete_laptop(laptop_id):
    laptop = Laptop.query.get_or_404(laptop_id)
    db.session.delete(laptop)
    db.session.commit()
    return redirect(url_for('laptops.get_laptops'))

@laptops_bp.route('/update/<int:laptop_id>', methods=['GET', 'POST'])
def update_laptop(laptop_id):
    laptop = Laptop.query.get_or_404(laptop_id)

    if request.method == 'POST':
        laptop.brand = request.form['brand']
        laptop.model = request.form['model']
        laptop.specs = request.form['specs']
        db.session.commit()
        return redirect(url_for('laptops.get_laptops'))

    return render_template('edit_laptops.html', laptop=laptop)

app.register_blueprint(laptops_bp)

if __name__ == '__main__':
    app.run(debug=True)
