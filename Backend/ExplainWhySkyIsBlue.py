```python
from manim import *

class RayleighScattering(Scene):
    def construct(self):
        # Scene 1: Introduction
        # Have you ever wondered why the sky appears blue? It's a question that puzzled scientists for centuries!
        heading = Text("Why is the Sky Blue?", font_size=60).move_to(UP*3.5) # Title
        self.play(FadeIn(heading))
        narration1 = Text("Have you ever wondered why the sky appears blue?", font_size=24).move_to(DOWN*3.5)
        self.play(FadeIn(narration1))
        self.wait(2)
        narration2 = Text("It's a question that puzzled scientists for centuries!", font_size=24).move_to(DOWN*3.5)
        self.play(Transform(narration1, narration2))

        self.wait(3)
        self.play(FadeOut(heading, narration1))

        # Scene 2: Explanation of Rayleigh Scattering
        # Sunlight, which looks white, is actually made up of all the colors of the rainbow.
        heading = Text("Rayleigh Scattering", font_size=60).move_to(UP*3.5) # Title
        self.play(FadeIn(heading))

        sun = Circle(radius=0.5, color=WHITE).move_to(UP*3)
        self.play(Create(sun))
        narration1 = Text("Sunlight, which looks white, is actually made up of all the colors of the rainbow.", font_size=24).move_to(DOWN*3.5)
        self.play(FadeIn(narration1))

        self.wait(5)

        # As sunlight enters the Earth's atmosphere, it collides with tiny air molecules like nitrogen and oxygen.
        earth = Circle(radius=1, color=BLUE).move_to(DOWN*2)
        self.play(Create(earth))
        molecules = VGroup(*[Circle(radius=0.05, color=GRAY).move_to([np.random.uniform(-6, 6), np.random.uniform(-1, 2), 0]) for _ in range(20)])
        self.play(Create(molecules))
        narration2 = Text("As sunlight enters the Earth's atmosphere, it collides with tiny air molecules like nitrogen and oxygen.", font_size=24).move_to(DOWN*3.5)
        self.play(Transform(narration1, narration2))

        self.wait(5)

        # This collision causes a phenomenon called Rayleigh scattering, where light is scattered in different directions. Blue light is scattered much more than other colors because it travels as shorter, smaller waves.
        def create_scattering_animation(color, scale):
            animations = []
            for molecule in molecules:
                line = Line(start=sun.get_center(), end=molecule.get_center(), color=color)
                dot = Dot(molecule.get_center(), color=color)
                animations.append(Create(line))
                animations.append(Create(dot))
                animations.append(ScaleInPlace(dot, scale))
            return animations

        scattering_blue = create_scattering_animation(BLUE, 2)
        self.play(*scattering_blue, run_time=3)
        narration3 = Text("This collision causes a phenomenon called Rayleigh scattering, where light is scattered in different directions.", font_size=24).move_to(DOWN*3.5)
        self.play(Transform(narration1, narration3))
        self.wait(2)
        narration4 = Text("Blue light is scattered much more than other colors because it travels as shorter, smaller waves.", font_size=24).move_to(DOWN*3.5)
        self.play(Transform(narration1, narration4))
        self.wait(3)

        self.play(FadeOut(sun, earth, molecules, narration1, *[anim.mobject for anim in scattering_blue]),FadeOut(heading))

        # Scene 3: Sunset Explanation
        # At sunset, the sunlight has to travel through much more of the atmosphere to reach your eyes.
        heading = Text("Sunset Explanation", font_size=60).move_to(UP*3.5) # Title
        self.play(FadeIn(heading))
        earth = Circle(radius=1, color=BLUE).move_to(DOWN*2.5)
        observer = Dot(point=earth.point_from_function(PI/4), color=RED)
        self.play(Create(earth), Create(observer))

        sun = Circle(radius=0.5, color=YELLOW).move_to(RIGHT*5 + UP*0.5)
        self.play(Create(sun))
        narration1 = Text("At sunset, the sunlight has to travel through much more of the atmosphere to reach your eyes.", font_size=24).move_to(DOWN*3.5)
        self.play(FadeIn(narration1))

        self.wait(5)

        # By the time it reaches you, most of the blue light has been scattered away.
        long_path = Line(start=sun.get_center(), end=observer.get_center(), color=YELLOW)
        self.play(Create(long_path))
        narration2 = Text("By the time it reaches you, most of the blue light has been scattered away.", font_size=24).move_to(DOWN*3.5)
        self.play(Transform(narration1, narration2))
        self.wait(5)

        # This leaves the longer wavelengths like red and orange to dominate, creating those beautiful sunset colors.
        sun.set_color(RED)
        self.play(sun.animate.set_color(RED))
        narration3 = Text("This leaves the longer wavelengths like red and orange to dominate, creating those beautiful sunset colors.", font_size=24).move_to(DOWN*3.5)
        self.play(Transform(narration1, narration3))
        self.wait(5)
        self.play(FadeOut(earth, observer, sun, long_path, narration1),FadeOut(heading))

        # Scene 4: Summary
        # So, the next time you look up at the blue sky or admire a stunning sunset, remember Rayleigh scattering – the reason for the beautiful colors we see!
        heading = Text("Summary", font_size=60).move_to(UP*3.5) # Title
        self.play(FadeIn(heading))
        # Create a split screen (placeholders for images/videos)
        left_square = Square(side_length=4, color=BLUE).move_to(LEFT*3)
        right_square = Square(side_length=4, color=RED).move_to(RIGHT*3)
        text_overlay = Text("Rayleigh Scattering: Blue sky and colorful sunsets!", font_size=30).move_to(DOWN*0.5)

        self.play(Create(left_square), Create(right_square), Write(text_overlay))
        narration = Text("So, the next time you look up at the blue sky or admire a stunning sunset, remember Rayleigh scattering – the reason for the beautiful colors we see!", font_size=24).move_to(DOWN*3.5)
        self.play(FadeIn(narration))
        self.wait(8)

        self.play(FadeOut(left_square, right_square, text_overlay, narration),FadeOut(heading))
        self.play(FadeOut(self.camera.background_color))
```