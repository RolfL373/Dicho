from flask import Flask, render_template, request, redirect, url_for,send_file, session, flash
from flask_bootstrap import Bootstrap5
import tempfile
import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import datetime
import csv
import os
from io import BytesIO, TextIOWrapper
from dicho_data import (sound_files, codage, tr_index, di_index, tab_paires, client_header,
                        reference_ages, reference_values, confidence_intervals,bloc_size)

app = Flask(__name__)
app.secret_key='1234'
Bootstrap5(app)

dicho_results=[]
index_list=[]
register_flag=False
UPLOAD_FOLDER=tempfile.gettempdir()
# ----------
@app.route('/shutdown')
def shutdown():
    session.clear()
    os._exit(0)
    return "Server shutting down ..."

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()  # Shuts down the server

def calculate_age(b_date):
    birthdate = datetime.strptime(b_date, "%d/%m/%Y")
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    age = 15 if age > 11 else age
    return age

def test_nan(element):
    if pd.isna(element):
        return True
    else:
        return False

def select_elements(pairs):
    pair_list = []
    index_list=[]
    for l in range(0, len(pairs)):
        el = pairs.iloc[l].tolist()[2]
        ix = pairs.iloc[l].name
        if not test_nan(el):
            pair_list.append(el)
            index_list.append(int(ix))
    session["index_list"] = index_list

    return pair_list

def test_equality(lst):
    equality = all(x == lst[0] for x in lst)
    return equality

def opposite(l1, l2):
    if len(l1) == 0 or len(l2) == 0:
        return False
    if l1[0] == l2[0]:
        return False
    else:
        return True

def calc_lambda(vois, data):

    # Extract replies into a new dataframe; exclude NaN values and convert to list
    data_L = data[data.CODAGE == vois]["REPONSE"]
    data_L_list = data_L.dropna().tolist()
    # Calculate the lambda values for each data sample
    n_d = data_L_list.count("D")
    n_g = data_L_list.count("G")
    session["n_dicho"] = len(data_L)
    session["n_valid"] = n_d + n_g

    return math.log((n_d + 1) / (n_g + 1))

def plot_result(age,value):

    # Plot the reference value and the analysis results
    plt.figure(figsize=(8,6))
    plt.plot(reference_ages, reference_values, label='Reference', color='blue')
    plt.fill_between(
        reference_ages,
        [v - ci for v, ci in zip(reference_values, confidence_intervals)],
        [v + ci for v, ci in zip(reference_values, confidence_intervals)],
        color='blue', alpha=0.2, label='Confidence Interval'
    )
    plt.scatter(age, value, color='red', label='Data Point', zorder=5)
    plt.title('Comparison with reference data and confidence intervals')
    plt.xlabel('Age')
    plt.ylabel('Lambda-L')
    plt.legend()
    plt.grid(True)

    # Save the plot as a static image
    plot_path = os.path.join('static', 'plot.png')
    plt.savefig(plot_path)
    plt.close()


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    global register_flag
    if request.method == "POST":
        session['index'] = 0
        x = datetime.now()     # Current date and time
        yy = x.strftime("%y")  # Last two digits of the year
        mm = x.strftime("%m")  # Month
        dd = x.strftime("%d")  # Day

        # Get the data from the form
        data = request.form
        last_name = data["last_name"]
        birth_date = data["birthDate"]
        age=calculate_age(birth_date)    #returns "15"  if age > 11
        # Format the birth date as DDMMYYYY
        birth_date_formatted = datetime.strptime(birth_date, "%d/%m/%Y").strftime("%d%m%Y")
        # Construct the filename with current date, last name, and birth date
        filename = f"{yy}{mm}{dd}_{last_name}_{birth_date_formatted}.csv"

        user_data={
                "first_name": data['first_name'],
                "last_name": data["last_name"],
                "birth_date": data["birthDate"],
                "gender": data["gender"],
                "age": age,
                "filename": filename
                   }
        session["user_data"] = user_data
        register_flag=True
        print("in register", register_flag)

        # If file already exists, delete it; then create/initialize new file with header
        if os.path.exists(filename):
            os.remove(filename)

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(client_header)  # Write the header to the new file

        dicho_results.append(client_header)
        return redirect(url_for("home"))

    return render_template("register.html")

@app.route('/training')
def training():
    session['index'] = 0
    index = session['index']
    return render_template('training.html', audio_file=sound_files[tr_index[index]], next_index=index)

@app.route('/play_training')
def play_training():
    index = session['index']+1
    if index >= len(tr_index):
        index = 0  # Reset the index if it goes out of bounds
    session['index'] = index
    return render_template('training.html', audio_file=sound_files[tr_index[index]], next_index=index)

@app.route('/dicho_test')
def dicho_test():
    index = session['index']
    return render_template('dicho_test.html', audio_file=sound_files[di_index[index]], next_index=index)


@app.route('/play_dicho',methods=['GET', 'POST'])
def play_dicho():
    index = session['index']
    if index >= len(di_index):
        session['index'] = 0  # Reset the index if it goes out of bounds
        index=session['index']

    if request.method == "POST":
        data = request.form
        choice = data.get("option")
        bloc=int(index/bloc_size+1)
        stimulus=sound_files[di_index[index]].split(".")[0]
        code=codage[di_index[index]]
        c_data = [str(index+1), f"bloc "+str(bloc), str(stimulus),choice, "", "", "", "", code]

        if c_data[0] == dicho_results[-1][0]:   #if the 'BACK' option has been chosen, overwrite last result
            dicho_results[-1] = c_data
        else:
            dicho_results.append(c_data)

        session['index'] = index+1
        return redirect(url_for("play_dicho", index=index))
    return render_template('dicho_test.html', audio_file=sound_files[di_index[index]], next_index=index)

@app.route('/download_csv',methods=['GET'])
def download_csv():
    output = BytesIO()
    wrapper = TextIOWrapper(output, 'utf-8', newline='')
    writer = csv.writer(wrapper)
    for row in dicho_results:
        writer.writerow(row[1:])
    wrapper.flush()
    output.seek(0)
    wrapper.detach()

    user_data = session.get("user_data", {}) #retrieve filename
    filename = user_data["filename"]
    return send_file(output, mimetype='text/csv', download_name=filename, as_attachment=True)

@app.route("/select_data", methods=['GET', 'POST'])
def select_data():
    global register_flag
    print("in select data", register_flag)
    data_current=pd.DataFrame(dicho_results[1:],columns=client_header)
    filename="dicho_results.csv"
    file_path=os.path.join(UPLOAD_FOLDER, filename)
    data_current.to_csv(file_path, index=False)

    if request.method == "POST":    # archived file has been selected and is uploaded
        file = request.files['file']
        # Ensure the file is a .csv file
        if file and file.filename.endswith('.csv'):
            # Save the file to a temporary folder
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Create dummy user data for the result display
            user_data = {
                "first_name": "",
                "last_name": file.filename,
                "birth_date": "15",
                "gender": "",
                "age": 15,
                "filename": file.filename
            }
            session["user_data"] = user_data
            register_flag=False


            # Redirect to analyse_data and pass the file path as a URL parameter
            return redirect(url_for('analyse_data', file_path=file_path))

    return render_template("select_data.html", file_path=file_path, registered=register_flag)


@app.route("/analyse", methods=['GET', 'POST'])
def analyse_data():
    file_path = request.args.get('file_path')
    if file_path and os.path.exists(file_path):
        data_to_analyse = pd.read_csv(file_path)
    else:
        return "File not found or invalid file path", 400  # Return error if file path is invalid

    lambda_L_all = calc_lambda("L", data_to_analyse)
    dicho_l_total=session["n_dicho"]
    dicho_l_valid=session["n_valid"]
    data_to_analyse=eliminate_dominance(data_to_analyse)  # filter out 'dominance'
    lambda_L = calc_lambda("L", data_to_analyse)
    dicho_l_filtered = session["n_valid"]
    user_data = session.get("user_data", {})
    result_data={
        "dicho_l_total": dicho_l_total,
        "dicho_l_valid": dicho_l_valid,
        "dicho_l_filtered": dicho_l_filtered,
        "lambda_L_all": lambda_L_all,
        "lambda_L": lambda_L,
    }
    plot_result(user_data["age"], lambda_L)
    return render_template('show_data.html', userdata=user_data, results=result_data,registered=register_flag)

def eliminate_dominance(data):
    # eliminate 'dominance' when subject always hears the same of two sounds, independent of 'G' or 'D'
    session["n_eliminated"] = 0
    new_data=data

    for idx in range(len(tab_paires)):

        elim_index = []
        #r1 = list of all results where "pair1" is played
        r1 = select_elements(data[data.STIMULUS == tab_paires[idx]["pair1"]])
        elim_index.append(session["index_list"])

        # r2 = list of all results where "pair2" is played
        r2 = select_elements(data[data.STIMULUS == tab_paires[idx]["pair2"]])
        elim_index.append(session["index_list"])

        # elim_list = list of all indices where either pair1 or pair2 was played
        elim_list = elim_index[0] + elim_index[1]
        #Logic test: All elements of r1 AND all elements of r2 are equal; and r1 and r2 are opposite (D:G or G:D)
        eliminate = test_equality(r1) & test_equality(r2) & opposite(r1, r2)

        if eliminate:
            session["n_eliminated"] += len(elim_list)
            # Drop rows in elim_list, but don't reset the index
            new_data = new_data.drop(elim_list)
    print("eliminated total ", session["n_eliminated"])
    return new_data


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=False)