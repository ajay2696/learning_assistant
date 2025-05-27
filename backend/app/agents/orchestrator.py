from app.agents.sub_agents.study_planner.study_planner_agent import study_planner_agent
from app.agents.sub_agents.study_content.study_content_agent import study_content_agent, DayPlan
from app.agents.sub_agents.quiz.quiz_preparation_agent import quiz_preparation_agent, QuizDay
from google.adk.runners import Runner
from google.genai.types import Content, Part
import json
import asyncio, time, os, logging
from app.models.models import StudyPlanOutput, DayPlan, QuizDay

async def create_study_plan(session_service, request):
    """
    Create a comprehensive study plan with content and quizzes based on user input.
    
    Returns:
        dict: Complete study plan response with topics, content, and quizzes
    """
    user_id = request.user_id
    session_id = request.session_id
    APP_NAME = "my_study_planner"

    user_content = Content(role="user", parts=[Part(text=request.text)])

    try:
        # Initialize runners
        study_planner_runner = Runner(agent=study_planner_agent, app_name=APP_NAME, session_service=session_service)
        study_content_runner = Runner(agent=study_content_agent, app_name=APP_NAME, session_service=session_service)
        quiz_preparation_runner = Runner(agent=quiz_preparation_agent, app_name=APP_NAME, session_service=session_service)
        
        # Step 1: Generate initial study plan
        study_plan_obj = await _generate_study_plan(study_planner_runner, user_id, session_id, user_content)
        if not study_plan_obj:
            return {"error": "Failed to generate study plan"}
        
        # Step 2: Generate content and quizzes for each topic
        complete_study_plan = []
        
        for item in study_plan_obj.study_plan:
            try:
                # Generate study content
                day_plan_obj = await _generate_study_content(study_content_runner, user_id, session_id, item.topic)
                if not day_plan_obj:
                    logging.warning(f"Failed to generate content for topic: {item.topic}")
                    continue
                
                # Generate quizzes
                quiz_obj = await _generate_quizzes(quiz_preparation_runner, user_id, session_id, day_plan_obj)
                
                # Combine all information for this topic
                topic_data = {
                    "topic": item.topic,
                    "day_plan": day_plan_obj.dict() if day_plan_obj else None,
                    "quizzes": quiz_obj.dict() if quiz_obj else None
                }
                
                complete_study_plan.append(topic_data)
                
            except Exception as e:
                logging.error(f"Error processing topic {item.topic}: {str(e)}")
                # Continue with other topics even if one fails
                continue
        
        # Return complete study plan response
        return {
            "success": True,
            "study_plan": {
                "original_plan": study_plan_obj.dict(),
                "detailed_topics": complete_study_plan
            },
            "total_topics": len(complete_study_plan)
        }
        
    except Exception as e:
        logging.error(f"Error in create_study_plan: {str(e)}")
        return {"error": f"Failed to create study plan: {str(e)}"}


async def _generate_study_plan(runner, user_id, session_id, user_content):
    """Generate the initial study plan structure."""
    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=user_content):
            if event.is_final_response():
                if event.content and event.content.parts:
                    study_plan_text = event.content.parts[0].text
                    
                    try:
                        parsed_output = json.loads(study_plan_text)
                        return StudyPlanOutput(**parsed_output)
                    except (json.JSONDecodeError, TypeError) as e:
                        logging.error(f"Failed to parse study plan JSON: {str(e)}")
                        return None
        return None
        
    except Exception as e:
        logging.error(f"Error generating study plan: {str(e)}")
        return None


async def _generate_study_content(runner, user_id, session_id, topic):
    """Generate detailed study content for a specific topic."""
    try:
        content_request = Content(role="user", parts=[Part(text=f"Generate study content for: {topic}")])
        
        async for content_event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content_request):
            if content_event.is_final_response():
                if content_event.content and content_event.content.parts:
                    study_content = content_event.content.parts[0].text
                    
                    try:
                        parsed_output = json.loads(study_content)
                        day_plan_obj = DayPlan(**parsed_output)
                        print(f"Generated content for {topic}")
                        return day_plan_obj
                    except (json.JSONDecodeError, TypeError) as e:
                        logging.error(f"Failed to parse study content JSON for {topic}: {str(e)}")
                        return None
        return None
        
    except Exception as e:
        logging.error(f"Error generating study content for {topic}: {str(e)}")
        return None


async def _generate_quizzes(runner, user_id, session_id, day_plan_obj):
    """Generate quizzes based on the study content."""
    try:
        quiz_request = Content(role="user", parts=[Part(text=f"Prepare quizzes for: {day_plan_obj}")])
        
        async for quiz_event in runner.run_async(user_id=user_id, session_id=session_id, new_message=quiz_request):
            if quiz_event.is_final_response():
                if quiz_event.content and quiz_event.content.parts:
                    quizzes = quiz_event.content.parts[0].text
                    
                    try:
                        parsed_output = json.loads(quizzes)
                        quiz_obj = QuizDay(**parsed_output)
                        print(f"Generated quizzes for topic")
                        return quiz_obj
                    except (json.JSONDecodeError, TypeError) as e:
                        logging.error(f"Failed to parse quiz JSON: {str(e)}")
                        return None
        return None
        
    except Exception as e:
        logging.error(f"Error generating quizzes: {str(e)}")
        return None