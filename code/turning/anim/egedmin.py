from manim import *

class ResolvingInconsistentPreferences(Scene):
	def construct(self):
		# Create initial inconsistent graph
		vertices = {"A": [-1, 1, 0], "B": [1, 1, 0], "C": [0, -1, 0]}
		edges = [("A", "B"), ("B", "C"), ("C", "A")]
		g = DiGraph(vertices, edges, layout="spring", layout_scale=3,
				  vertex_config={"radius": 0.3},
				  edge_config={"tip_length": 0.2})

		self.play(Create(g))
		self.wait(1)

		self.play(g.animate.set_fill(RED), run_time=1)
		self.wait(1)

		# Show possible resolutions
		res1 = Graph(vertices, [("A", "B"), ("B", "C"), ("A", "C")], layout="spring", layout_scale=3,
					 vertex_config={"radius": 0.3},
					 edge_config={"tip_length": 0.2}).shift(LEFT * 3)
		res2 = Graph(vertices, [("B", "A"), ("A", "C"), ("B", "C")], layout="spring", layout_scale=3,
					 vertex_config={"radius": 0.3},
					 edge_config={"tip_length": 0.2}).shift(RIGHT * 3)

		self.play(
			Transform(g, res1),
			FadeIn(res2),
		)
		self.wait(1)

		# Highlight the differences
		removed_edge1 = Line(res1.vertices["C"].get_center(), res1.vertices["A"].get_center()).set_color(RED)
		added_edge1 = Arrow(res1.vertices["A"].get_center(), res1.vertices["C"].get_center(), buff=0.3).set_color(GREEN)

		removed_edge2 = Line(res2.vertices["A"].get_center(), res2.vertices["B"].get_center()).set_color(RED)
		added_edge2 = Arrow(res2.vertices["B"].get_center(), res2.vertices["A"].get_center(), buff=0.3).set_color(GREEN)

		self.play(
			Create(removed_edge1),
			Create(added_edge1),
			Create(removed_edge2),
			Create(added_edge2)
		)
		self.wait(2)

		self.play(
			*[FadeOut(mob) for mob in self.mobjects]
		)
