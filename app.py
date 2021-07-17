from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
posts = {
    0: {
        'post_id': 0,
        'title': 'Hello, world!',
        'content': 'This is my first blog post'
    }
}


@app.route('/')
def home():
    return render_template('home.html', posts=posts)


@app.route('/posts/<int:post_id>')
def read_post(post_id):
    post = posts.get(post_id)
    if not post:  # if post_id value not found in posts keys - returns None
        return render_template('404.html', message=f'A post with id {post_id} was not found.')
    return render_template('post.html', post=post)


# This route will just render another page with the form.
# HTML forms can then send data to another route... /posts/create in this case.
# @app.route('/posts/form')
# def post_input_form():
#     return render_template('create.html')


# This route will be arrived at looking like this:
# 127.0.0.1:5000/posts/create, but with either:
# # - POST and including the form inner data as part of the payload (which is hidden), containing the data in the form.; or
# # - the user may load this page with the browser—which is always using GET.
@app.route('/posts/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')  # This takes the 'Hello' from the title query string parameter
        content = request.form.get('content')  # This takes the 'This is the post content' form the content query string parameter.
        post_id = len(posts)  # This just gives us a new post_id as the number of posts currently existing (thing of it as an auto-increment).
        posts[post_id] = {
            'post_id': post_id,
            'title': title,
            'content': content
        }
        # Ths url_for gives us the route associated with the `read_post` function (defined in line 19). The route is /posts/<int:post_id>
        # So we must also give it the argument it requires.
        # redirect then sends a response which tells the browser to load the other route instead of the one we're in.
        return redirect(url_for('read_post', post_id=post_id))
    return render_template('create.html')  # if method == GET - we show post form page


if __name__ == '__main__':
    app.run(debug=True)
