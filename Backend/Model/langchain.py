from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import Field , BaseModel
from typing import  TypedDict, Optional, Dict, List, Any
import subprocess
import textwrap 
from langchain_core.prompts import PromptTemplate
from langchain.schema.messages import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

load_dotenv()

class ScenePlan(BaseModel):
    scene : str = Field(description="Detailed plan for the animation")
    scene_class_name : str = Field(description="Name of the scene class")

def plan_scene(prompt:str):
    system_prompt = """
        You are a manim expert and an excellent teacher who can explain complex
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
    chat_prompt = ChatPromptTemplate([
        ('system' , system_prompt),
        ("human" ,"Plan the scene for the following topic: {topic}")
    ])

    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        temperature=0.8
    )
    model = model.with_structured_output(ScenePlan)

    chain = chat_prompt | model
    
    response = chain.invoke({"topic" : prompt})

    return response

class ManimCodeResponse(BaseModel):
    code:str = Field(description="Complete valid Python code for the animation")
    explanation: Optional[str] = Field(None, description="Explanation of the code")
    error_fixes: Optional[List[str]] = Field(None, description="Error fixes if any")

def generate_code(plan:str, scene_class_name:str) -> ManimCodeResponse:
    """Generate a manim code from the plan"""
    system_prompt = f"""
You are a Python expert and a professional Manim animation developer.

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
    messages = chat_prompt.format_messages(plan=plan)

    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        temperature=0.8
    )
    model = model.with_structured_output(ManimCodeResponse) 

    response = model.invoke(messages)

    return response

import os
import time
import glob
import subprocess
from typing import Optional
from pydantic import BaseModel, Field

class ManimExecutionResponse(BaseModel):
    output: str = Field(description="Output of the execution")
    error: Optional[str] = Field(None, description="Error message")
    video_path : Optional[str] = Field(None , description="Path of the file")

def execute_manim_code(code: str, scene_class_name: str) -> ManimExecutionResponse:
    # Save code to a .py file
    file_path = f"{scene_class_name}.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f" Saved code to: {os.path.abspath(file_path)}")
    print(f" Starting Manim rendering...")

    # Build manim command
    cmd = [
        "python", "-m", "manim",
        "-pql",  # Preview mode, low quality
        file_path,
        scene_class_name
    ]

    # Run subprocess with correct encoding
    start_time = time.time()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'  # Prevent UnicodeDecodeError
    )
    duration = time.time() - start_time

    # Check result
    if result.returncode == 0:
        print(f" Animation completed successfully in {duration:.1f} seconds!")

        # Locate output video
        video_files = glob.glob(f"media/videos/{scene_class_name}/480p15/*.mp4", recursive=True)
        if video_files:
            video_path = max(video_files, key=os.path.getctime)
            print(f"📽️ Video saved to: {os.path.abspath(video_path)}")
            print("🎬 Playing animation:")
        else:
            print(" Render completed but no video file was found.")
        return ManimExecutionResponse(output=result.stdout , video_path=os.path.abspath(video_path))
    else:
        print(" Animation failed to render.")
        print("\n--- Stdout ---\n", result.stdout)
        print("\n--- Stderr ---\n", result.stderr)
        return ManimExecutionResponse(output=result.stdout, error=result.stderr)

class ManimErrorCorrectionResponse(BaseModel): 
    fixed_code: str = Field(...,description="The corrected Manim code that should resolve the errors")
    explanation: str = Field(description="Explanation of what was fixed and why")
    changes_made: List[str] = Field(description="List of specific changes made to fix the code")


def correct_manim_errors(code: str,error_message: str):
    """
    Analyze Manim errors and generate fixed code.

    Args:
        code: Original Manim code that produced errors
        error_message: Error output from the Manim execution
        scene_class_name: Name of the scene class

    Returns:
        ManimErrorCorrectionResponse with fixed code and explanation
    """
    system_prompt = """
    You are an expert Manim developer and debugger. Your task is to fix errors in Manim code.

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
    3. A list of specific changes you made
    """

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", """Please fix the errors in this Manim code.


            CODE WITH ERRORS:
            ```python
            {code}
            ```

            ERROR MESSAGE:
            ```
            {error_message}
            ```
            Please provide a complete fixed version of the code, along with an explanation of what went wrong and how you fixed it.
            """
        )
    ])
    messages = chat_prompt.format_messages(code = code , error_message = error_message)

    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        temperature=0.8
    )
    model = model.with_structured_output(ManimErrorCorrectionResponse) 

    response = model.invoke(messages)

    return response


def generate_and_execute_with_correction(prompt: str, max_correction_attempts: int = 3):
    storyboard_response = plan_scene(prompt)
    scene_class_name = storyboard_response.scene_class_name
    print(f" Scene planning complete: {scene_class_name}")

    # Step 2: Generate the code
    generated_code = generate_code(storyboard_response.scene, scene_class_name)
    current_code = generated_code.code
    print(" Initial code generation complete")

    # Step 3: Execute with correction loop
    for attempt in range(max_correction_attempts + 1):
        if attempt > 0:
            print(f"\n Correction attempt {attempt}/{max_correction_attempts}...")

        # Execute current code
        result = execute_manim_code(current_code, scene_class_name)

        # Check if execution succeeded
        if not result.error or "Animation completed successfully" in result.output:
            print(" Animation executed successfully!")
            break

        # If we've reached max attempts, exit
        if attempt >= max_correction_attempts:
            print(f" Failed to fix errors after {max_correction_attempts} attempts.")
            break

        # Try to fix the errors
        print("Errors detected, attempting to fix...")
        correction = correct_manim_errors(current_code, result.error)

        # Update the code for next attempt
        if correction == None:
            return None
        
        current_code = correction.fixed_code

    # Return results
    return {
        "scene_class_name": scene_class_name,
        "final_code": current_code,
        "plan": storyboard_response.scene,
        "execution_result": result,
        "correction_attempts": attempt,
        "video_path" : result.video_path
    }

