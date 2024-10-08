from manim import *

class BugDemo(Scene):
    def construct(self):
        # Create a graph with two edges
        graph1 = Graph(["A", "B", "C"], [("A", "B"), ("A", "C")])

        # Create another graph with three edges
        graph2 = Graph(["A", "B", "C"], [("A", "B"), ("A", "C"), ("B", "C")])

        # Display the first graph
        self.play(Create(graph1))
        self.wait(1)

        # Attempt to transform graph1 into graph2
        self.play(Transform(graph1, graph2))
        self.wait(1)

class ReplacementBugDemo(Scene):
    def construct(self):
        # Create a graph with two edges
        graph1 = DiGraph(["A", "B", "C"], [("A", "B"), ("A", "C"), ("B", "C")])

        # Create another graph with three edges
        graph2 = DiGraph(["A", "B", "C"], [("A", "B"), ("A", "C")])

        # Display the first graph
        self.play(Create(graph1))
        self.wait(1)

        # Attempt to transform graph1 into graph2
        self.play(ReplacementTransform(graph1, graph2))
        self.wait(1)
