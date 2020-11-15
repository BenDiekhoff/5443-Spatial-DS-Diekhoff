
import networkx as nx
import matplotlib.pyplot as plt

# PR = "Assignments\\A05\\Data\\Primary_Roads.geojson"
RR = "Assignments\\A05\\Data\\railroads.shp"

railGraph = nx.read_shp(RR, simplify=False, geom_attrs=True,strict=True)


