from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Assuming you have already loaded your new_df and similarity
# For example, new_df = pd.read_csv('movies.csv') or similar
# Also, similarity should be calculated beforehand as in your original code

# Movie recommendation function
def recommend(movie):
    try:
        # Remove spaces and convert to lowercase
        movie_cleaned = movie.replace(" ", "").lower()
        
        # Find the movie index
        index = new_df[new_df['title'].str.replace(" ", "").str.lower() == movie_cleaned].index[0]
        
        # Get the movie distances
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        # Prepare a list of recommended movie titles
        recommendations = []
        for i in distances[1:6]:
            recommendations.append(new_df.iloc[i[0]].title)
        
        return recommendations
    except IndexError:
        return None  # If movie is not found, return None


# API endpoint to get movie recommendations
@app.route('/recommend', methods=['POST'])
def api_recommend():
    # Get the movie title from the query parameters
    movie = request.args.get('movie')
    
    if not movie:
        return jsonify({"error": "No movie title provided"}), 400
    
    # Get recommendations
    recommendations = recommend(movie)
    
    if recommendations:
        return jsonify({"recommendations": recommendations})
    else:
        return jsonify({"error": "Movie not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port= 10000, host='0.0.0.0')
