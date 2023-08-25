from flask import Flask, render_template, redirect, request
from modules.env import environ
from modules.backend import (
    get_auth_params,
    initialize_state,
    request_token,
    refresh_token,
    invalid_state
)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

"""""
Base this route on the callback URI.
After step 1 is completed, we are redirected here.
Check state variable matches existing, only complete step 2 if so.
"""
@app.route('/callback')
def callback():
    if invalid_state(request.args.get('state')):
        redirect("/")
    code = request.args.get('code')
    request_token(code)
    return render_template('redirect.html')

"""
In example, clicking authorize button redirects here
If token exists, refresh token.
If not, complete step 1.
"""
@app.route('/authorize', methods=['GET'])
def authorize():
    if refresh_token():
        return render_template('redirect.html')
    else:
        initialize_state()
        params = get_auth_params()
        return redirect(environ["AUTH_URL"] +
            '?' +
            '&'.join([f'{k}={v}' for k, v in params.items()])
                        )

if __name__ == '__main__':
    app.run(host='localhost', port=int(environ["FLASK_PORT"]))
