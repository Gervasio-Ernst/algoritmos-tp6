import networkx as nx

# Crear grafo no dirigido para la casa (Punto a)
casa = nx.Graph()

ambientes = [
    'cocina',
    'comedor',
    'cochera',
    'quincho',
    'baño 1',
    'baño 2',
    'habitación 1',
    'habitación 2',
    'sala de estar',
    'terraza',
    'patio',
]
casa.add_nodes_from(ambientes)

# Punto b: Cargar al menos tres aristas por vértice y asignar peso 5 a dos aristas específicas
conexiones = [
    ('cocina', 'comedor', 5),  # Arista con peso 5
    ('cocina', 'sala de estar', 4),
    ('cocina', 'patio', 6),
    ('comedor', 'sala de estar', 3),
    ('comedor', 'baño 1', 5),  # Segunda arista con peso 5
    ('cochera', 'patio', 8),
    ('cochera', 'habitación 1', 10),
    ('cochera', 'sala de estar', 12),
    ('quincho', 'patio', 7),
    ('quincho', 'terraza', 9),
    ('quincho', 'comedor', 11),
    ('baño 1', 'habitación 1', 2),
    ('baño 1', 'habitación 2', 4),
    ('baño 2', 'habitación 2', 3),
    ('baño 2', 'terraza', 6),
    ('baño 2', 'patio', 10),
    ('habitación 1', 'habitación 2', 5),
    ('habitación 2', 'sala de estar', 6),
    ('sala de estar', 'terraza', 5),
    ('terraza', 'patio', 4),
]

casa.add_weighted_edges_from(conexiones)

print('=== Verificación de Grados (Mínimo 3 aristas por vértice) ===')
for nodo in casa.nodes():
  grado = casa.degree(nodo)
  print(f'  - {nodo}: {grado} conexiones')

print('\n=== PUNTO C: Árbol de Expansión Mínima (MST) ===')
mst_casa = nx.minimum_spanning_tree(casa, weight='weight')
total_metros_cables = sum(
    data['weight'] for u, v, data in mst_casa.edges(data=True)
)

for u, v, data in mst_casa.edges(data=True):
  print(f'  - {u} <---> {v} : {data["weight"]} metros')

print(
    f'\n  -> Total de metros de cables necesarios para conectar todos los'
    f' ambientes: **{total_metros_cables} metros**.'
)

print('\n=== PUNTO D: Camino más corto (Habitación 1 a Sala de estar) ===')
path_casa = nx.shortest_path(
    casa, source='habitación 1', target='sala de estar', weight='weight'
)
length_casa = nx.shortest_path_length(
    casa, source='habitación 1', target='sala de estar', weight='weight'
)

print(f'  - Ruta óptima: {path_casa}')
print(
    f'  - Metros de cable de red necesarios para conectar el router con el'
    f' Smart Tv: **{length_casa} metros**.'
)