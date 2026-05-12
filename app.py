from flask import Flask, render_template, abort
import os
import markdown

app = Flask(__name__)

CONTENT_DIR = "content"

@app.route("/")
def home():
    categories = {
        "deployment": "Deployment Guides",
        "best_practices": "Best Practices",
        "troubleshooting": "Troubleshooting"
    }
    return render_template("home.html", categories=categories)

@app.route("/category/<category>")
def category(category):
    path = os.path.join(CONTENT_DIR, category)
    if not os.path.isdir(path):
        abort(404)

    articles = [
        f.replace(".md", "")
        for f in os.listdir(path)
        if f.endswith(".md")
    ]
    return render_template("category.html", category=category, articles=articles)

@app.route("/article/<category>/<article>")
def article(category, article):
    file_path = os.path.join(CONTENT_DIR, category, f"{article}.md")
    if not os.path.isfile(file_path):
        abort(404)

    with open(file_path, encoding="utf-8") as f:
        html = markdown.markdown(
            f.read(),
            extensions=["fenced_code", "tables"]
        )

    return render_template("article.html", content=html)
    
@app.route("/search")
def search():
    query = os.environ.get("QUERY", None)
    from flask import request
    query = request.args.get("q", "").lower()

    results = []

    if not query:
        return render_template("search.html", query=query, results=results)

    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                if query in content.lower() or query in file.lower():
                    category = os.path.basename(root)
                    article = file.replace(".md", "")

                    # Create preview snippet
                    index = content.lower().find(query)
                    start = max(index - 40, 0)
                    end = index + 40
                    snippet = content[start:end].replace("\n", " ")

                    results.append({
                        "title": article.replace("_", " ").title(),
                        "category": category,
                        "snippet": snippet
                    })

    return render_template("search.html",
                           query=query,
                           results=results)
                           
from flask import jsonify, request

@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").lower()
    results = []

    if len(query) < 2:
        return jsonify(results)

    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, encoding="utf-8") as f:
                    content = f.read().lower()

                if query in content or query in file.lower():
                    category = os.path.basename(root)
                    article = file.replace(".md", "")

                    results.append({
                        "title": article.replace("_", " ").title(),
                        "url": f"/article/{category}/{article}"
                    })

    return jsonify(results[:10])  # limit results



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
