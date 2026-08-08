import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(
    page_title="CineMatch | Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)


with open("style.css", "r", encoding="utf-8") as file:
    css = file.read()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)

@st.cache_data
def load_data():

    df = pd.read_csv("movies.csv")

    df["content"] = (
        df["genres"]
        .fillna("")
        .str.replace("|", " ", regex=False)

        + " "

        + df["keywords"]
        .fillna("")
        .str.replace(",", " ", regex=False)

        + " "

        + df["cast"]
        .fillna("")
        .str.replace("|", " ", regex=False)
    )

    return df


@st.cache_resource
def build_model(df):

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(
        df["content"]
    )

    # Calculate cosine similarity between all movies
    similarity = cosine_similarity(matrix)

    return similarity

df = load_data()

similarity = build_model(df)


st.html("""
<div class="hero">

    <div class="hero-badge">
        🎥 AI-Powered Movie Discovery
    </div>

    <div class="hero-title">
        CineMatch
    </div>

    <div class="hero-subtitle">
        Discover your next favorite movie,
        based on what you already love.
    </div>

</div>
""")


col1, col2, col3 = st.columns(3)


with col1:

    st.html(f"""
    <div class="stat-card">

        <div class="stat-number">
            {len(df)}
        </div>

        <div class="stat-label">
            Movies in Dataset
        </div>

    </div>
    """)


with col2:

    st.html("""
    <div class="stat-card">

        <div class="stat-number">
            🎯
        </div>

        <div class="stat-label">
            Content-Based Filtering
        </div>

    </div>
    """)


with col3:

    st.html("""
    <div class="stat-card">

        <div class="stat-number">
            ⚡
        </div>

        <div class="stat-label">
            Instant Recommendations
        </div>

    </div>
    """)



st.html("""
<div class="section-title">
    🎬 Tell us what you like
</div>

<div class="section-subtitle">
    Choose a movie you enjoyed and optionally tell us
    your preferred genres.
</div>
""")

col1, col2 = st.columns([1.5, 1])


with col1:

    selected_movie = st.selectbox(
        "🎬 Choose a movie you like:",
        df["title"].tolist()
    )


with col2:

    # Get all available genres
    genre_options = sorted(
        set(
            genre.strip()
            for row in df["genres"]
            for genre in row.split("|")
        )
    )

    selected_genres = st.multiselect(
        "❤️ Preferred genres (optional):",
        genre_options
    )


selected_movie_data = df[
    df["title"] == selected_movie
].iloc[0]


selected_movie_genres = (
    selected_movie_data["genres"]
    .replace("|", " • ")
)


if selected_genres:

    preferred_genres_text = (
        "❤️ Your preferred genres: "
        + " • ".join(selected_genres)
    )

else:

    preferred_genres_text = (
        "❤️ No additional genre preference selected"
    )


st.html(
    f"""
    <div class="taste-card">

        <div class="taste-label">
            YOUR MOVIE TASTE
        </div>

        <div class="taste-movie">
            🎬 {selected_movie}
        </div>

        <div class="taste-genres">

            🎭 {selected_movie_genres}

            <br>

            {preferred_genres_text}

        </div>

    </div>
    """
)

num_recommendations = st.slider(
    "Number of recommendations:",
    min_value=3,
    max_value=8,
    value=5
)

st.write("")

recommend_button = st.button(
    "✨ Find My Movies"
)


if recommend_button:

    movie_index = df.index[
        df["title"] == selected_movie
    ][0]

    scores = list(
        enumerate(
            similarity[movie_index]
        )
    )


    if selected_genres:

        for i, row in df.iterrows():

            movie_genres = row["genres"].split("|")

            matching_genres = sum(
                genre in movie_genres
                for genre in selected_genres
            )

            scores[i] = (
                i,
                scores[i][1]
                + (0.15 * matching_genres)
            )


    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )


    recommendations = []

    for index, score in scores:

        # Don't recommend the movie
        # that the user already selected
        if index != movie_index:

            recommendations.append(
                (index, score)
            )

        if len(recommendations) == num_recommendations:

            break


    st.html("""
    <div class="section-title">
        🍿 Your Recommendations
    </div>
    """)


    st.html(
        f"""
        <div class="section-subtitle">

            Because you liked
            <b>{selected_movie}</b>,
            here are some movies you might enjoy.

        </div>
        """
    )


    for rank, (index, score) in enumerate(
        recommendations,
        start=1
    ):

        movie = df.iloc[index]


        # Convert similarity score
        # into a percentage for display

        similarity_percentage = min(
            int(score * 100),
            99
        )


        genre_html = ""

        for genre in movie["genres"].split("|"):

            genre_html += (
                f'<span class="genre-badge">'
                f'{genre}'
                f'</span>'
            )


        if rank == 1:

            st.html(
                f"""
                <div class="featured-card">

                    <div class="featured-label">

                        🏆 TOP RECOMMENDATION

                    </div>


                    <div class="featured-title">

                        {movie["title"]}

                    </div>


                    <div>

                        {genre_html}

                    </div>


                    <div class="featured-description">

                        This is the highest-ranked
                        recommendation based on the
                        content similarity to
                        <b>{selected_movie}</b>.

                    </div>


                    <div class="movie-meta">

                        🎭 <b>Cast:</b>
                        {movie["cast"].replace("|", ", ")}

                    </div>


                    <div class="movie-meta">

                        🔍 <b>Keywords:</b>
                        {movie["keywords"]}

                    </div>


                    <div class="similarity-container">

                        <div class="similarity-label">

                            <span>
                                Similarity
                            </span>

                            <span>
                                {similarity_percentage}%
                            </span>

                        </div>


                        <div class="similarity-track">

                            <div
                                class="similarity-fill"
                                style="width:{similarity_percentage}%"
                            ></div>

                        </div>

                    </div>

                </div>
                """
            )


        else:

            st.html(
                f"""
                <div class="movie-card">

                    <div class="movie-rank">

                        RECOMMENDATION #{rank}

                    </div>


                    <div class="movie-title">

                        {movie["title"]}

                    </div>


                    <div>

                        {genre_html}

                    </div>


                    <div class="movie-meta">

                        🎭 <b>Cast:</b>
                        {movie["cast"].replace("|", ", ")}

                    </div>


                    <div class="movie-meta">

                        🔍 <b>Keywords:</b>
                        {movie["keywords"]}

                    </div>


                    <div class="similarity-container">

                        <div class="similarity-label">

                            <span>
                                Similarity
                            </span>

                            <span>
                                {similarity_percentage}%
                            </span>

                        </div>


                        <div class="similarity-track">

                            <div
                                class="similarity-fill"
                                style="width:{similarity_percentage}%"
                            ></div>

                        </div>

                    </div>

                </div>
                """
            )


st.html("""
<div class="info-card">

    <div class="info-title">
        🧠 How CineMatch Works
    </div>


    <div class="info-text">

        CineMatch uses
        <b>content-based filtering</b>
        to find movies that are similar
        to your selected movie.

    </div>


    <div class="workflow">


        <div class="workflow-step">

            <div class="workflow-icon">
                🎬
            </div>

            <div class="workflow-name">
                Your Movie
            </div>

        </div>


        <div class="workflow-arrow">
            →
        </div>


        <div class="workflow-step">

            <div class="workflow-icon">
                🔤
            </div>

            <div class="workflow-name">
                Movie Features
            </div>

        </div>


        <div class="workflow-arrow">
            →
        </div>


        <div class="workflow-step">

            <div class="workflow-icon">
                🧮
            </div>

            <div class="workflow-name">
                TF-IDF
            </div>

        </div>


        <div class="workflow-arrow">
            →
        </div>


        <div class="workflow-step">

            <div class="workflow-icon">
                📐
            </div>

            <div class="workflow-name">
                Cosine Similarity
            </div>

        </div>


        <div class="workflow-arrow">
            →
        </div>


        <div class="workflow-step">

            <div class="workflow-icon">
                🍿
            </div>

            <div class="workflow-name">
                Recommendations
            </div>

        </div>


    </div>

</div>
""")



st.html("""
<div class="custom-footer">

    🎬 <b>CineMatch</b>
    — Movie Recommendation System

    <br>

    Built with Python • Pandas • Scikit-learn • Streamlit

    <br><br>

    CODSOFT Internship — Task 4

</div>
""")