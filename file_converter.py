import streamlit as st
import PyPDF2
import pandas as pd
import base64
import io
import requests
import xmltodict
import json
import xlsxwriter

from PIL import Image
from streamlit_extras.badges import badge

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
        badge(type = 'github', name = 'tsu2000/file_converter', url = 'https://github.com/tsu2000/file_converter')

    st.markdown('This web applications lets users convert files from one format to another. See the possible options for conversion in the drop-down menu. Suggest any other conversion methods [**here**](https://github.com/tsu2000/file_converter). For any concerns about the security of uploaded file data, view the official Streamlit documentation [**here**](https://docs.streamlit.io/knowledge-base/using-streamlit/where-file-uploader-store-when-deleted).')

    options = ['MyAnimeList (MAL) Exported XML to XLSX Converter',
               'PDF to XLSX Converter',
               'TXT to CSV Converter',
               'CSV to JSON Converter']

    choice = st.selectbox('Select conversion process:', options)

    st.markdown('---')

    if choice == options[0]:
        malxml_to_xlsx()
    elif choice == options[1]:
        pdf_to_xlsx()
    elif choice == options[2]:
        txt_to_csv()
    elif choice == options[3]:
        csv_to_json()


def malxml_to_xlsx():
    st.markdown('### 📁 &nbsp; MyAnimeList (MAL) Exported XML to XLSX Converter')

    st.markdown('Converts an exported MyAnimeList File from an `.xml` file to a `.xlsx` format for greater readability. Available for both exported anime and manga lists on MyAnimeList. To get to the export page, click [**here.**](https://myanimelist.net/panel.php?go=export)')

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload", type=["xml"])

    if uploaded_file is not None:
        # Parse the XML file and convert it to a dictionary
        xml_data = uploaded_file.read().decode("utf-8")
        dict_data = xmltodict.parse(xml_data)

        # Convert the dictionary to a JSON string
        json_string = json.dumps(dict_data)
        json_dict = json.loads(json_string)

        # Get user data
        user = json_dict['myanimelist']['myinfo']
        user_df = pd.DataFrame(data = user.values(), index = user.keys(), columns = ['Result']).reset_index(names = ['Stat'])

        if 'anime' in json_dict['myanimelist']:
            # Get anime data

            # Check the type of the input data
            data = json_dict['myanimelist']['anime']

            if isinstance(data, list) and isinstance(data[0], dict):
                # Input data is a list of dictionaries
                df = pd.DataFrame(data = data)
            else:
                # Input data is a list of scalar values
                df = pd.DataFrame(data = data, index = [0])

            # Change data types of selected columns to appropriate formats:
            obj_to_int = ['series_animedb_id',
                          'series_episodes',
                          'my_id',
                          'my_watched_episodes',
                          'my_score',
                          'my_times_watched',
                          'my_rewatching',
                          'my_rewatching_ep',
                          'my_discuss']

            df[obj_to_int] = df[obj_to_int].astype(int)
            df['my_storage_value'] = df['my_storage_value'].astype(float)
            df[['my_start_date', 'my_finish_date']] = df[['my_start_date', 'my_finish_date']].replace('0000-00-00', pd.NaT)
            # st.write(df.dtypes)
            anime_df = df

        elif 'manga' in json_dict['myanimelist']:
            # Get manga data

            # Check the type of the input data
            data = json_dict['myanimelist']['manga']

            if isinstance(data, list) and isinstance(data[0], dict):
                # Input data is a list of dictionaries
                df = pd.DataFrame(data = data)
            else:
                # Input data is a list of scalar values
                df = pd.DataFrame(data = data, index = [0])

            # Change data types of selected columns to appropriate formats:
            obj_to_int = ['manga_mangadb_id',
                          'manga_volumes',
                          'manga_chapters',
                          'my_id',
                          'my_read_volumes',
                          'my_read_chapters',
                          'my_score',
                          'my_retail_volumes',
                          'my_times_read']

            df[obj_to_int] = df[obj_to_int].astype(int)
            df[['my_start_date', 'my_finish_date']] = df[['my_start_date', 'my_finish_date']].replace('0000-00-00', pd.NaT)
            # st.write(df.dtypes)
            manga_df = df

        # Create function that writes both anime and user data to 2 separate sheets in same workbook
        def anime_to_excel(anime_df, user_df):
            # Create a Pandas Excel writer
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine = 'xlsxwriter')

            # Write the first data frame to a sheet named 'Anime Data'
            anime_df.to_excel(writer, sheet_name = 'Anime Data', index = False)

            # Write the second data frame to a sheet named 'User Data'
            user_df.to_excel(writer, sheet_name = 'User Data', index = False)

            # Initialise workbook
            workbook = writer.book

            # Add formats and templates here        
            font_color = '#000000'

            # Column templates
            string_left_template = workbook.add_format(
                {
                    'font_color': font_color, 
                    'align': 'left'
                }
            )

            string_right_template = workbook.add_format(
                {
                    'font_color': font_color, 
                    'align': 'right'
                }
            )

            string_center_template = workbook.add_format(
                {
                    'font_color': font_color, 
                    'align': 'center'
                }
            )

            num_right_template = workbook.add_format(
                {
                    'num_format': '0',
                    'font_color': font_color, 
                }
            )

            num_center_template = workbook.add_format(
                {
                    'num_format': '0',
                    'font_color': font_color, 
                    'align': 'center'
                }
            )

            float_template = workbook.add_format(
                {
                    'num_format': '0.00',
                    'font_color': font_color, 
                }
            )

            # Header templates
            header_template_1 = workbook.add_format(
                {
                    'bg_color': '#cfe2f3', 
                    'border': 1
                }
            )

            header_template_2 = workbook.add_format(
                {
                    'bg_color': '#d9d2e9', 
                    'border': 1
                }
            )

            column_formats_1 = {
                'A': [num_right_template, 16],
                'B': [string_left_template, 60],
                'C': [string_center_template, 12],
                'D': [num_right_template , 16],
                'E': [num_right_template , 8],
                'F': [num_right_template , 20],
                'G': [string_right_template, 16],
                'H': [string_right_template, 16],
                'I': [string_left_template, 8],
                'J': [num_center_template, 8],
                'K': [string_left_template, 16],
                'L': [float_template, 16],
                'M': [string_center_template, 16],
                'N': [string_left_template, 16],
                'O': [num_right_template, 18],
                'P': [string_left_template, 20],
                'Q': [string_center_template, 12],
                'R': [string_left_template, 16],
                'S': [num_right_template, 16],
                'T': [num_right_template, 16],
                'U': [num_right_template, 16],
                'V': [string_center_template, 16],
                'W': [string_left_template, 16]
            }

            column_formats_2 = {
                'A': [string_right_template, 24],
                'B': [string_right_template, 12]
            }

            worksheet_1 = writer.sheets['Anime Data']
            worksheet_2 = writer.sheets['User Data']

            # Format columns for each worksheet:
            for column in column_formats_1.keys():
                worksheet_1.set_column(f'{column}:{column}', column_formats_1[column][1], column_formats_1[column][0])
                worksheet_1.conditional_format(f'{column}1:{column}1', {'type': 'no_errors', 'format': header_template_1})

            for column in column_formats_2.keys():
                worksheet_2.set_column(f'{column}:{column}', column_formats_2[column][1], column_formats_2[column][0])
                worksheet_2.conditional_format(f'{column}1:{column}1', {'type': 'no_errors', 'format': header_template_2})
            
            # Automatically apply Excel filter function on shape of dataframe
            worksheet_1.autofilter(0, 0, anime_df.shape[0], anime_df.shape[1]-1)

            # Saving and returning data
            writer.close()
            processed_data = output.getvalue()

            return processed_data

        def manga_to_excel(manga_df, user_df):
            # Create a Pandas Excel writer
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine = 'xlsxwriter')

            # Write the first data frame to a sheet named 'Manga Data'
            manga_df.to_excel(writer, sheet_name = 'Manga Data', index = False)

            # Write the second data frame to a sheet named 'User Data'
            user_df.to_excel(writer, sheet_name = 'User Data', index = False)

            # Initialise workbook
            workbook = writer.book

            # Add formats and templates here        
            font_color = '#000000'

            # Column templates
            string_left_template = workbook.add_format(
                {
                    'font_color': font_color, 
                    'align': 'left'
                }
            )

            string_right_template = workbook.add_format(
                {
                    'font_color': font_color, 
                    'align': 'right'
                }
            )

            string_center_template = workbook.add_format(
                {
                    'font_color': font_color, 
                    'align': 'center'
                }
            )

            num_right_template = workbook.add_format(
                {
                    'num_format': '0',
                    'font_color': font_color, 
                }
            )

            num_center_template = workbook.add_format(
                {
                    'num_format': '0',
                    'font_color': font_color, 
                    'align': 'center'
                }
            )

            float_template = workbook.add_format(
                {
                    'num_format': '0.00',
                    'font_color': font_color, 
                }
            )

            # Header templates
            header_template_1 = workbook.add_format(
                {
                    'bg_color': '#cfe2f3', 
                    'border': 1
                }
            )

            header_template_2 = workbook.add_format(
                {
                    'bg_color': '#d9d2e9', 
                    'border': 1
                }
            )

            column_formats_1 = {
                'A': [num_right_template, 16],
                'B': [string_left_template, 60],
                'C': [num_center_template, 16],
                'D': [num_right_template, 16],
                'E': [num_right_template, 16],
                'F': [num_right_template, 20],
                'G': [num_right_template, 16],
                'H': [string_center_template, 16],
                'I': [string_center_template, 16],
                'J': [num_center_template, 20],
                'K': [num_center_template, 12],
                'L': [float_template, 16],
                'M': [num_right_template, 16],
                'N': [string_center_template, 16],
                'O': [string_left_template, 18],
                'P': [num_right_template, 16],
                'Q': [string_left_template, 12],
                'R': [string_center_template, 12],
                'S': [num_right_template, 16],
                'T': [string_left_template, 16],
                'U': [string_left_template, 16],
                'V': [string_center_template, 16],
                'W': [string_left_template, 16]
            }

            column_formats_2 = {
                'A': [string_right_template, 24],
                'B': [string_right_template, 12]
            }

            worksheet_1 = writer.sheets['Manga Data']
            worksheet_2 = writer.sheets['User Data']

            # Format columns for each worksheet:
            for column in column_formats_1.keys():
                worksheet_1.set_column(f'{column}:{column}', column_formats_1[column][1], column_formats_1[column][0])
                worksheet_1.conditional_format(f'{column}1:{column}1', {'type': 'no_errors', 'format': header_template_1})

            for column in column_formats_2.keys():
                worksheet_2.set_column(f'{column}:{column}', column_formats_2[column][1], column_formats_2[column][0])
                worksheet_2.conditional_format(f'{column}1:{column}1', {'type': 'no_errors', 'format': header_template_2})
            
            # Automatically apply Excel filter function on shape of dataframe
            worksheet_1.autofilter(0, 0, manga_df.shape[0], manga_df.shape[1]-1)

            # Saving and returning data
            writer.close()
            processed_data = output.getvalue()

            return processed_data

        def get_table_download_link(df1, df2, type):
            """Generates a link allowing the data in a given Pandas DataFrame to be downloaded
            in:  dataframe
            out: href string
            """
            if type == 'anime':
                val = anime_to_excel(df1, df2)
            elif type == 'manga':
                val = manga_to_excel(df1, df2)

            b64 = base64.b64encode(val)

            return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="my_{type}_list.xlsx">:inbox_tray: Download (.xlsx)</a>'

        st.markdown('#### Your file is ready:')

        if 'anime' in json_dict['myanimelist']:
            st.markdown(get_table_download_link(anime_df, user_df, 'anime'), unsafe_allow_html = True)
        elif 'manga' in json_dict['myanimelist']:
            st.markdown(get_table_download_link(manga_df, user_df, 'manga'), unsafe_allow_html = True)


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
