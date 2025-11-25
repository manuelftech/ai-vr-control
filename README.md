# ai-vr-control

# Python + Virtual Reality

Project to control a Virtual Reality environment using Python with ChatGPT

The Virtual Reality environment is programmed in C# for Unity Engine, it allows ChatGPT to change the state of the 3D elements of the scene.

### Application running:
https://github.com/user-attachments/assets/e3112758-53c1-4b0e-9e11-0b5f836ff20f


### Project Structure

*   `Assets/` Scenes, Materials and prefabs to create a 3D scene
    *   `Scripts/`Programming scripts in C# to control the environment
*   `Orchestrator/` Python OpenAI main application
    *   `config/` Extraction of configuration properties
    *   `controllers/` API Endpoints and receiving user input
    *   `core/` Main application managers
    *   `prompts/` Structure and templates for prompt configuration
    *   `repository/` Database integration
    *   `services/` Chatbot Tools

### JSON structure to manipulate the 3D environment:
```json
{
    "Prompt": "I want the red sofas to levitate, become blue and start spinning",
    "VirtualRealityState": [
        {
            "Id": "ae89ab88-6d94-4235-b8f1-68c419d9d968",
            "Tag": "sofa",
            "Name": "Sofa_livingroom",
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
                    "X": 2.04,
                    "Y": 1.61,
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
                "Text": "the television object can display text",
            }
        }
    ]
}

```

Tools integrated and used for the creation, testing and validation of the project:
* OpenAI Python libraries (https://platform.openai.com/docs/overview)
* Redis Database (https://redis.io/)
* Unity Engine (https://unity.com/)
