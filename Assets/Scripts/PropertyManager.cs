using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Text;
using System;
using System.Collections.Generic;
using System.Linq;

public class PropertyManager : MonoBehaviour
{
    // curl -iX POST http://localhost:5000/game-objects/status -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"prompt": "test"}'
    public string apiURL = "http://localhost:5000/game-objects/status";
    private ConstantForce constantForceComponent;
    private List<int> instanceIdsList = new List<int>();
    public string targetTag = "cube";

    void Start()
    {
        // Register this object in the Global manager, to modify gameObject properties
        if (GlobalManager.Instance != null)
        {
            GlobalManager.Instance.RegisterObject(this.gameObject);
            Debug.Log("GameObject registered: " + this.name);
        }
        else
        {
            Debug.LogError("GlobalManager instance not found! Cannot register " + this.name);
        }

        Dictionary<int, GameObject> newGameObjects = new Dictionary<int, GameObject>();
        foreach (var localGameObject in GlobalManager.Instance.objectMap)
        {
            Debug.Log("InstanceId: " + localGameObject.Key);
            Debug.Log("GameObject: " + localGameObject.Value);
            if (newGameObjects.TryGetValue(localGameObject.Key, out GameObject newGameObject))
            {
                Renderer renderer = localGameObject.Value.GetComponent<Renderer>();
                if (renderer != null)
                {
                    //renderer.material.color = newGameObject.color;
                    renderer.material.color = Color.red;
                    Debug.Log("Changed color of object with ID " + localGameObject.Key);
                }
                else
                {
                    Debug.LogError("Object with ID " + localGameObject.Key + " has no Renderer component.");
                }
            }
            else
            {
                Debug.LogWarning("Could not find an object with ID: " + localGameObject.Key);
            }
        }
    }

    // - 1) Register this Object when it starts
    // if (GlobalManager.Instance != null) {
    //     GlobalManager.Instance.RegisterObject(this.gameObject);
    // } else {
    //     Debug.LogError("GlobalManager instance not found! Cannot register " + this.name);
    // }

    // - 2) Find gameObjects based on their ID:
    // GameObject[] taggedObjects = GameObject.FindGameObjectsWithTag(targetTag);
    // if (taggedObjects.Length == 0)
    // {
    //     Debug.LogWarning("No GameObjects found with the tag: " + targetTag);
    //     return;
    // }
    // foreach (GameObject obj in taggedObjects)
    // {
    //     int id = obj.GetInstanceID();
    //     instanceIdsList.Add(id);
    //     Debug.Log("Found object: " + obj.name + " with Instance ID: " + id);
    // }
    // Debug.Log("Total objects found with tag '" + targetTag + "': " + instanceIdsList.Count);

    // - 3) Change value to make objects float:
    // constantForceComponent = GetComponent<ConstantForce>();
    // if (constantForceComponent != null)
    // {
    //     constantForceComponent.force = new Vector3(0, 9.82f, 0);
    // }
    // else
    // {
    //     Debug.LogError("ConstantForce component not found on this GameObject!");
    // }

    // - 4) Change the gameObject's color:
    // Renderer renderer = GetComponent<Renderer>();
    // if (renderer != null)
    // {
    //     renderer.material.color = Color.yellow; // Changes to a specific color
    // }

    // - 5) Call endpoint:
    // StartCoroutine(SendPostRequest());

    IEnumerator SendPostRequest()
    {
        // 1. Create the data payload as a C# class (optional, but cleaner)
        // You would typically define a class matching your JSON structure:
        // [System.Serializable]
        // public class UserData { public string username; public int age; }
        // UserData user = new UserData { username = "jdoe", age = 30 };
        // string jsonData = JsonUtility.ToJson(user);

        // For this example, we'll use a raw JSON string:
        string jsonData = "{\"prompt\":\"increase the gravity of all the green objects that are near the chair\"}";
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
        using (UnityWebRequest request = new UnityWebRequest(apiURL, "POST"))
        {
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            yield return request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + request.error);
            }
            else
            {
                Debug.Log("Received: " + request.downloadHandler.text);
            }
        }
        // Return the following Dictionary:
        // Dictionary<int, string> newGameObjects = apiResponseList.ToDictionary(gameObject => gameObject.id, gameObject => gameObject.color);
    }
}

public class GameObjectStatus
{
    // Properties of the Book class
    public string instanceId { get; set; }
    public string tag { get; set; } // cube
    public float color { get; set; }
    public int constantForce { get; set; } // 9.83
    public int x { get; set; }
    public int y { get; set; }
    public int z { get; set; }

}
