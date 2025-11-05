using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Text;
using System;
using System.Collections.Generic;

public class PropertyManager : MonoBehaviour
{
    // curl -iX POST http://localhost:5000/game-objects/status -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"prompt": "test"}'
    public string apiURL = "http://localhost:5000/game-objects/status";
    private ConstantForce constantForceComponent;
    private List<int> instanceIdsList = new List<int>();
    public string targetTag = "cube";

    void Start()
    {
        if (GlobalManager.Instance != null)
        {
            GlobalManager.Instance.RegisterObject(this.gameObject);
            Debug.Log("GameObject registered: " + this.name);
        }
        else
        {
            Debug.LogError("GlobalManager instance not found! Cannot register " + this.name);
        }
        
        // if (objectMap.TryGetValue(targetID, out GameObject objToColor))
        // {
        //     Renderer renderer = objToColor.GetComponent<Renderer>();
        //     if (renderer != null)
        //     {
        //         renderer.material.color = newColor;
        //         Debug.Log("Changed color of object with ID " + targetID);
        //     }
        //     else
        //     {
        //         Debug.LogError("Object with ID " + targetID + " has no Renderer component.");
        //     }
        // }
        // else
        // {
        //     Debug.LogError("Object with ID " + targetID + " not found in map.");
        // }
        // When this object loads and starts in the scene,
        // it automatically finds the ObjectManager instance
        // and registers itself.

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

        // 2. Convert the JSON string to a byte array
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);

        // 3. Create the UnityWebRequest object
        using (UnityWebRequest request = new UnityWebRequest(apiURL, "POST"))
        {
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();

            // 4. Set the necessary Content-Type header to tell the server it's JSON
            request.SetRequestHeader("Content-Type", "application/json");

            // 5. Send the request and wait for a response
            yield return request.SendWebRequest();

            // 6. Check for errors
            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + request.error);
            }
            else
            {
                // 7. Success: Log the response received from the server
                Debug.Log("Received: " + request.downloadHandler.text);
            }
        }
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
