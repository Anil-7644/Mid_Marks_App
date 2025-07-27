import streamlit as st
import sqlite3
import re

# Connect to SQLite DB (create if not exists)
conn = sqlite3.connect('mid_marks.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mid_marks (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        roll_no TEXT NOT NULL,
        daa INTEGER CHECK(daa BETWEEN 0 AND 100),
        dld INTEGER CHECK(dld BETWEEN 0 AND 100),
        flat INTEGER CHECK(flat BETWEEN 0 AND 100),
        dbms INTEGER CHECK(dbms BETWEEN 0 AND 100),
        ps INTEGER CHECK(ps BETWEEN 0 AND 100)
    )
''')
conn.commit()

st.title("Mid Marks Entry Form")

with st.form("marks_form"):
    id = st.text_input("ID (e.g., N22123)")
    name = st.text_input("Name")
    roll = st.text_input("Roll Number")

    st.markdown("### Enter Mid Marks of Following Subjects")
    daa = st.number_input("DAA", min_value=0, max_value=100, step=1)
    dld = st.number_input("DLD", min_value=0, max_value=100, step=1)
    flat = st.number_input("FLAT", min_value=0, max_value=100, step=1)
    dbms = st.number_input("DBMS", min_value=0, max_value=100, step=1)
    ps = st.number_input("P&S", min_value=0, max_value=100, step=1)

    submitted = st.form_submit_button("Submit")

    if submitted:
        if not re.match(r'^N220\d{3}$', id):
            st.error("ID must start with N220 followed by 3 digits (e.g., N220123)")
        elif name.strip() == "" or roll.strip() == "":
            st.error("Name and Roll Number cannot be empty")
        elif 0 in [daa, dld, flat, dbms, ps]:
            st.error("Marks for all subjects must be *greater than 0*")
        else:
            try:
                cursor.execute('''
                    INSERT INTO mid_marks (id, name, roll_no, daa, dld, flat, dbms, ps)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (id, name, roll, daa, dld, flat, dbms, ps))
                conn.commit()
                st.success("Marks submitted successfully!")
                
                cursor.execute('SELECT * FROM mid_marks')
                rows = cursor.fetchall()
                st.subheader("📄 All Mid Marks Records")
                st.dataframe(rows, use_container_width=True)

            except sqlite3.IntegrityError:
                st.warning("A record with this ID already exists.")
            except Exception as e:
                st.error(f"Error occurred: {e}")