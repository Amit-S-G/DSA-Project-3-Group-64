Hello there! This is thr group repository for Group 64 of Spring 2024's Data Structures and Algorithms class at UF! Our program aims to help people see what different graph search algorithms look like and how they perform. We have implemented BFS, DFS, and A* for the searching algorithms, and you can see either the route that it outputs, or the nodes it visits on a visual map. The graph and map both use Paris, France as a base, and ONLY addresses in Paris will work for this, as that is how the graph is intialized.

You can simply run the main.py, but there are some dependencies.

You will need:

OSMNX, which has installation instructions here: https://osmnx.readthedocs.io/en/stable/installation.html
You will want to read this, OSMNX is _not_ simply pip-installable.

You will also want NetworkX, which is pip-installable. We are not sure if installing OSMNX will for sure also install NetworkX (as NetworkX is a dependency of OSMNX), so we just want to mention it here in case.

You will also need to install geopy, which is also pip-installable. You'll need Nominatim from this, which is linked to Open Street Maps, which powers OMSNX. An article about geocoding we used is here: https://medium.com/@hazallgultekin/convert-address-to-latitude-longitude-using-python-21844da3d032

That should cover all dependencies. Thank you all so much for a wonderful semester! The steetmap.png file in this repository shows an early test routing from Marston Science Library to Library West. It's just a neat little visual!

