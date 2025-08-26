## Connations
This project is a web-based puzzle game inspired by NYT's Connections and Teuteuf Games Geogrid by implementing a similar gameplay but focusing the content on countries of the world. This project is built with Python on the backend and HTML/CSS/JS on the frontend.

## How to Play
The easiest way to play is to visit [https://connations.onrender.com](https://connations.onrender.com).
If this doesn't work, you can do the following:
1. Clone the repository:
```bash
git clone https://github.com/chatmartin/Connations.git
```
2. Create a virtual environment and activate it:
```bash
python -m venv venv
venv\Scripts\activate #For Windows users
source venv/bin/activate #For Mac/Linux users
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Start the Flask server:
```bash
python main.py
```
5. Go to http://127.0.0.1:5000 on your browser (or click the link in python's output).

## Features
- Select a group of four tiles to form a connection
- Shuffle and deselect buttons
- Game loss results in an auto-completion
- New board button generates a new random board
- UI with animations
- Share your results upon winning or losing
- Win/loss message along with message signifying you are one tile away from a connection.
- Learn more about each connection through the info modal

## Tech Stack
- Python 3
- Flask
- HTML / CSS / JavaScript

## Credits
- Inspired by New York Times Connections game and Teuteuf Games Geogrid
- [https://pngimg.com/uploads/un/small/un_PNG9.png](UN logo image)
- Much of the data was taken from Wikipedia or my knowledge
