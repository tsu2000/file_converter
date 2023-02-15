import streamlit as st
import PyPDF2
import pandas as pd
import base64
import io
import requests
import xlsxwriter

from PIL import Image
# from streamlit_extras.badges import badge

def main():
    col1, col2, col3 = st.columns([0.05, 0.265, 0.035])
    
    with col1:
        url = 'https://github.com/tsu2000/file_converter/raw/main/images/convert.png'
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        st.image(img, output_format = 'png')

    with col2:
        st.title('&nbsp; File Converter Web App')

    with col3:
        # badge(type = 'github', name = 'tsu2000/file_converter', url = 'https://github.com/tsu2000/file_converter')
        pass

    st.markdown('This web applications lets users convert files from one format to another. See the possible options for conversion in the drop-down menu. Suggest any other conversion methods [**here**](https://github.com/tsu2000/file_converter). For any concerns about the security of uploaded file data, view the official Streamlit documentation [**here**](https://docs.streamlit.io/knowledge-base/using-streamlit/where-file-uploader-store-when-deleted).')

    options = ['PDF to XLSX Converter',
               'TXT to CSV Converter',
               'CSV to JSON Converter']

    choice = st.selectbox('Select conversion process:', options)

    st.markdown('---')

    if choice == options[0]:
        pdf_to_xlsx()
    elif choice == options[1]:
        txt_to_csv()
    elif choice == options[2]:
        csv_to_json()


def pdf_to_xlsx():
    st.markdown('### PDF to XLSX Converter')

    # Upload PDF file
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Convert PDF to Excel
        with st.spinner('Converting PDF to Excel...'):
            # Create a PDF reader object
            reader = PyPDF2.PdfReader(uploaded_file)

            # Get the total number of pages in the PDF file
            num_pages = len(reader.pages)

            # Initialize a list to hold all the text data from the PDF file
            text_data = []

            # Loop through each page in the PDF file and extract the text data
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                text_data.append(page_text)

            # Create a pandas DataFrame from the text data
            df = pd.DataFrame(text_data, columns=['text'])

        # Download Excel file
        with st.spinner('Preparing download...'):
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine = 'xlsxwriter')
            df.to_excel(writer, sheet_name = 'Sheet1', index=False)
            writer.save()
            processed_data = output.getvalue()
            b64 = base64.b64encode(processed_data).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="output.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True)


def txt_to_csv():
    st.markdown('### TXT to CSV Converter')

    # Upload text file
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"])

    if uploaded_file is not None:
        # Read text file into a list of strings
        lines = uploaded_file.readlines()
        lines = [line.decode('utf-8').strip() for line in lines]

        # Split lines into columns using delimiter
        delimiter = st.text_input('Delimiter (default is ",")', ',')
        data = [line.split(delimiter) for line in lines]

        # Convert data to pandas DataFrame
        df = pd.DataFrame(data, columns=None)

        # Download CSV file
        with st.spinner('Preparing download...'):
            b64 = base64.b64encode(df.to_csv(index=False).encode()).decode()
            href = f'<a href="data:text/csv;base64,{b64}" download="output.csv">Download CSV file</a>'
            st.markdown(href, unsafe_allow_html=True)


def csv_to_json():
    st.markdown('### CSV to JSON Converter')

    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file into pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Convert DataFrame to JSON
        json_data = df.to_json(orient='records')

        # Download JSON file
        with st.spinner('Preparing download...'):
            b64 = base64.b64encode(json_data.encode()).decode()
            href = f'<a href="data:application/json;base64,{b64}" download="output.json">Download JSON file</a>'
            st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(page_title = 'File Converter', page_icon = ':pencil2:')
    main()
