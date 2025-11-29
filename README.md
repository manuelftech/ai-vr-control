# ai-vr-control

# Python + Virtual Reality

This project demonstrates using Python and ChatGPT to control a Virtual Reality (VR) environment. ChatGPT is used to modify the state of 3D elements within the scene, which is built on the C# Unity Engine.

### Application running:
[![overview](https://img.youtube.com/vi/ndNi4NiTwP4/hqdefault.jpg)](https://youtu.be/ndNi4NiTwP4)

### Data Components
- Vector Store: Facilitates semantic search capabilities, enabling the Agent to access system usage instructions and operational guidelines.
- Redis Database: Serves as a centralized repository for storing, retrieving, and updating temporal 3D world state data, as well as maintaining a record of chat history and conversation context.
- Drive: Provides secure storage and retrieval of primary Agent Prompt instructions, leveraging Google Workspace integration to inform and refine Agent behavior.behavior.

### Directory Structure

*   `Orchestrator/` Python OpenAI application
    *   `config/` Configuration property management
    *   `controllers/` API endpoints and user input handling
    *   `core/` Main application helpers and managers
    *   `docs/` PDF documents ingested into the Vector Store for semantic search 
    *   `schemas/` Data Transfer Object (DTO) models for Redis database interactions 
    *   `models/` API data models (requests and responses)
    *   `prompts/` Prompt configuration structure and templates
    *   `repository/` Database integration layer
    *   `services/` OpenAI agent interaction logic
        *   `tools/` Agent tool definitions
*   `Assets/` Project assets (scenes, materials, prefabs) of the 3D environment
    *   `Scripts/` C# source code for environment control
        *   `Data/` Data management and processing logic
            *   `Models/` API data models (requests and responses)
            *   `ScriptableObjects/` Configurable interaction elements
        *   `Managers/` 3D element management (registration and processing)
            *   `Networking/` API communication logic (endpoint calls, status/prompt transmission)


### JSON schema for controlling the 3D environment
```json
{
    "Id": "ae89ab88-6d94-4235-b8f1-68c419d9d968",
    "Tag": "chair",
    "Name": "Chair_livingroom",
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
            "Z": 1.0
        }
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
        "Text": "The television 3D object is capable of rendering text-based content",
    }
}
```

Tools integrated and used for the creation, testing and validation of the project:
* OpenAI Python libraries (https://platform.openai.com/docs/overview)
* Redis Database (https://redis.io/)
* Drive (https://developers.google.com/workspace/drive)
* Unity Engine (https://unity.com/)
