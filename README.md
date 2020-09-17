# rss_filter_server
A Flask server to filter rss feed.  

## Usage
`GET /` require url params `rss_url` and `title_contains`.  
using the given `rss_url`, get it and filter it by `title_contains`.  
(remove item which not contains `title_contains`, by using lxml)

`GET /github_releases` require url params `repos_arg`.  
using the given repos name, for each them and combines to a rss feed.  
`repos_arg` format: `user_1/repo, user_2/repo, ...`, splitter is "," + space.
