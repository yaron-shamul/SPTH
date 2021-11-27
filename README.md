# SPTH
shortest-path-to-hitler
A crawler, crawling through WikiPedia in order to find paths to Hitler!
Starting from a random page (or a specified page given via ARGV) and crawling all the way to the page of Adolf Hitler.

Currently supports:
 - DFS search
- Caching, in order to prevent re-requesting the same page

Options to add:
- Asynchronously get the data from the Api
