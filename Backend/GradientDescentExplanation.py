
from manim import *

class GradientDescent(Scene):
    def construct(self):
        # Scene 1: Introduction
        # Imagine you're on a mountain, and you want to get to the lowest point.
        # Gradient descent is like feeling around to find the steepest way down.
        title = Text("Gradient Descent: Finding the Bottom", color=WHITE, font_size=24).to_edge(UP)
        self.play(FadeIn(title))
        
        axes = Axes(x_range=[0, 10, 1], y_range=[0, 5, 1], x_length=7, y_length=5).move_to(DOWN)
        labels = axes.get_axis_labels(x_label="Model Parameters", y_label="Cost")
        
        def func(x):
            return 0.1 * (x - 5)**2 + 1
        
        curve = axes.plot(func, x_range=[0, 10], color=BLUE)
        
        red_dot = Dot(axes.coords_to_point(2, func(2)), color=RED)

        narration1 = Text("Imagine you're on a mountain, and you want to get to the lowest point.", font_size=18).to_edge(DOWN)
        self.play(FadeIn(axes, labels, curve,red_dot))
        self.play(Write(narration1))
        self.wait(2)
        narration2 = Text("Gradient descent is like feeling around to find the steepest way down.", font_size=18).to_edge(DOWN)

        self.play(Transform(narration1,narration2))
        self.wait(3)
        self.play(FadeOut(narration1))


        # Scene 2: The Descent
        # We calculate the slope at our current position (the gradient).
        # Then, we take a step in the opposite direction of the slope to reduce the cost.
        gradient_arrow = Arrow(start=axes.coords_to_point(2, func(2)), end=axes.coords_to_point(2 - 0.5, func(2) - 0.5), color=GREEN)
        self.play(Create(gradient_arrow))

        narration3 = Text("We calculate the slope at our current position (the gradient).", font_size=18).to_edge(DOWN)
        self.play(Write(narration3))
        self.wait(2)
        narration4 = Text("Then, we take a step in the opposite direction of the slope to reduce the cost.", font_size=18).to_edge(DOWN)
        self.play(Transform(narration3,narration4))
        self.wait(2)
        self.play(FadeOut(narration3))

        path = VMobject()
        path.set_points_as_corners([red_dot.get_center(), red_dot.get_center()])
        def update_path(path):
            new_point = red_dot.get_center()
            path.add_points_as_corners([new_point])

        path.add_updater(update_path)
        self.add(path)

        def move_dot(obj, alpha):
            obj.move_to(axes.coords_to_point(2 - 2*alpha, func(2 - 2*alpha)))
        self.play(UpdateFromAlphaFunc(red_dot, move_dot), run_time=3)
        self.remove(path)
        self.play(FadeOut(gradient_arrow))
        self.wait(1)

        # Scene 3: Overstepping and Learning Rate
        # If we take too big of a step (high learning rate), we might overshoot the minimum.
        # The learning rate controls the step size.
        red_dot_overshoot = Dot(axes.coords_to_point(2 - 1, func(2-1)), color=RED)
        self.add(red_dot_overshoot)

        narration5 = Text("If we take too big of a step (high learning rate), we might overshoot the minimum.", font_size=18).to_edge(DOWN)
        self.play(Write(narration5))
        self.wait(3)
        narration6 = Text("The learning rate controls the step size.", font_size=18).to_edge(DOWN)
        self.play(Transform(narration5,narration6))
        self.wait(2)
        self.play(FadeOut(narration5))

        learning_rate_text = Text("Learning Rate", font_size=20).shift(UP*2)
        learning_rate_arrow = Arrow(start=learning_rate_text.get_bottom(), end=red_dot_overshoot.get_center(), buff=0.5)
        self.play(Create(learning_rate_text), Create(learning_rate_arrow))
        self.wait(2)
        self.play(FadeOut(learning_rate_text, learning_rate_arrow,red_dot_overshoot))


        # Scene 4: Finding the Minimum
        # By carefully adjusting the learning rate and repeating this process, we gradually get closer and closer to the minimum,
        # finding the optimal parameter values.

        red_dot_minimum = Dot(axes.coords_to_point(7, func(7)), color=RED)
        self.add(red_dot_minimum)

        narration7 = Text("By carefully adjusting the learning rate and repeating this process, we gradually get closer and closer to the minimum,", font_size=16).to_edge(DOWN)
        self.play(Write(narration7))
        self.wait(3)
        narration8 = Text("finding the optimal parameter values.", font_size=16).to_edge(DOWN)
        self.play(Transform(narration7,narration8))
        self.wait(2)
        self.play(FadeOut(narration7))

        path2 = VMobject()
        path2.set_points_as_corners([red_dot_minimum.get_center(), red_dot_minimum.get_center()])
        def update_path2(path):
            new_point = red_dot_minimum.get_center()
            path.add_points_as_corners([new_point])

        path2.add_updater(update_path2)
        self.add(path2)

        def move_dot_minimum(obj, alpha):
            x_pos = 7 - (7-5)*alpha
            obj.move_to(axes.coords_to_point(x_pos, func(x_pos)))

        self.play(UpdateFromAlphaFunc(red_dot_minimum, move_dot_minimum), run_time=3)
        self.remove(path2)
        red_dot_minimum.set_color(GREEN)
        minimum_circle = Circle(radius=0.2, color=YELLOW).move_to(axes.coords_to_point(5, func(5)))
        self.play(Create(minimum_circle))
        self.wait(1)

        # Scene 5: Summary
        # So, gradient descent helps us find the best parameters for our model by iteratively calculating the gradient, adjusting the parameters, and repeating until we reach the minimum cost.
        summary_text = MarkupText(
            "Gradient Descent: " +
            "\n - Calculate the gradient. " +
            "\n - Adjust parameters. " +
            "\n - Repeat until minimum is found.",
            font_size=20
        ).to_edge(DOWN)

        narration9 = Text("So, gradient descent helps us find the best parameters for our model by iteratively calculating the gradient, adjusting the parameters, and repeating until we reach the minimum cost.", font_size=16).to_edge(DOWN)
        self.play(Write(narration9))
        self.wait(5)
        self.play(FadeOut(narration9))

        self.play(FadeIn(summary_text))
        self.wait(3)

        self.play(FadeOut(axes, labels, curve, red_dot_minimum, minimum_circle, summary_text,title))
        self.wait(1)
