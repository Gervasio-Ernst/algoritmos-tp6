import networkx as nx

# Crear grafo no dirigido (Punto h)
G = nx.Graph()

# Definir nodos y sus tipos (Punto a)
nodes = [
    ('Router 2', {'tipo': 'router'}),
    ('Router 1', {'tipo': 'router'}),
    ('Router 3', {'tipo': 'router'}),
    ('Switch 1', {'tipo': 'switch'}),
    ('Switch 2', {'tipo': 'switch'}),
    ('Guaraní', {'tipo': 'servidor'}),
    ('MongoDB', {'tipo': 'servidor'}),
    ('Red Hat', {'tipo': 'notebook'}),
    ('Debian', {'tipo': 'notebook'}),
    ('Arch', {'tipo': 'notebook'}),
    ('Manjaro', {'tipo': 'pc'}),
    ('Parrot', {'tipo': 'pc'}),
    ('Fedora', {'tipo': 'pc'}),
    ('Ubuntu', {'tipo': 'pc'}),
    ('Mint', {'tipo': 'pc'}),
    ('Impresora', {'tipo': 'impresora'}),
]

G.add_nodes_from(nodes)

# Cargar aristas con sus pesos según el esquema
edges = [
    ('Guaraní', 'Router 2', 9),
    ('Red Hat', 'Router 2', 25),
    ('Router 2', 'Router 3', 50),
    ('Router 2', 'Router 1', 37),
    ('Debian', 'Switch 1', 17),
    ('Ubuntu', 'Switch 1', 18),
    ('Impresora', 'Switch 1', 22),
    ('Mint', 'Switch 1', 80),
    ('Switch 1', 'Router 1', 29),
    ('Router 1', 'Router 3', 43),
    ('Router 3', 'Switch 2', 61),
    ('Manjaro', 'Switch 2', 40),
    ('Parrot', 'Switch 2', 12),
    ('Fedora', 'Switch 2', 3),
    ('Arch', 'Switch 2', 56),
    ('MongoDB', 'Switch 2', 5),
]

G.add_weighted_edges_from(edges)

print('=== PUNTO B: Barridos desde las tres notebooks ===')
notebooks = ['Red Hat', 'Debian', 'Arch']
for nb in notebooks:
  print(f'\nPartiendo desde {nb}:')
  dfs_nodes = list(nx.dfs_preorder_nodes(G, source=nb))
  bfs_nodes = list(nx.bfs_tree(G, source=nb).nodes())
  print(f'  - DFS (Profundidad): {dfs_nodes}')
  print(f'  - BFS (Amplitud):    {bfs_nodes}')

print('\n=== PUNTO C: Camino más corto a la Impresora ===')
origenes_c = ['Manjaro', 'Red Hat', 'Fedora']
for org in origenes_c:
  path = nx.shortest_path(G, source=org, target='Impresora', weight='weight')
  length = nx.shortest_path_length(
      G, source=org, target='Impresora', weight='weight'
  )
  print(f'  - Desde {org}: {path} (Distancia: {length})')

print('\n=== PUNTO D: Árbol de Expansión Mínima (MST) ===')
mst = nx.minimum_spanning_tree(G, weight='weight')
for u, v, data in mst.edges(data=True):
  print(f'  - {u} <---> {v} (Peso: {data["weight"]})')

print(
    '\n=== PUNTO E: PC (no notebook) con camino más corto al servidor Guaraní ==='
)
pcs = [
    n
    for n, data in G.nodes(data=True)
    if data['tipo'] == 'pc' and n not in notebooks
]
shortest_to_guarani = {}
for pc in pcs:
  length = nx.shortest_path_length(
      G, source=pc, target='Guaraní', weight='weight'
  )
  path = nx.shortest_path(G, source=pc, target='Guaraní', weight='weight')
  shortest_to_guarani[pc] = (length, path)
  print(f'  - {pc}: Distancia = {length}, Camino = {path}')

min_pc = min(shortest_to_guarani, key=lambda x: shortest_to_guarani[x][0])
print(
    f'\n  -> La PC con el camino más corto al servidor Guaraní es:'
    f' **{min_pc}**'
)

print('\n=== PUNTO F: Computadora del Switch 1 con camino más corto a MongoDB ===')
vecinos_switch1 = [
    n
    for n in G.neighbors('Switch 1')
    if G.nodes[n]['tipo'] in ['pc', 'notebook']
]
shortest_to_mongo = {}
for comp in vecinos_switch1:
  length = nx.shortest_path_length(
      G, source=comp, target='MongoDB', weight='weight'
  )
  path = nx.shortest_path(G, source=comp, target='MongoDB', weight='weight')
  shortest_to_mongo[comp] = (length, path)
  print(f'  - {comp}: Distancia = {length}, Camino = {path}')

# Corrección aplicada aquí (usando 'x' en vez de 'comp' dentro del lambda)
min_comp = min(shortest_to_mongo, key=lambda x: shortest_to_mongo[x][0])
print(
    f'\n  -> La computadora de Switch 1 con el camino más corto a MongoDB es:'
    f' **{min_comp}**'
)

print(
    '\n=== PUNTO G: Cambiar conexión de Impresora al Router 2 y resolver punto'
    ' b ==='
)
G_mod = G.copy()
if G_mod.has_edge('Impresora', 'Switch 1'):
  G_mod.remove_edge('Impresora', 'Switch 1')
G_mod.add_edge('Impresora', 'Router 2', weight=30)  # Conexión al router 2

for nb in notebooks:
  print(f'\nPartiendo desde {nb} (Impresora en Router 2):')
  dfs_mod = list(nx.dfs_preorder_nodes(G_mod, source=nb))
  bfs_mod = list(nx.bfs_tree(G_mod, source=nb).nodes())
  print(f'  - DFS: {dfs_mod}')
  print(f'  - BFS: {bfs_mod}')