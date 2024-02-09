import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader , Template
import sys


df = pd.read_csv("./data.csv")
# print(df)
# print(df.info())  # All are int64



def generate_student_html(student_id):
    df = pd.read_csv("./data.csv")
    # Filter data for the given Student id
    std_df = df[df["Student id"] == int(student_id)]

    # print(std_df)
    # print(std_df.info())
    # print((std_df[' Marks']))
    # Calculate total marks
    total_marks = std_df[' Marks'].sum()
    

    # Create an HTML table
    html_table = std_df.to_html(index=False, classes="table")

    # Generate the complete HTML page
    template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Details</title>
    </head>
    <body>
        <h1>Student Details</h1>
            {% if std_df %}
         <table>
            <tr>
                <th>Student id</th>
                <th>Course id</th>
                <th>Marks</th>
            </tr>
            {% for row in std_df %}
            <tr>
                <td>{{ row['Student id'] }}</td>
                <td>{{ row[' Course id'] }}</td>
                <td>{{ row[' Marks'] }}</td>
            </tr>
            {% endfor %}
            <tr>
                    <td colspan="2">Total Marks</td>
                    <td>{{ total_marks }}</td>
            </tr>
        </table>
        {% endif %}

    </body>
    </html>
    """)
    html_page = template.render(std_df=std_df.to_dict(orient='records'), total_marks=total_marks)
    with open('output.html', 'w') as file:
        file.write(html_page)
    return html_page


def generate_course_html(course_id):

    df = pd.read_csv("./data.csv")

    # Filter data for the given Course id
    course_df = df[df[" Course id"] == int(course_id)]

    # Calculate average and maximum marks
    average_marks = course_df[" Marks"].mean()
    max_marks = course_df[" Marks"].max()

    # Create a histogram of marks
    plt.hist(course_df[" Marks"], bins=10, edgecolor='black')
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.title(f"Histogram of Marks for Course {course_id}")
    plt.savefig("histogram.png")  # Save the histogram as an image

    # Generate the complete HTML page
    template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Course Details</title>
    </head>
    <body>
        <h1>Course Details</h1>
        <table>
            <tr>
                <th>Average Marks</th>
                <th>Maximum Marks</th>
            </tr>
            <tr>
                <td>{average_marks:.2f}</td>
                <td>{max_marks}</td>
            </tr>
        </table>
        <img src="histogram.png" alt="Histogram of Marks">
    </body>
    </html>
    """)
    html_page = template.render(std_df=course_df.to_dict(orient='records'), average_marks=average_marks ,max_marks=max_marks )
    with open('output.html', 'w') as file:
        file.write(html_page)
    return html_page




def main():
    if len(sys.argv) != 3:
        print("Invalid number of arguments. Usage: python app.py [-s|-c] <id>")
        return

    option = sys.argv[1]
    id_param = int(sys.argv[2])
 
    if option == '-s':
        # print(option , id_param)
        print(generate_student_html(id_param))
    elif option == '-c':
        # print(option , id_param)
        print(generate_course_html(id_param))
    else:
        print("Provide Correct Arguments")


if __name__ == "__main__":
    main()
