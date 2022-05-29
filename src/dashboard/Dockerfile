FROM python:3.9.7

# Copy local code into docker image
ADD ./ /dashboard

# Change working directory to be the copied folder
WORKDIR /dashboard

# Install code dependencies
RUN pip install -r requirements.txt

ENV PORT = 8080
## This is the command that will be executed in "docker run <imagename>"
CMD streamlit run streamlit.py --server.port ${PORT}