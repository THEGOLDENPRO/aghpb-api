from decouple import config

__all__ = (
    "EXCLUDED_FILES",
    "ALLOWED_FILE_EXTENSIONS",
    "GIT_REPO_PATH",
    "GIT_REPO_URL"
)

EXCLUDED_FILES = [".DS_Store"]
ALLOWED_FILE_EXTENSIONS = [".png", ".jpeg", ".jpg", ".gif"]
GIT_REPO_PATH = config("GIT_REPO_PATH", default = "./assets/git_repo", cast = str)
GIT_REPO_URL = config("GIT_REPO_URL", default = "https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books", cast = str)