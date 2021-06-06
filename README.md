# Jar of Ideas
### Jar of Ideas is a university project made for "Interactive internet technologies" module. The idea of this project is a forum made for start-ups where investors can contact a post auther and and simple people can't give ideas in the form of post.
# Prerequisite
    virtualenv
    python3

# Instalations

1.  Clone this repository
    ```sh
    git clone https://github.com/Necrorez/JarOfIdeas | cd JarOfIdeas
    ```
2. Create a virtual enviroment
    ```sh
    virtualenv -p python3 .
    ```
3. Activate the enviroment
    ```sh
    source bin/activate
    ```
4. Install needed libraries
    ```sh
    pip3 install -r  requirements.txt  
    ```
5. Create a .env file and add a secret key
    ```sh
    echo "SECRET_KEY=secret-key" > .env
    ```
6. Make model migrations to sqlite
    ```sh
    python3 manage.py makemigrations && python3 manage.py migrate
    ```

7. Run the server
    ```sh
    python3 manage.py runserver
    ```