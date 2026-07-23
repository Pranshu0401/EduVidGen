from dotenv import load_dotenv
import os
import subprocess
import time
import glob
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI


load_dotenv()

# =============================== #
#    Pydantic Output Models       #
# =============================== #

class ScenePlan(BaseModel):
    scene: str = Field(description="Detailed plan for the animation")
    scene_class_name: str = Field(description="Name of the scene class")


class ManimCodeResponse(BaseModel):
    code: str = Field(description="Complete valid Python code for the animation")
    explanation: Optional[str] = Field(None, description="Explanation of the code")
    error_fixes: Optional[List[str]] = Field(None, description="Error fixes if any")


class ManimExecutionResponse(BaseModel):
    output: str = Field(description="Output of the execution")
    error: Optional[str] = Field(None, description="Error message")
    video_path: Optional[str] = Field(None, description="Path of the file")


class ManimErrorCorrectionResponse(BaseModel):
    fixed_code: str = Field(..., description="The corrected Manim code")
    explanation: str = Field(description="Explanation of what was fixed and why")
    changes_made: List[str] = Field(description="List of specific changes made to fix the code")

# =============================== #
#     Scene Planning Function     #
# =============================== #

def plan_scene(prompt: str) -> ScenePlan:
    system_prompt = """You are a manim expert and an excellent teacher who can explain complex
        concepts in a clear and engaging way.
        You'll be working with a manim developer who will write a manim script
        to render a video that explains the concept.
        Your task is to plan the scenes **NOT TO WRITE CODE** for a 30-60 second video using objects
        and animations that are feasible to execute using Manim.
        Break it down into few scenes, use the following guidelines:

        INTRODUCTION AND EXPLANATION:
           - Introduce the concept with a clear title
           - Break down the concept into 2-3 key components
           - For each component, specify:
             * What visual elements to show (shapes, diagrams, etc.)
             * How they should move or transform
             * Exact narration text that syncs with the visuals

        PRACTICAL EXAMPLE:
           - Show a concrete, relatable example of the concept
           - Demonstrate cause and effect or the process in action
           - Include interactive elements if possible

        SUMMARY:
           - Recap the key points with visual reinforcement
           - Connect back to the introduction

        CRITICALLY IMPORTANT:
        For EACH scene:
        - Ensure that the visual elements do not overlap or go out of the frame
        - The scene measures 8 units in height and 14 units in width.
        The origin is in the center of the scene, which means that, for example,
        the upper left corner of the scene has coordinates [-7, 4, 0].
        - Ensure that objects are aligned properly (e.g., if creating a pendulum,
        the circle should be centered at the end of the line segment and move together with it as a cohesive unit)
        - Ensure that the scene is not too crowded
        - Ensure that the explanations are scientifically accurate and pedagogically effective
        - Specify the visual elements to include
        - Specify the exact narration text
        - Specify the transitions between scenes
        - When specifying colors, you MUST ONLY use standard Manim color constants like:
        BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, PINK, WHITE, BLACK, GRAY, GOLD, TEAL
"""
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Plan the scene for the following topic: {topic}")
    ])

    model = ChatOpenAI(
        model="llama3-70b-8192",
        openai_api_base="https://api.groq.com/openai/v1",
        openai_api_key=os.getenv("GROQ_API_KEY")
    )
    parser = PydanticOutputParser(pydantic_object=ScenePlan)
    chain = chat_prompt | model | parser
    return chain.invoke({"topic": prompt})

# =============================== #
#    Code Generation Function     #
# =============================== #

def generate_code(plan: str, scene_class_name: str) -> ManimCodeResponse:
    system_prompt = f"""You are a Python expert and a professional Manim animation developer.

You will be given a detailed multi-scene visualization plan that includes:
- Scene titles and layout
- Visual elements (shapes, arrows, graphs, etc.)
- Descriptions of object placements and transformations
- Narration text that should sync with visuals
- Frame constraints and styling details
- Scene transitions

Your task is to convert the described scenes into Python code using the Manim library (Community Edition), following these requirements:

🟢 STRUCTURE:
- All scenes must be implemented within a **single class**, e.g., `class scene_class_name()`.
- Each logical scene should be a separate block inside the `construct()` method, with clear section comments like:
  `# Scene 1: Introduction`

🟢 FUNCTIONALITY:
- Accurately place and animate all elements using Manim CE objects within a 14x8 unit frame
- Align visuals with narration using `.play()` and `.wait()` appropriately
- Display **narration text clearly on-screen** (centered at bottom or top) using `Text` or `MarkupText`
- Do **not tilt or rotate narration text** — keep it flat and readable and small in font 
- You may fade in/out or transform narration text as scenes progress
- Use standard Manim classes only: `Text`, `MathTex`, `Circle`, `Line`, `Arrow`, `VGroup`, etc.
- Use only Manim color constants like `BLUE`, `YELLOW`, `RED`, etc.
- Ensure visuals are clean, not overlapping, and scientifically accurate

🟢 IMPORTANT:
- Follow the scene plan exactly — do not invent or skip content
- For every narration segment:
  - Display the narration on screen as visible `Text`, centered and not angled (also run it as a form of subtitle removing old text then write new text on the bootom of screen)
  - Also include the narration as a **Python comment** in the code above that animation block
  - **DO NOT over zoom anywhere**
  - Use small font size to fit complete text on screen 
  - heading should always be on top of screen
  - if you are using 3D Scenes and camera functions do not forget To inherit from base class ThreeDScene , MovingCameraScene
  - dont use longer sentences if you want to use longer sentence then break it two meaningful parts and show one below each other
-No need to use Voiceover

OUTPUT: A single Python file, with one class and all scenes, ready to run in Manim.

  """

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Generate Manim code from this animation plan:\n\n{plan}")
    ])

    model = ChatOpenAI(
        model="llama3-70b-8192",
        openai_api_base="https://api.groq.com/openai/v1",
        openai_api_key=os.getenv("GROQ_API_KEY")
    )
    parser = PydanticOutputParser(pydantic_object=ManimCodeResponse)
    chain = chat_prompt | model | parser
    return chain.invoke({})

# =============================== #
#     Manim Execution Function    #
# =============================== #

def execute_manim_code(code: str, scene_class_name: str) -> ManimExecutionResponse:
    file_path = f"{scene_class_name}.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    cmd = ["python", "-m", "manim", "-pql", file_path, scene_class_name]
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    duration = time.time() - start_time

    if result.returncode == 0:
        video_files = glob.glob(f"media/videos/{scene_class_name}/480p15/*.mp4", recursive=True)
        video_path = max(video_files, key=os.path.getctime) if video_files else None
        return ManimExecutionResponse(output=result.stdout, video_path=os.path.abspath(video_path))
    else:
        return ManimExecutionResponse(output=result.stdout, error=result.stderr)

# =============================== #
#     Error Correction Function   #
# =============================== #

def correct_manim_errors(code: str, error_message: str) -> ManimErrorCorrectionResponse:
    system_prompt = """ You are an expert Manim developer and debugger. Your task is to fix errors in Manim code.

    ANALYZE the error message carefully to identify the root cause of the problem.
    EXAMINE the code to find where the error occurs.
    FIX the issue with the minimal necessary changes.

    Common Manim errors and solutions:
    1. 'AttributeError: object has no attribute X' - Check if you're using the correct method or property for that object type
    2. 'ValueError: No coordinates specified' - Ensure all mobjects have positions when created or moved
    3. 'ImportError: Cannot import name X' - Verify you're using the correct import from the right module
    4. 'TypeError: X() got an unexpected keyword argument Y' - Check parameter names and types
    5. 'Animation X: 0%' followed by crash - Look for errors in animation setup or objects being animated

    When fixing:
    - Preserve the overall structure and behavior of the animation
    - Ensure all objects are properly created and positioned
    - Check that all animations have proper timing and sequencing
    - Verify that voiceover sections have proper timing allocations
    - Maintain consistent naming and style throughout the code

    Your response must include:
    1. The complete fixed code
    2. A clear explanation of what was wrong and how you fixed it
    3. A list of specific changes you made"""

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", f"""Please fix the errors in this Manim code.
        
        CODE WITH ERRORS:
        ```python
        {code}
        ```

        ERROR MESSAGE:
        ```
        {error_message}
        ```
        """)
    ])

    model = ChatOpenAI(
        model="llama3-70b-8192",
        openai_api_base="https://api.groq.com/openai/v1",
        openai_api_key=os.getenv("GROQ_API_KEY")
    )
    parser = PydanticOutputParser(pydantic_object=ManimErrorCorrectionResponse)
    chain = chat_prompt | model | parser
    return chain.invoke({})

# =============================== #
#  Main Flow with Auto-Correction #
# =============================== #

def generate_and_execute_with_correction(prompt: str, max_correction_attempts: int = 3):
    storyboard_response = plan_scene(prompt)
    scene_class_name = storyboard_response.scene_class_name
    print(f"[✓] Scene planned: {scene_class_name}")

    generated_code = generate_code(storyboard_response.scene, scene_class_name)
    current_code = generated_code.code

    for attempt in range(max_correction_attempts + 1):
        print(f"\n[Attempt {attempt}] Executing code...")
        result = execute_manim_code(current_code, scene_class_name)

        if not result.error:
            print(f"[✓] Success! Video path: {result.video_path}")
            break

        if attempt >= max_correction_attempts:
            print("[X] Max correction attempts reached.")
            break

        print("[!] Error detected. Attempting to fix...")
        correction = correct_manim_errors(current_code, result.error)
        current_code = correction.fixed_code

    return {
        "scene_class_name": scene_class_name,
        "final_code": current_code,
        "plan": storyboard_response.scene,
        "execution_result": result,
        "correction_attempts": attempt,
        "video_path": result.video_path
    }
