mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"11014044@STUD.HOCHSCHULE-HEIDELBERG.DE\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml