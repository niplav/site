from manim import *

class PreferenceTransformation(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        def create_graph(visible_edges, position, scale=1, layout='tree'):
            # Determine vertical position based on outgoing edges
            out_edges = {v: sum(1 for e in visible_edges if e[0] == v) for v in 'abc'}
            sorted_vertices = sorted(out_edges.items(), key=lambda x: x[1], reverse=True)
            vertices = {
                v: np.array([
                    (1 if i == 1 else -1 if i == 2 else 0) * scale,
                    (1-i) * scale,
                    0
                ]) for i, (v, _) in enumerate(sorted_vertices)
            }

            # Create all possible edges
            all_possible_edges = [("a", "b"), ("b", "c"), ("c", "a")]
            edge_config = {}
            for edge in all_possible_edges:
                if edge in visible_edges:
                    edge_config[edge] = {"color": BLACK, "stroke_width": 2 * scale}
                else:
                    edge_config[edge] = {"color": WHITE, "stroke_opacity": 0}  # Completely invisible

            print(edge_config)

            g = DiGraph(vertices, all_possible_edges, layout="spring", layout_scale=2*scale,
                        vertex_config={"color": BLACK, "radius": 0.15*scale, "fill_opacity": 1},
                        edge_config=edge_config)

            # Adjust arrowhead size
            for edge in g.edges.values():
                edge.tip.scale(0.5 * scale)

            g.move_to(position)

            # Add node labels with increased size
            labels = VGroup(*[Text(v, color=BLACK, font_size=24*scale).next_to(g.vertices[v], UP*0.1)
                              for v in vertices])

            return VGroup(g, labels)

        # Create the initial cyclic graph (larger)
        initial_graph = create_graph([("a", "b"), ("b", "c"), ("c", "a")], LEFT * 3, 1.2, layout='circular')

        # Create the three acyclic graphs (smaller)
        scale_factor = 0.5
        acyclic1 = create_graph([("a", "b"), ("b", "c")], RIGHT * 3 + UP * 2, scale_factor, layout='tree')
        acyclic2 = create_graph([("b", "c"), ("c", "a")], RIGHT * 3, scale_factor, layout='tree')
        acyclic3 = create_graph([("c", "a"), ("a", "b")], RIGHT * 3 + DOWN * 2, scale_factor, layout='tree')

        # Display the initial graph
        self.play(Create(initial_graph))
        self.wait(1)

        # Transform to the acyclic graphs
        self.play(Transform(initial_graph.copy(), acyclic1))
        self.wait(1)
        self.play(Transform(initial_graph.copy(), acyclic2))
        self.wait(1)
        self.play(Transform(initial_graph.copy(), acyclic3))
        self.wait(1)

        # Fade out all objects
        self.play(*[FadeOut(mob) for mob in self.mobjects])

class PreferenceTransformationFade(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        def create_graph(edges, position, scale=1):
            vertices = {"a": [-1, 1, 0], "b": [1, 1, 0], "c": [0, -1, 0]}
            g = DiGraph(vertices, edges, layout="spring", layout_scale=2*scale,
                        vertex_config={"color": BLACK, "radius": 0.15*scale, "fill_opacity": 1},
                        edge_config={"color": BLACK, "stroke_width": 2 * scale})

            # Adjust arrowhead size
            for edge in g.edges.values():
                edge.tip.scale(0.5 * scale)

            g.move_to(position)

            # Add node labels
            labels = VGroup(*[Text(v, color=BLACK, font_size=24*scale).next_to(g.vertices[v], UP*0.1)
                              for v in vertices])

            return VGroup(g, labels)

        # Create the initial cyclic graph (larger)
        initial_graph = create_graph([("a", "b"), ("b", "c"), ("c", "a")], LEFT * 3, 1.2)

        # Create the three acyclic graphs (smaller)
        scale_factor = 0.5
        acyclic1 = create_graph([("a", "b"), ("b", "c")], RIGHT * 3 + UP * 2, scale_factor)
        acyclic2 = create_graph([("b", "c"), ("c", "a")], RIGHT * 3, scale_factor)
        acyclic3 = create_graph([("c", "a"), ("a", "b")], RIGHT * 3 + DOWN * 2, scale_factor)

        # Display the initial graph
        self.play(Create(initial_graph))
        self.wait(1)

        # Fade out initial graph and fade in acyclic graphs
        self.play(
            FadeIn(acyclic1),
            FadeIn(acyclic2),
            FadeIn(acyclic3)
        )
        self.wait(2)

        # Fade out all objects
        self.play(*[FadeOut(mob) for mob in self.mobjects])
