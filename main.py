from workflows.shorts_workflow import workflow

if __name__ == "__main__":
    agent = workflow()
    initial_state = {
        "user_topic": "What are the key differnces in OLAP vs OLTP systems?",
        "iteration": 1,
        "max_iteration": 3,
        "evaluation": "",
        "feedback": "",
        "feedback_history": []
    }
    result = agent.invoke(initial_state)
    print(result["script"])
    print(result)