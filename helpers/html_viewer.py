import webbrowser
import os

# Path to your HTML file
html_file = os.path.abspath("report.html")

# Open the file in the default browser
webbrowser.open(f"file://{html_file}")
