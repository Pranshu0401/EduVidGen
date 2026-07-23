from manim import *
import random
import numpy as np

class SunsetExplanation(Scene):
    def construct(self):
        # Scene 1: Introduction (5 seconds)
        # Ever wondered why the setting sun looks so red? It's all about how sunlight interacts with our atmosphere.
        title = Text("Why is the Sunset Red?", font_size=48).move_to(UP*3)
        self.play(Write(title))
        sun_icon = Circle(radius=1, color=YELLOW).move_to(ORIGIN)
        self.play(Create(sun_icon))
        narration1 = Text("Ever wondered why the setting sun looks so red?", font_size=24).move_to(DOWN*3)
        self.play(Write(narration1))
        self.wait(2)
        narration2 = Text("It's all about how sunlight interacts with our atmosphere.", font_size=24).move_to(DOWN*3)
        self.play(Transform(narration1, narration2))
        self.wait(2)
        self.play(FadeOut(title, sun_icon, narration1))

        # Scene 2: Atmospheric Scattering (15 seconds)
        # Sunlight is made of all colors. As it enters the atmosphere, it collides with air molecules. This is called scattering.
        earth = Circle(radius=2, color=BLUE).move_to(RIGHT*4)
        continents = Circle(radius=1.8, color=GREEN).move_to(RIGHT*4)
        earth_group = VGroup(earth, continents)
        self.play(Create(earth_group))
        sun = Circle(radius=1, color=YELLOW).move_to(LEFT*4)
        self.play(Create(sun))

        num_molecules = 50
        molecules = []
        for _ in range(num_molecules):
            x = random.uniform(-4, 4)
            y = random.uniform(-3, 3)
            dot = Dot(point=[x, y, 0], color=BLUE, radius=0.03)
            molecules.append(dot)
        molecules_group = VGroup(*molecules)
        self.play(Create(molecules_group))

        red_lines = []
        for i in range(5):
            line = Line(start=sun.get_center(), end=earth.get_center() + UP * random.uniform(-0.5,0.5) + LEFT * random.uniform(-0.5,0.5), color=RED)
            red_lines.append(line)
        red_lines_group = VGroup(*red_lines)
        self.play(Create(red_lines_group))

        blue_lines = []
        for i in range(20):
            angle = random.uniform(0, 2 * PI)
            end_x = sun.get_x() + 3 * np.cos(angle)
            end_y = sun.get_y() + 3 * np.sin(angle)
            line = Line(start=sun.get_center(), end=[end_x, end_y, 0], color=BLUE)
            blue_lines.append(line)
        blue_lines_group = VGroup(*blue_lines)
        self.play(Create(blue_lines_group))

        narration3 = Text("Sunlight is made of all colors. As it enters the atmosphere,", font_size=24).move_to(DOWN*3)
        self.play(Write(narration3))
        self.wait(4)
        narration4 = Text("it collides with air molecules. This is called scattering.", font_size=24).move_to(DOWN*3)
        self.play(Transform(narration3, narration4))
        self.wait(4)
        narration5 = Text("Blue light is scattered more than red light.", font_size=24).move_to(DOWN*3)
        self.play(Transform(narration3, narration5))
        self.wait(3)
        narration6 = Text("That's why the sky is blue during the day.", font_size=24).move_to(DOWN*3)
        self.play(Transform(narration3, narration6))
        self.wait(4)
        self.play(FadeOut(earth_group, sun, molecules_group, red_lines_group, blue_lines_group, narration3))

        # Scene 3: Sunset Geometry (15 seconds)
        # At sunset, sunlight travels through much more of the atmosphere.
        earth = Circle(radius=2, color=BLUE).move_to(DOWN*2)
        continents = Circle(radius=1.8, color=GREEN).move_to(DOWN*2)
        earth_group = VGroup(earth, continents)
        self.play(Create(earth_group))
        sun_noon = Circle(radius=0.7, color=YELLOW).move_to(UP*3 + LEFT*5)
        self.play(Create(sun_noon))
        sun_sunset = Circle(radius=0.7, color=YELLOW).move_to(DOWN*2 + RIGHT*5)

        line_noon = Line(start=sun_noon.get_center(), end=earth.get_center(), color=YELLOW)
        self.play(Create(line_noon))
        line_sunset = Line(start=sun_sunset.get_center(), end=earth.get_center(), color=RED)
        self.play(Create(line_sunset))

        num_molecules = 50
        molecules = []
        for _ in range(num_molecules):
            x = random.uniform(-6, 6)
            y = random.uniform(-4, 4)
            dot = Dot(point=[x, y, 0], color=BLUE, radius=0.03)
            molecules.append(dot)
        molecules_group = VGroup(*molecules)
        self.play(Create(molecules_group))

        self.play(sun_noon.animate.move_to(sun_sunset.get_center()), run_time=5)

        red_lines = []
        for i in range(10):
            line = Line(start=sun_sunset.get_center(), end=earth.get_center() + UP * random.uniform(-0.5,0.5) + LEFT * random.uniform(-0.5,0.5), color=RED)
            red_lines.append(line)
        red_lines_group = VGroup(*red_lines)
        self.play(Create(red_lines_group))

        narration7 = Text("At sunset, sunlight travels through much more of the atmosphere.", font_size=24).move_to(UP*3)
        self.play(Write(narration7))
        self.wait(5)
        narration8 = Text("The blue light is scattered away, leaving mostly red light to reach our eyes.", font_size=24).move_to(UP*3)
        self.play(Transform(narration7, narration8))
        self.wait(5)
        self.play(FadeOut(earth_group, sun_noon, line_noon, line_sunset, molecules_group, red_lines_group, narration7))

        # Scene 4: Recap (5 seconds)
        # So, the next time you see a red sunset, remember it's because the blue light has been scattered away!
        sun_horizon = Circle(radius=1.5, color=RED).move_to(DOWN*3)
        self.play(Create(sun_horizon))
        recap_text = Text("Red Sunset = More Atmosphere = Less Blue Light", font_size=36).move_to(UP*1)
        self.play(Write(recap_text))
        narration9 = Text("So, the next time you see a red sunset, remember it's because", font_size=24).move_to(UP*3)
        self.play(Write(narration9))
        self.wait(2)
        narration10 = Text("the blue light has been scattered away!", font_size=24).move_to(UP*3)
        self.play(Transform(narration9, narration10))
        self.wait(3)
        self.play(FadeOut(sun_horizon, recap_text, narration9))