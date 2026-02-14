import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ DATABASE CONNECTION ------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="student1_db"
    )


# ------------------ ADD STUDENT ------------------
def add_student(name, age, subject, marks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, age, subject, marks) VALUES (%s, %s, %s, %s)",
        (name, age, subject, marks)
    )
    conn.commit()
    conn.close()

# ------------------ VIEW STUDENTS ------------------
def view_students():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df

# ------------------ UPDATE MARKS ------------------
def update_marks(student_id, new_marks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET marks=%s WHERE id=%s",
        (new_marks, student_id)
    )
    conn.commit()
    conn.close()

# ------------------ DELETE STUDENT ------------------
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    conn.close()

# ------------------ STREAMLIT UI ------------------
st.title("🎓 Student Performance Management System")

menu = ["Add Student", "View Students", "Update Marks", "Delete Student", "Analytics"]
choice = st.sidebar.selectbox("Menu", menu)

# ------------------ ADD ------------------
if choice == "Add Student":
    st.subheader("Add New Student")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=5, max_value=100)
    subject = st.text_input("Subject")
    marks = st.number_input("Marks", min_value=0.0, max_value=100.0)

    if st.button("Add"):
        add_student(name, age, subject, marks)
        st.success("Student Added Successfully!")

# ------------------ VIEW ------------------
elif choice == "View Students":
    st.subheader("All Students")
    df = view_students()

    if not df.empty:
        df["Status"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")
        st.dataframe(df)
    else:
        st.warning("No records found.")

# ------------------ UPDATE ------------------
elif choice == "Update Marks":
    st.subheader("Update Student Marks")
    student_id = st.number_input("Student ID", min_value=1)
    new_marks = st.number_input("New Marks", min_value=0.0, max_value=100.0)

    if st.button("Update"):
        update_marks(student_id, new_marks)
        st.success("Marks Updated Successfully!")

# ------------------ DELETE ------------------
elif choice == "Delete Student":
    st.subheader("Delete Student Record")
    student_id = st.number_input("Student ID", min_value=1)

    if st.button("Delete"):
        delete_student(student_id)
        st.success("Student Deleted Successfully!")

# ------------------ ANALYTICS ------------------
elif choice == "Analytics":
    st.subheader("Performance Analytics")
    df = view_students()

    if not df.empty:
        df["Status"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")

        # Average Marks
        avg_marks = df["marks"].mean()
        st.write("📊 Overall Average Marks:", round(avg_marks, 2))

        # Pass Percentage
        pass_percent = (df["Status"] == "Pass").mean() * 100
        st.write("✅ Pass Percentage:", round(pass_percent, 2), "%")

        # Top Scorer
        top_scorer = df.loc[df["marks"].idxmax()]
        st.write("🏆 Top Scorer:", top_scorer["name"], "-", top_scorer["marks"])

        # Average per Subject
        subject_avg = df.groupby("subject")["marks"].mean()
        st.write("📘 Average Marks per Subject")
        st.dataframe(subject_avg)

        # Bar Chart
        st.subheader("Bar Chart: Subject vs Average Marks")
        fig1, ax1 = plt.subplots()
        subject_avg.plot(kind="bar", ax=ax1)
        st.pyplot(fig1)

        # Pie Chart
        st.subheader("Pie Chart: Pass/Fail Ratio")
        status_counts = df["Status"].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    else:
        st.warning("No data available for analysis.")