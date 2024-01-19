from decouple import config

__all__ = (
    "EXCLUDED_FILES",
    "ALLOWED_FILE_EXTENSIONS",
    "GIT_REPO_PATH",
    "GIT_REPO_URL",
    "RANDOM_BOOK_RATE_LIMIT",
    "GET_BOOK_RATE_LIMIT"
)

EXCLUDED_FILES = [".DS_Store"]
ALLOWED_FILE_EXTENSIONS = [".png", ".jpeg", ".jpg", ".gif"]
GIT_REPO_PATH = config("GIT_REPO_PATH", default = "./assets/git_repo", cast = str)
GIT_REPO_URL = config("GIT_REPO_URL", default = "https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books", cast = str)
RANDOM_BOOK_RATE_LIMIT = config("RANDOM_BOOK_RATE_LIMIT", default = 3, cast = int)
GET_BOOK_RATE_LIMIT = config("GET_BOOK_RATE_LIMIT", default = 3, cast = int)