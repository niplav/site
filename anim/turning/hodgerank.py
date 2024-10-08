from manim import *
import numpy as np

class HodgeRankResolution(Scene):
	def construct(self):
		self.camera.background_color = WHITE
		# Create initial edge-weighted graph
		vertices = {"A": [-2, 1, 0], "B": [0, 2, 0], "C": [2, 1, 0], "D": [0, -2, 0]}
		edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C"), ("B", "D")]
		weights = {"AB": 2, "BC": 1, "CD": 3, "DA": -2, "AC": 4, "BD": -1}

		g = DiGraph(vertices, edges, layout="planar", layout_scale=3,
				  vertex_config={"radius": 0.1},
				  edge_config={"tip_length": 0.2}).set_color(BLACK)

		# Add weight labels
		weight_labels = {}
		for edge, weight in weights.items():
			start, end = edge
			mid_point = (g.vertices[start].get_center() + g.vertices[end].get_center()) / 2
			label = Text(str(weight), font_size=24, color=BLACK).move_to(mid_point).shift(0.3 * UP)
			weight_labels[edge] = label

		self.play(Create(g))
		self.play(*[Write(label) for label in weight_labels.values()])
		self.wait(1)

		# Simulate HodgeRank calculation (simplified)
		potentials = {"A": 0, "B": 2, "C": 3, "D": 1}

		# Show potentials
		potential_labels = {}
		for vertex, potential in potentials.items():
			label = Text(f"{potential:.1f}", font_size=24, color=PURPLE).next_to(g.vertices[vertex], DOWN)
			potential_labels[vertex] = label

		self.play(*[Write(label) for label in potential_labels.values()])
		self.wait(1)

		# Show new edge weights
		new_weights = {}
		new_weight_labels = {}
		for edge, weight in weights.items():
			start, end = edge
			new_weight = potentials[end] - potentials[start]
			new_weights[edge] = new_weight
			mid_point = (g.vertices[start].get_center() + g.vertices[end].get_center()) / 2
			label = Text(f"{new_weight:.1f}", font_size=24, color=GREEN).move_to(mid_point).shift(0.3 * DOWN)
			new_weight_labels[edge] = label

		g.set_color(BLACK)
		self.play(*[Transform(weight_labels[edge], new_label) for edge, new_label in new_weight_labels.items()])
		self.wait(1)

		# Show final ranking
		ranking = sorted(potentials.items(), key=lambda x: x[1], reverse=True)
		ranking_text = VGroup(*[Text(f"{v}: {p:.1f}", font_size=24) for v, p in ranking]).arrange(DOWN).to_edge(RIGHT)

		self.play(Write(ranking_text))
		self.wait(2)

		self.play(*[FadeOut(mob) for mob in self.mobjects])
