from flask import Flask
from ProductionCode.command_line import find_sightings_all_locations, find_most_popular_stop, load_csv

app = Flask(__name__)

@app.route('/sightingslocationsall/<int:year>/<bird>/')
def sightings_route(year: int, bird: str) -> str:
    """
    Usage guide: check readme.md
    """
    result = find_sightings_all_locations(bird, year)
    
    if result is None:
        return "The file was not found"

    return f"{bird} was sighted {result} times" 

@app.route('/mostpopularstop/<int:year>/')
def most_popular_route(year: int) -> str:
    """
    Usage guide: check readme.md
    """
    result = find_most_popular_stop(str(year))

    if result is None:
        return "Data for year not found"
    
    return f"Most popular stop for {year}: {result}"

@app.errorhandler(404)
def page_not_found(error):
    """
    Returns this when the error number 404 is thrown by the Flask app.
    """
    
    return '''
    Error Code 404 Not Found: Silly goose (Haha, get it? It's a bird website)! That page doesn\'t exist...<br>
    <br>
    To get a the number of a specific bird's sightings at all stops, do: /sightingslocationsall/BIRD_NAME/<br>
    Example usage: /sightingslocationsall/American Goldfinch (Carduelis tristis) /<br>
    <br>
    To get the most popular stop of a given year, do: /mostpopularstop/YEAR/<br>
    Example usage: /mostpopularstop/2018/<br>
    '''

@app.errorhandler(500)
def code_error(error):
    """
    Returns this when the error number 500 is thrown by the Flask app.
    """

    return 'Error Code 500 Internal Server Error: Fatal error with our code, sorry bro'

if __name__ == '__main__':
    app.run()