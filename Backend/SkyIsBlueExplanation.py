from manim import *

class WhyIsTheSkyBlue(Scene):
    def construct(self):
        # Scene 1: Introduction
        # Have you ever wondered why the sky appears blue? It's not because of the oceans!
        heading = Text("Why is the Sky Blue?", font_size=36).to_edge(UP)
        self.play(FadeIn(heading))
        narration1 = Text("Have you ever wondered why the sky appears blue?", font_size=20).to_edge(DOWN)
        self.play(Write(narration1))
        self.wait(2)
        narration2 = Text("It's not because of the oceans!", font_size=20).to_edge(DOWN)
        self.play(Transform(narration1, narration2))
        self.wait(3)
        self.play(FadeOut(narration1))

        # Earth and Atmosphere (Simplified)
        earth = Circle(radius=2, color=BLUE)
        atmosphere = Circle(radius=2.2, color=WHITE, fill_opacity=0.2)
        self.play(Create(earth), Create(atmosphere))
        self.wait(1)

        self.play(FadeOut(earth, atmosphere))
        self.play(FadeOut(heading))

        # Scene 2: Rayleigh Scattering Explanation
        # The answer lies in a phenomenon called Rayleigh scattering. Sunlight is made of all colors, but when it enters the Earth's atmosphere, it collides with tiny air molecules.
        heading = Text("Rayleigh Scattering", font_size=36).to_edge(UP)
        self.play(FadeIn(heading))
        narration3 = Text("The answer lies in a phenomenon called Rayleigh scattering.", font_size=20).to_edge(DOWN)
        self.play(Write(narration3))
        self.wait(3)
        narration4 = Text("Sunlight is made of all colors, but when it enters the Earth's atmosphere,", font_size=20).to_edge(DOWN)
        self.play(Transform(narration3, narration4))
        self.wait(3)
        narration5 = Text("it collides with tiny air molecules.", font_size=20).to_edge(DOWN)
        self.play(Transform(narration3, narration5))
        self.wait(3)
        self.play(FadeOut(narration3))

        # Atmosphere and light interaction
        atmosphere_zoom = Circle(radius=3, color=WHITE, fill_opacity=0.1).shift(UP*0.5)
        self.play(FadeIn(atmosphere_zoom))
        air_molecule1 = Circle(radius=0.05, color=GRAY).shift(LEFT*2 + UP*0.5)
        air_molecule2 = Circle(radius=0.05, color=GRAY).shift(RIGHT*1 + DOWN*0.3)
        self.play(Create(air_molecule1), Create(air_molecule2))

        sunlight1 = Arrow(start=LEFT*6 + UP*0.5, end=air_molecule1.get_center(), color=WHITE)
        sunlight2 = Arrow(start=LEFT*6 + DOWN*0.3, end=air_molecule2.get_center(), color=WHITE)
        self.play(Create(sunlight1), Create(sunlight2))

        blue_scatter1_1 = Arrow(start=air_molecule1.get_center(), end=air_molecule1.get_center() + UP*0.5, color=BLUE, max_tip_length_to_length_ratio=0.2)
        blue_scatter1_2 = Arrow(start=air_molecule1.get_center(), end=air_molecule1.get_center() + DOWN*0.3, color=BLUE, max_tip_length_to_length_ratio=0.2)
        blue_scatter1_3 = Arrow(start=air_molecule1.get_center(), end=air_molecule1.get_center() + RIGHT*0.4, color=BLUE, max_tip_length_to_length_ratio=0.2)

        blue_scatter2_1 = Arrow(start=air_molecule2.get_center(), end=air_molecule2.get_center() + UP*0.4, color=BLUE, max_tip_length_to_length_ratio=0.2)
        blue_scatter2_2 = Arrow(start=air_molecule2.get_center(), end=air_molecule2.get_center() + DOWN*0.5, color=BLUE, max_tip_length_to_length_ratio=0.2)
        blue_scatter2_3 = Arrow(start=air_molecule2.get_center(), end=air_molecule2.get_center() + LEFT*0.3, color=BLUE, max_tip_length_to_length_ratio=0.2)
        self.play(*[Create(x) for x in [blue_scatter1_1, blue_scatter1_2, blue_scatter1_3, blue_scatter2_1, blue_scatter2_2, blue_scatter2_3]])
        self.wait(1)

        red_light1 = Arrow(start=LEFT*6 + UP*1, end=RIGHT*0.5, color=RED)
        red_light2 = Arrow(start=LEFT*6 + DOWN*0.7, end=RIGHT*0.5, color=RED)

        # Blue light has a shorter wavelength and is scattered more easily in all directions than other colors like red and yellow.
        narration6 = Text("Blue light has a shorter wavelength and is scattered more easily", font_size=20).to_edge(DOWN)
        self.play(Write(narration6))
        self.wait(3)
        narration7 = Text("in all directions than other colors like red and yellow.", font_size=20).to_edge(DOWN)
        self.play(Transform(narration6, narration7))
        self.wait(3)
        self.play(FadeOut(narration6))

        self.play(*[FadeOut(x) for x in [atmosphere_zoom, air_molecule1, air_molecule2, sunlight1, sunlight2, blue_scatter1_1, blue_scatter1_2, blue_scatter1_3, blue_scatter2_1, blue_scatter2_2, blue_scatter2_3]])
        self.play(FadeOut(heading))

        # Scene 3: Demonstration
        # You can see a similar effect by adding a bit of milk to water and shining a light through it. The milk particles scatter the blue light, making the water appear blue from the side.
        heading = Text("Milk and Water Demonstration", font_size=36).to_edge(UP)
        self.play(FadeIn(heading))
        narration8 = Text("You can see a similar effect by adding a bit of milk to water", font_size=20).to_edge(DOWN)
        self.play(Write(narration8))
        self.wait(3)
        narration9 = Text("and shining a light through it. The milk particles scatter the blue light,", font_size=20).to_edge(DOWN)
        self.play(Transform(narration8, narration9))
        self.wait(3)
        narration10 = Text("making the water appear blue from the side.", font_size=20).to_edge(DOWN)
        self.play(Transform(narration8, narration10))
        self.wait(3)
        self.play(FadeOut(narration8))

        # Glass of water and milk
        water_glass = Rectangle(width=2, height=3, color=BLUE, fill_opacity=0.3).shift(LEFT*2)
        self.play(Create(water_glass))
        milk_particles = []
        for i in range(10):
            x = np.random.uniform(water_glass.get_left()[0]+0.2, water_glass.get_right()[0]-0.2)
            y = np.random.uniform(water_glass.get_bottom()[1]+0.2, water_glass.get_top()[1]-0.2)
            particle = Circle(radius=0.03, color=WHITE).move_to([x, y, 0])
            milk_particles.append(particle)
        self.play(*[Create(p) for p in milk_particles])

        white_light = Arrow(start=RIGHT*4 + UP*0.5, end=water_glass.get_right() + LEFT*0.1, color=WHITE)
        blue_light_scatter = []
        for particle in milk_particles:
            scatter = Arrow(start=particle.get_center(), end=particle.get_center() + UP*0.3 + LEFT*0.3, color=BLUE, max_tip_length_to_length_ratio=0.2)
            blue_light_scatter.append(scatter)
        self.play(Create(white_light))
        self.play(*[Create(s) for s in blue_light_scatter])
        self.wait(2)

        red_light = Arrow(start=RIGHT*4 + DOWN*0.5, end=water_glass.get_right() + LEFT*0.1, color=RED)
        self.play(*[FadeOut(x) for x in blue_light_scatter])
        self.play(Create(red_light))
        self.wait(2)

        self.play(*[FadeOut(x) for x in [water_glass] + milk_particles + [white_light, red_light]])
        self.play(FadeOut(heading))

        # Scene 4: Sunset Explanation
        # At sunset, the sunlight travels through much more of the atmosphere. The blue light is scattered away, leaving the longer wavelengths like red and orange to reach our eyes.
        heading = Text("Sunset Explanation", font_size=36).to_edge(UP)
        self.play(FadeIn(heading))
        narration11 = Text("At sunset, the sunlight travels through much more of the atmosphere.", font_size=20).to_edge(DOWN)
        self.play(Write(narration11))
        self.wait(3)
        narration12 = Text("The blue light is scattered away, leaving the longer wavelengths like red and orange", font_size=20).to_edge(DOWN)
        self.play(Transform(narration11, narration12))
        self.wait(3)
        narration13 = Text("to reach our eyes.", font_size=20).to_edge(DOWN)
        self.play(Transform(narration11, narration13))
        self.wait(3)
        self.play(FadeOut(narration11))

        # Earth and atmosphere at sunset
        earth = Circle(radius=2, color=BLUE)
        atmosphere = Circle(radius=2.2, color=YELLOW, fill_opacity=0.2)
        sun = Circle(radius=0.5, color=ORANGE).shift(RIGHT*5 + DOWN*2)
        self.play(Create(earth), Create(atmosphere), Create(sun))
        sunset_light = Arrow(start=sun.get_center(), end=earth.get_right()+UP*0.5, color=RED)
        self.play(Create(sunset_light))
        self.wait(3)
        self.play(*[FadeOut(x) for x in [earth, atmosphere, sun, sunset_light]])
        self.play(FadeOut(heading))

        # Scene 5: Summary
        # So, the sky is blue because of Rayleigh scattering, where blue light is scattered more than other colors. And sunsets are red because the blue light has been scattered away.
        heading = Text("Summary", font_size=36).to_edge(UP)
        self.play(FadeIn(heading))
        narration14 = Text("So, the sky is blue because of Rayleigh scattering, where blue light is scattered more than other colors.", font_size=20).to_edge(DOWN)
        self.play(Write(narration14))
        self.wait(4)
        narration15 = Text("And sunsets are red because the blue light has been scattered away.", font_size=20).to_edge(DOWN)
        self.play(Transform(narration14, narration15))
        self.wait(4)

        # Split screen (simplified)
        blue_sky = Rectangle(width=5, height=4, color=BLUE, fill_opacity=0.3).shift(LEFT*3)
        red_sunset = Rectangle(width=5, height=4, color=RED, fill_opacity=0.3).shift(RIGHT*3)
        self.play(Create(blue_sky), Create(red_sunset))
        self.wait(2)

        self.play(*[FadeOut(x) for x in [blue_sky, red_sunset]])
        self.play(FadeOut(heading, narration14))

        self.wait(2)
