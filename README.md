# ai-vr-control

# Python + Virtual Reality

This project demonstrates the integration of Python and ChatGPT for dynamic control of a Virtual Reality (VR) environment. The system utilizes a Python-based application to facilitate communication, allowing ChatGPT to modify the state of 3D elements within the scene, which is built on the Unity Engine.

### Application running:
[![overview](https://img.youtube.com/vi/bB7ghHSNvR4/hqdefault.jpg)](https://youtu.be/bB7ghHSNvR4)

### Data Components
- Vector Store: Facilitates semantic search capabilities, enabling the Agent to access system usage instructions and operational guidelines.
- Redis Database: Serves as a centralized repository for storing, retrieving, and updating temporal 3D world state data, as well as maintaining a record of chat history and conversation context.
- Drive: Provides secure storage and retrieval of primary Agent Prompt instructions, leveraging Google Workspace integration to inform and refine Agent behavior.

### Directory Structure

*   `Orchestrator/` Python OpenAI application
    *   `config/` Configuration property management
    *   `controllers/` API endpoints and user input handling
    *   `core/` Main application helpers and managers
    *   `docs/` PDF documents ingested into the Vector Store for semantic search 
    *   `schemas/` API data models (requests and responses)
    *   `prompts/` Prompt configuration structure and templates
    *   `repository/` Database integration layer
    *   `services/` OpenAI agent interaction logic
        *   `tools/` Agent tool definitions
*   `Assets/` Project assets (scenes, materials, prefabs) of the 3D environment
    *   `Scripts/` C# source code for environment control
        *   `Data/` Data management and processing logic
            *   `Models/` API data models (requests and responses)
            *   `ScriptableObjects/` Configurable interaction elements
        *   `Config/` Management of environment variables and properties
        *   `Managers/` 3D element management (registration and processing)
            *   `Networking/` API communication logic (endpoint calls, state/prompt transmission)


### JSON Schema Definition for 3D Environment Data
```json
{
    "Id": "ae89ab88-6d94-4235-b8f1-68c419d9d968",
    "Tag": "chair",
    "Name": "chair_livingroom",
    "Transform": {
        "Position": {
            "X": 13.7924623,
            "Y": -0.5499997,
            "Z": 7.930001
        },
        "Rotation": {
            "X": 5.40021574E-08,
            "Y": -0.9496292,
            "Z": -2.83122063E-07
        },
        "Scale": {
            "X": 1.0,
            "Y": 1.5,
            "Z": 0.5
        },
        "Reshape": 1.5,
    },
    "Components": {
        "ConstantForce": {
            "Force": {
                "X": 0.0,
                "Y": 9.83,
                "Z": 0.0
            },
            "RelativeTorque": {
                "X": 4.76,
                "Y": 0.0,
                "Z": 0.0
            }
        },
        "Color": "#FF0000",
        "Text": "Streaming data provided by the agent",
    }
}
```

Tools integrated and used for the creation, testing and validation of the project:
* OpenAI Python libraries (https://platform.openai.com/docs/overview)
* Redis Database (https://redis.io/)
* Drive (https://developers.google.com/workspace/drive)
* Unity Engine (https://unity.com/)
