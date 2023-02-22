# file_converter

A simple file conversion web application that allows users to convert (for now):

- MyAnimeList (MAL) `.xml` file exports to `.xlsx` files for greater readability. Available for both 'Anime List' and 'Manga List' files. View [**here**](https://myanimelist.net/panel.php?go=export) to see how to export your data.
- `.pdf` files to `.xlsx` files
- `.txt` files to `.csv` files
- `.csv` files to `.json` files

Any suggestion for different types of file conversions (that are widely used, or fulfill a specific niche) is welcome.

**Known limitations:**
- Individual file size for `st.file_uploader` is limited to a maximum of **200MB**
- Modules used may not be up-to-date, resulting in conversion errors, or unexpected data conversions.
- Encrypted `.pdf` files cannot be processed. Check `.pdf` security settings before uploading.

**Link to Web App**:

[<img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg">](<https://convert-file.streamlit.app>)
