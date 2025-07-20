from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

# In-memory data store
items = []

@app.route('/')
def home():
    status_filter = request.args.get('status')
    filtered_items = [item for item in items if item['status'] == status_filter] if status_filter else items
    statuses = sorted(set(item['status'] for item in items))
    return render_template('home.html', items=filtered_items, statuses=statuses, selected=status_filter)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_item = {
            'id': str(uuid.uuid4()),
            'title': request.form['title'],
            'description': request.form['description'],
            'status': request.form['status'],  # "Lost" or "Found"
            'image': request.form['image']  # static/images/xxx.jpg
        }
        items.append(new_item)
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/item/<id>')
def item_detail(id):
    item = next((i for i in items if i['id'] == id), None)
    if not item:
        return "<h2>Item not found.</h2>", 404
    return render_template('item.html', item=item)

if __name__ == '__main__':
    app.run(debug=True)
