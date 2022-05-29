mkdir -p ~/.dashboard/
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.dashboard/config.toml