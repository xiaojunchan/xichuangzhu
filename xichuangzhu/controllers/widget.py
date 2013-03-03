from flask import render_template, request, redirect, url_for, json, render_template_string

from xichuangzhu import app

from xichuangzhu.models.widget_model import Widget

# page - admin widgets of a target
#--------------------------------------------------

# view
@app.route('/widget/admin/<target_type>/<int:target_id>', methods=['GET', 'POST'])
def admin_widgets(target_type, target_id):
	widgets = Widget.get_widgets(target_type, target_id)
	return render_template('admin_widgets.html', target_type=target_type, target_id=target_id, widgets=widgets)

# proc - add widget
@app.route('/widget/add', methods=['POST'])
def add_widget():
	target_type = request.form['target_type']
	target_id   = int(request.form['target_id'])
	title       = request.form['title']
	content     = request.form['content']
	index       = int(request.form['index'])

	Widget.add_widget(target_type, target_id, title, content, index)
	return redirect(url_for('admin_widgets', target_type=target_type, target_id=target_id))

# page - edit widget
#--------------------------------------------------

@app.route('/widget/edit/<int:widget_id>', methods=['GET', 'POST'])
def edit_widget(widget_id):
	if request.method == 'GET':
		widget = Widget.get_widget(widget_id)
		return render_template('edit_widget.html', widget=widget)
	elif request.method == 'POST':
		target_type = request.form['target_type']
		target_id   = int(request.form['target_id'])		
		title       = request.form['title']
		content     = request.form['content']
		index       = int(request.form['index'])

		Widget.edit_widget(widget_id, title, content, index)
		return redirect(url_for('admin_widgets', target_type=target_type, target_id=target_id))